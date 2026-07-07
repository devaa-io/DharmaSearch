from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

from fastapi import FastAPI, APIRouter, Request, HTTPException, Depends
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import bcrypt
import jwt
import secrets
import uuid
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")

JWT_ALGORITHM = "HS256"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Password Hashing ---
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# --- JWT ---
def get_jwt_secret() -> str:
    return os.environ["JWT_SECRET"]

def create_access_token(user_id: str, email: str) -> str:
    payload = {"sub": user_id, "email": email, "exp": datetime.now(timezone.utc) + timedelta(minutes=60), "type": "access"}
    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALGORITHM)

def create_refresh_token(user_id: str) -> str:
    payload = {"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(days=7), "type": "refresh"}
    return jwt.encode(payload, get_jwt_secret(), algorithm=JWT_ALGORITHM)

# --- Auth Helper ---
async def get_current_user(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        user["_id"] = str(user["_id"])
        user.pop("password_hash", None)
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# --- Models ---
class RegisterInput(BaseModel):
    name: str
    email: str
    password: str

class LoginInput(BaseModel):
    email: str
    password: str

class SearchInput(BaseModel):
    query: str
    text_filter: Optional[str] = None

class ExplainInput(BaseModel):
    verse_id: str

class BookmarkInput(BaseModel):
    verse_id: str

class PlanCreate(BaseModel):
    title: str
    description: Optional[str] = ""
    verse_ids: List[str]
    duration_days: Optional[int] = None

class AnnotationCreate(BaseModel):
    verse_id: str
    text: str
    tradition: Optional[str] = None

class CorrectionCreate(BaseModel):
    verse_id: str
    field: str
    current_value: str
    suggested_value: str
    reason: Optional[str] = ""

# --- Auth Routes ---
@api_router.post("/auth/register")
async def register(input: RegisterInput):
    email = input.email.lower().strip()
    existing = await db.users.find_one({"email": email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(input.password)
    user_doc = {
        "email": email,
        "name": input.name,
        "password_hash": hashed,
        "role": "user",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    result = await db.users.insert_one(user_doc)
    user_id = str(result.inserted_id)
    access_token = create_access_token(user_id, email)
    refresh_token = create_refresh_token(user_id)
    response = JSONResponse(content={
        "id": user_id, "email": email, "name": input.name, "role": "user"
    })
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="lax", max_age=3600, path="/")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=False, samesite="lax", max_age=604800, path="/")
    return response

@api_router.post("/auth/login")
async def login(input: LoginInput):
    email = input.email.lower().strip()
    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not verify_password(input.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    user_id = str(user["_id"])
    access_token = create_access_token(user_id, email)
    refresh_token = create_refresh_token(user_id)
    response = JSONResponse(content={
        "id": user_id, "email": email, "name": user.get("name", ""), "role": user.get("role", "user")
    })
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=False, samesite="lax", max_age=3600, path="/")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=False, samesite="lax", max_age=604800, path="/")
    return response

@api_router.post("/auth/logout")
async def logout():
    response = JSONResponse(content={"message": "Logged out"})
    response.delete_cookie("access_token", path="/")
    response.delete_cookie("refresh_token", path="/")
    return response

@api_router.get("/auth/me")
async def get_me(request: Request):
    user = await get_current_user(request)
    return user

@api_router.post("/auth/refresh")
async def refresh_token(request: Request):
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="No refresh token")
    try:
        payload = jwt.decode(token, get_jwt_secret(), algorithms=[JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user = await db.users.find_one({"_id": ObjectId(payload["sub"])})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        user_id = str(user["_id"])
        new_access = create_access_token(user_id, user["email"])
        response = JSONResponse(content={"message": "Token refreshed"})
        response.set_cookie(key="access_token", value=new_access, httponly=True, secure=False, samesite="lax", max_age=3600, path="/")
        return response
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

# --- Scripture Routes ---
@api_router.get("/public/sample-verses")
async def get_sample_verses():
    """Public endpoint - returns curated sample verses for landing page preview"""
    sample_ids = [
        "bg-2-47", "bg-2-20", "bg-4-7", "bg-18-66",
        "brihad-1", "katha-1", "ys-1-2", "dm-4-2",
        "nar-1-1", "sb-4-1", "sl-1-1", "vc-2-1",
        "ram-6-2", "mb-1-1", "rv-1-2", "ls-2-1"
    ]
    verses = await db.verses.find({"verse_id": {"$in": sample_ids}}, {"_id": 0}).to_list(20)
    # Sort by the order defined above
    order = {vid: i for i, vid in enumerate(sample_ids)}
    verses.sort(key=lambda v: order.get(v["verse_id"], 999))
    return verses

@api_router.get("/public/search")
async def public_search(q: str):
    """Public keyword search - limited to 5 results for preview"""
    import re
    words = [re.escape(w) for w in q.strip().split() if w]
    if not words:
        return []
    pattern = "|".join(words)
    query = {"$or": [
        {"translation": {"$regex": pattern, "$options": "i"}},
        {"keywords": {"$regex": pattern, "$options": "i"}}
    ]}
    verses = await db.verses.find(query, {"_id": 0}).limit(5).to_list(5)
    return verses

@api_router.get("/scriptures")
async def get_scriptures():
    texts = await db.scriptures.find({}, {"_id": 0}).to_list(100)
    return texts

@api_router.get("/scriptures/{text_id}/chapters")
async def get_chapters(text_id: str):
    pipeline = [
        {"$match": {"text_id": text_id}},
        {"$group": {"_id": "$chapter", "chapter_name": {"$first": "$chapter_name"}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    chapters = await db.verses.aggregate(pipeline).to_list(100)
    result = [{"chapter": c["_id"], "chapter_name": c.get("chapter_name", ""), "verse_count": c["count"]} for c in chapters]
    return result

@api_router.get("/scriptures/{text_id}/chapters/{chapter}/verses")
async def get_verses(text_id: str, chapter: int):
    verses = await db.verses.find(
        {"text_id": text_id, "chapter": chapter},
        {"_id": 0}
    ).sort("verse_number", 1).to_list(500)
    return verses

@api_router.get("/scriptures/{text_id}/verses/{verse_id}")
async def get_verse(text_id: str, verse_id: str):
    verse = await db.verses.find_one({"verse_id": verse_id}, {"_id": 0})
    if not verse:
        raise HTTPException(status_code=404, detail="Verse not found")
    return verse

# --- Search ---
@api_router.get("/search")
async def keyword_search(q: str, text_filter: Optional[str] = None):
    import re
    words = [re.escape(w) for w in q.strip().split() if w]
    if not words:
        return []
    # Match ANY word in the query (OR logic)
    pattern = "|".join(words)
    query = {"$or": [
        {"text": {"$regex": pattern, "$options": "i"}},
        {"translation": {"$regex": pattern, "$options": "i"}},
        {"keywords": {"$regex": pattern, "$options": "i"}}
    ]}
    if text_filter:
        query["text_id"] = text_filter
    verses = await db.verses.find(query, {"_id": 0}).limit(50).to_list(50)
    # Score by number of word matches and sort
    def score(v):
        text = f"{v.get('translation','')} {v.get('keywords','')} {v.get('text','')}".lower()
        return sum(1 for w in words if w.lower() in text)
    verses.sort(key=score, reverse=True)
    return verses

# --- AI Search ---
@api_router.post("/ai-search")
async def ai_search(input: SearchInput, request: Request):
    user = await get_current_user(request)
    from emergentintegrations.llm.chat import LlmChat, UserMessage

    api_key = os.environ.get("EMERGENT_LLM_KEY")
    session_id = f"search-{user['_id']}-{uuid.uuid4().hex[:8]}"

    # Get all verses for context
    query_filter = {}
    if input.text_filter:
        query_filter["text_id"] = input.text_filter

    all_verses = await db.verses.find(query_filter, {"_id": 0}).to_list(2000)

    # Build a condensed index of verses for the AI
    verse_index = []
    for v in all_verses:
        verse_index.append(f"[{v['verse_id']}] {v['text_name']} Ch.{v['chapter']} V.{v['verse_number']}: {v['translation'][:200]}")

    verse_text = "\n".join(verse_index)

    try:
        chat = LlmChat(
            api_key=api_key,
            session_id=session_id,
            system_message=f"""You are a Hindu scripture scholar. Given the user's query, find the most relevant verses from this collection. Return ONLY a JSON array of verse_ids (strings) that match, ordered by relevance. Return at most 10 results. If nothing matches, return an empty array [].

Available verses:
{verse_text}"""
        )
        chat.with_model("openai", "gpt-5.2")

        user_msg = UserMessage(text=f"Find verses related to: {input.query}")
        response = await chat.send_message(user_msg)

        # Parse the response to get verse IDs
        import json
        try:
            text = response.strip()
            if "```" in text:
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            verse_ids = json.loads(text.strip())
        except Exception:
            verse_ids = []

        # Fetch the actual verses
        if verse_ids:
            matched_verses = await db.verses.find(
                {"verse_id": {"$in": verse_ids}},
                {"_id": 0}
            ).to_list(50)
            id_order = {vid: i for i, vid in enumerate(verse_ids)}
            matched_verses.sort(key=lambda v: id_order.get(v["verse_id"], 999))
            return matched_verses
        return []
    except Exception as e:
        logger.error(f"AI search error: {e}")
        raise HTTPException(status_code=503, detail="AI search is temporarily unavailable. Please try keyword search instead.")

# --- AI Explain ---
@api_router.post("/ai-explain")
async def ai_explain(input: ExplainInput, request: Request):
    user = await get_current_user(request)
    verse = await db.verses.find_one({"verse_id": input.verse_id}, {"_id": 0})
    if not verse:
        raise HTTPException(status_code=404, detail="Verse not found")

    from emergentintegrations.llm.chat import LlmChat, UserMessage

    api_key = os.environ.get("EMERGENT_LLM_KEY")
    session_id = f"explain-{user['_id']}-{uuid.uuid4().hex[:8]}"

    try:
        chat = LlmChat(
            api_key=api_key,
            session_id=session_id,
            system_message="You are a revered Hindu scripture scholar. Provide a clear, insightful explanation of the given verse. Include its context within the text, philosophical significance, and practical application. Keep it concise but profound (3-4 paragraphs)."
        )
        chat.with_model("openai", "gpt-5.2")

        verse_context = f"""
Text: {verse['text_name']}
Chapter: {verse['chapter']} - {verse.get('chapter_name', '')}
Verse: {verse['verse_number']}
Sanskrit/Original: {verse.get('text', '')}
Translation: {verse['translation']}
"""
        user_msg = UserMessage(text=f"Please explain this verse:\n{verse_context}")
        explanation = await chat.send_message(user_msg)

        return {"verse": verse, "explanation": explanation}
    except Exception as e:
        logger.error(f"AI explain error: {e}")
        raise HTTPException(status_code=503, detail="AI explanation is temporarily unavailable. Please try again later.")

# --- Audio Recitation (TTS) ---
class TTSInput(BaseModel):
    verse_id: str
    voice: Optional[str] = "sage"

@api_router.post("/tts")
async def generate_tts(input: TTSInput, request: Request):
    user = await get_current_user(request)
    verse = await db.verses.find_one({"verse_id": input.verse_id}, {"_id": 0})
    if not verse:
        raise HTTPException(status_code=404, detail="Verse not found")

    # Check cache first
    cached = await db.tts_cache.find_one(
        {"verse_id": input.verse_id, "voice": input.voice}, {"_id": 0}
    )
    if cached:
        return {"audio_base64": cached["audio_base64"], "cached": True}

    # Generate audio
    try:
        from emergentintegrations.llm.openai import OpenAITextToSpeech
        api_key = os.environ.get("EMERGENT_LLM_KEY")
        tts = OpenAITextToSpeech(api_key=api_key)

        # Build recitation text: Sanskrit first, then translation
        recitation_text = ""
        if verse.get("text"):
            recitation_text += verse["text"] + ". "
        recitation_text += verse["translation"]

        # Truncate to 4096 chars (TTS limit)
        if len(recitation_text) > 4000:
            recitation_text = recitation_text[:4000]

        audio_base64 = await tts.generate_speech_base64(
            text=recitation_text,
            model="tts-1-hd",
            voice=input.voice,
            speed=0.85
        )

        # Cache for future use
        await db.tts_cache.update_one(
            {"verse_id": input.verse_id, "voice": input.voice},
            {"$set": {
                "verse_id": input.verse_id,
                "voice": input.voice,
                "audio_base64": audio_base64,
                "created_at": datetime.now(timezone.utc).isoformat()
            }},
            upsert=True
        )

        return {"audio_base64": audio_base64, "cached": False}
    except Exception as e:
        logger.error(f"TTS error: {e}")
        raise HTTPException(status_code=503, detail="Audio generation is temporarily unavailable. Please try again later.")

# --- Daily Verse ---
@api_router.get("/daily-verse")
async def get_daily_verse():
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # Use date as seed for consistent daily verse
    import hashlib
    seed = int(hashlib.md5(today.encode()).hexdigest(), 16)
    total = await db.verses.count_documents({})
    if total == 0:
        return None
    index = seed % total
    verse = await db.verses.find({}, {"_id": 0}).skip(index).limit(1).to_list(1)
    return verse[0] if verse else None

# --- Bookmarks ---
@api_router.post("/bookmarks")
async def add_bookmark(input: BookmarkInput, request: Request):
    user = await get_current_user(request)
    existing = await db.bookmarks.find_one({
        "user_id": user["_id"], "verse_id": input.verse_id
    })
    if existing:
        raise HTTPException(status_code=400, detail="Already bookmarked")
    await db.bookmarks.insert_one({
        "user_id": user["_id"],
        "verse_id": input.verse_id,
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    return {"message": "Bookmarked"}

@api_router.get("/bookmarks")
async def get_bookmarks(request: Request):
    user = await get_current_user(request)
    bookmarks = await db.bookmarks.find(
        {"user_id": user["_id"]}, {"_id": 0}
    ).to_list(500)
    # Fetch verse details
    verse_ids = [b["verse_id"] for b in bookmarks]
    if verse_ids:
        verses = await db.verses.find(
            {"verse_id": {"$in": verse_ids}}, {"_id": 0}
        ).to_list(500)
        return verses
    return []

@api_router.delete("/bookmarks/{verse_id}")
async def remove_bookmark(verse_id: str, request: Request):
    user = await get_current_user(request)
    await db.bookmarks.delete_one({
        "user_id": user["_id"], "verse_id": verse_id
    })
    return {"message": "Bookmark removed"}

# --- Reading Plans ---
@api_router.get("/plans")
async def get_plans(request: Request):
    user = await get_current_user(request)
    # Get all pre-built plans + user's custom plans
    plans = await db.reading_plans.find(
        {"$or": [{"is_prebuilt": True}, {"created_by": user["_id"]}]},
        {"_id": 0}
    ).to_list(100)
    # Get user's progress
    progress = await db.plan_progress.find(
        {"user_id": user["_id"]}, {"_id": 0}
    ).to_list(100)
    progress_map = {p["plan_id"]: p for p in progress}
    for plan in plans:
        prog = progress_map.get(plan["plan_id"], {})
        plan["completed_days"] = prog.get("completed_days", [])
        plan["started"] = prog.get("started", False)
    return plans

@api_router.get("/plans/{plan_id}")
async def get_plan(plan_id: str, request: Request):
    user = await get_current_user(request)
    plan = await db.reading_plans.find_one({"plan_id": plan_id}, {"_id": 0})
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    # Get progress
    prog = await db.plan_progress.find_one(
        {"user_id": user["_id"], "plan_id": plan_id}, {"_id": 0}
    )
    plan["completed_days"] = prog.get("completed_days", []) if prog else []
    plan["started"] = bool(prog)
    # Get verse details for each day
    all_verse_ids = []
    for day in plan.get("days", []):
        all_verse_ids.extend(day.get("verse_ids", []))
    verses = await db.verses.find({"verse_id": {"$in": all_verse_ids}}, {"_id": 0}).to_list(500)
    verse_map = {v["verse_id"]: v for v in verses}
    plan["verse_details"] = verse_map
    return plan

@api_router.post("/plans")
async def create_plan(input: PlanCreate, request: Request):
    user = await get_current_user(request)
    plan_id = f"custom-{uuid.uuid4().hex[:8]}"
    # Split verses into days
    verse_ids = input.verse_ids
    days_count = input.duration_days or max(1, len(verse_ids))
    per_day = max(1, len(verse_ids) // days_count)
    days = []
    for i in range(days_count):
        start = i * per_day
        end = start + per_day if i < days_count - 1 else len(verse_ids)
        day_verses = verse_ids[start:end]
        if day_verses:
            days.append({"day": i + 1, "verse_ids": day_verses})
    plan = {
        "plan_id": plan_id,
        "title": input.title,
        "description": input.description,
        "is_prebuilt": False,
        "created_by": user["_id"],
        "days": days,
        "total_days": len(days),
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.reading_plans.insert_one(plan)
    plan.pop("_id", None)
    return plan

@api_router.post("/plans/{plan_id}/progress")
async def update_progress(plan_id: str, request: Request):
    user = await get_current_user(request)
    body = await request.json()
    day_number = body.get("day_number")
    if day_number is None:
        raise HTTPException(status_code=400, detail="day_number required")
    prog = await db.plan_progress.find_one({"user_id": user["_id"], "plan_id": plan_id})
    if prog:
        completed = prog.get("completed_days", [])
        if day_number not in completed:
            completed.append(day_number)
        await db.plan_progress.update_one(
            {"user_id": user["_id"], "plan_id": plan_id},
            {"$set": {"completed_days": completed}}
        )
    else:
        await db.plan_progress.insert_one({
            "user_id": user["_id"],
            "plan_id": plan_id,
            "started": True,
            "completed_days": [day_number],
            "started_at": datetime.now(timezone.utc).isoformat()
        })
    return {"message": "Progress updated"}

# --- Community Annotations ---
@api_router.get("/annotations/{verse_id}")
async def get_annotations(verse_id: str):
    """Get all annotations for a verse (public)"""
    annotations = await db.annotations.find(
        {"verse_id": verse_id}, {"_id": 0}
    ).sort("upvotes", -1).to_list(100)
    return annotations

@api_router.post("/annotations")
async def create_annotation(input: AnnotationCreate, request: Request):
    user = await get_current_user(request)
    annotation_id = f"ann-{uuid.uuid4().hex[:10]}"
    doc = {
        "annotation_id": annotation_id,
        "verse_id": input.verse_id,
        "text": input.text,
        "tradition": input.tradition,
        "user_id": user["_id"],
        "user_name": user.get("name", "Anonymous"),
        "upvotes": 0,
        "downvotes": 0,
        "is_verified": False,
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.annotations.insert_one(doc)
    doc.pop("_id", None)
    return doc

@api_router.post("/annotations/{annotation_id}/vote")
async def vote_annotation(annotation_id: str, request: Request):
    user = await get_current_user(request)
    body = await request.json()
    vote = body.get("vote")  # 1 or -1
    if vote not in [1, -1]:
        raise HTTPException(status_code=400, detail="Vote must be 1 or -1")
    existing = await db.annotation_votes.find_one({
        "user_id": user["_id"], "annotation_id": annotation_id
    })
    if existing:
        if existing["vote"] == vote:
            return {"message": "Already voted"}
        # Change vote
        old_vote = existing["vote"]
        await db.annotation_votes.update_one(
            {"user_id": user["_id"], "annotation_id": annotation_id},
            {"$set": {"vote": vote}}
        )
        inc = {"upvotes": 0, "downvotes": 0}
        if old_vote == 1:
            inc["upvotes"] = -1
        else:
            inc["downvotes"] = -1
        if vote == 1:
            inc["upvotes"] = inc.get("upvotes", 0) + 1
        else:
            inc["downvotes"] = inc.get("downvotes", 0) + 1
        await db.annotations.update_one(
            {"annotation_id": annotation_id}, {"$inc": inc}
        )
    else:
        await db.annotation_votes.insert_one({
            "user_id": user["_id"],
            "annotation_id": annotation_id,
            "vote": vote
        })
        field = "upvotes" if vote == 1 else "downvotes"
        await db.annotations.update_one(
            {"annotation_id": annotation_id}, {"$inc": {field: 1}}
        )
    return {"message": "Vote recorded"}

@api_router.delete("/annotations/{annotation_id}")
async def delete_annotation(annotation_id: str, request: Request):
    user = await get_current_user(request)
    ann = await db.annotations.find_one({"annotation_id": annotation_id})
    if not ann:
        raise HTTPException(status_code=404, detail="Annotation not found")
    if ann["user_id"] != user["_id"] and user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    await db.annotations.delete_one({"annotation_id": annotation_id})
    await db.annotation_votes.delete_many({"annotation_id": annotation_id})
    return {"message": "Annotation deleted"}

# --- Corrections / Feedback ---
@api_router.post("/corrections")
async def submit_correction(input: CorrectionCreate, request: Request):
    user = await get_current_user(request)
    correction_id = f"cor-{uuid.uuid4().hex[:10]}"
    doc = {
        "correction_id": correction_id,
        "verse_id": input.verse_id,
        "field": input.field,
        "current_value": input.current_value,
        "suggested_value": input.suggested_value,
        "reason": input.reason,
        "user_id": user["_id"],
        "user_name": user.get("name", "Anonymous"),
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    await db.corrections.insert_one(doc)
    doc.pop("_id", None)
    return doc

@api_router.get("/corrections")
async def get_corrections(request: Request, status: Optional[str] = None):
    user = await get_current_user(request)
    query = {}
    if user.get("role") != "admin":
        query["user_id"] = user["_id"]
    if status:
        query["status"] = status
    corrections = await db.corrections.find(query, {"_id": 0}).sort("created_at", -1).to_list(200)
    return corrections

@api_router.patch("/corrections/{correction_id}")
async def review_correction(correction_id: str, request: Request):
    user = await get_current_user(request)
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin only")
    body = await request.json()
    new_status = body.get("status")  # "approved" or "rejected"
    if new_status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Status must be 'approved' or 'rejected'")
    correction = await db.corrections.find_one({"correction_id": correction_id})
    if not correction:
        raise HTTPException(status_code=404, detail="Correction not found")
    await db.corrections.update_one(
        {"correction_id": correction_id},
        {"$set": {"status": new_status, "reviewed_by": user["_id"], "reviewed_at": datetime.now(timezone.utc).isoformat()}}
    )
    # If approved, apply the correction to the verse
    if new_status == "approved":
        field = correction["field"]
        if field in ["translation", "text", "keywords", "chapter_name"]:
            await db.verses.update_one(
                {"verse_id": correction["verse_id"]},
                {"$set": {field: correction["suggested_value"]}}
            )
    return {"message": f"Correction {new_status}"}

# --- Startup ---
async def seed_admin():
    admin_email = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
    existing = await db.users.find_one({"email": admin_email})
    if existing is None:
        hashed = hash_password(admin_password)
        await db.users.insert_one({
            "email": admin_email,
            "password_hash": hashed,
            "name": "Admin",
            "role": "admin",
            "created_at": datetime.now(timezone.utc).isoformat()
        })
        logger.info(f"Admin seeded: {admin_email}")
    elif not verify_password(admin_password, existing["password_hash"]):
        await db.users.update_one(
            {"email": admin_email},
            {"$set": {"password_hash": hash_password(admin_password)}}
        )

async def seed_scriptures():
    count = await db.verses.count_documents({})
    if count > 0:
        logger.info(f"Scriptures already seeded ({count} verses)")
        return

    from scripture_data import get_all_verses, get_scripture_metadata
    
    metadata = get_scripture_metadata()
    for m in metadata:
        await db.scriptures.update_one(
            {"text_id": m["text_id"]},
            {"$set": m},
            upsert=True
        )

    verses = get_all_verses()
    if verses:
        await db.verses.insert_many(verses)
        logger.info(f"Seeded {len(verses)} verses")

    # Create indexes
    await db.verses.create_index("text_id")
    await db.verses.create_index("verse_id", unique=True)
    await db.verses.create_index([("translation", "text")])
    await db.users.create_index("email", unique=True)
    await db.bookmarks.create_index([("user_id", 1), ("verse_id", 1)])
    await db.reading_plans.create_index("plan_id", unique=True)
    await db.plan_progress.create_index([("user_id", 1), ("plan_id", 1)])
    await db.annotations.create_index("verse_id")
    await db.annotations.create_index("annotation_id", unique=True)
    await db.annotation_votes.create_index([("user_id", 1), ("annotation_id", 1)])
    await db.corrections.create_index("correction_id", unique=True)
    await db.corrections.create_index("status")
    await db.tts_cache.create_index([("verse_id", 1), ("voice", 1)])

    # Seed pre-built reading plans
    await seed_reading_plans()

async def seed_reading_plans():
    plans = [
        {
            "plan_id": "gita-7-days",
            "title": "7 Days of Gita Wisdom",
            "description": "Explore the essential teachings of the Bhagavad Gita in one week. Each day covers a key theme.",
            "is_prebuilt": True, "created_by": "system", "total_days": 7,
            "days": [
                {"day": 1, "title": "Arjuna's Crisis", "verse_ids": ["bg-1-47", "bg-2-7"]},
                {"day": 2, "title": "The Eternal Soul", "verse_ids": ["bg-2-13", "bg-2-20", "bg-2-22"]},
                {"day": 3, "title": "Karma Yoga", "verse_ids": ["bg-2-47", "bg-2-48", "bg-3-19"]},
                {"day": 4, "title": "Divine Incarnation", "verse_ids": ["bg-4-7", "bg-4-8"]},
                {"day": 5, "title": "Mind & Meditation", "verse_ids": ["bg-6-5", "bg-6-6", "bg-6-34"]},
                {"day": 6, "title": "Devotion & Surrender", "verse_ids": ["bg-9-22", "bg-9-26", "bg-12-13"]},
                {"day": 7, "title": "Final Wisdom", "verse_ids": ["bg-18-65", "bg-18-66", "bg-18-78"]}
            ]
        },
        {
            "plan_id": "upanishad-intro",
            "title": "Introduction to Upanishads",
            "description": "Discover the philosophical heart of Hinduism through the key Mahavakyas and teachings of the major Upanishads.",
            "is_prebuilt": True, "created_by": "system", "total_days": 5,
            "days": [
                {"day": 1, "title": "The Great Prayers", "verse_ids": ["brihad-1", "isha-1"]},
                {"day": 2, "title": "The Nature of Self", "verse_ids": ["katha-2", "katha-3", "brihad-2"]},
                {"day": 3, "title": "Arise, Awake!", "verse_ids": ["katha-1", "chando-1"]},
                {"day": 4, "title": "Om and Brahman", "verse_ids": ["mandukya-1", "chando-2", "mundaka-2"]},
                {"day": 5, "title": "Bliss and Truth", "verse_ids": ["taitt-2", "taitt-1", "mundaka-1"]}
            ]
        },
        {
            "plan_id": "kerala-devotion",
            "title": "Kerala's Devotional Heritage",
            "description": "A journey through the sacred texts of Kerala — from Guruvayur's Narayaneeyam to Shankaracharya's Advaita philosophy.",
            "is_prebuilt": True, "created_by": "system", "total_days": 7,
            "days": [
                {"day": 1, "title": "Guruvayur's Prayer", "verse_ids": ["nar-1-1", "nar-1-2"]},
                {"day": 2, "title": "Krishna's Glory", "verse_ids": ["sb-1-1", "sb-2-1", "sb-2-2"]},
                {"day": 3, "title": "Nine Forms of Bhakti", "verse_ids": ["sb-4-1", "sb-3-1"]},
                {"day": 4, "title": "Ezhuthachan's Ramayana", "verse_ids": ["ar-1-1", "ar-1-2", "ar-2-1"]},
                {"day": 5, "title": "The Divine Mother", "verse_ids": ["ls-1-1", "ls-2-1", "sl-1-1"]},
                {"day": 6, "title": "Shankaracharya's Wisdom", "verse_ids": ["vc-1-1", "vc-2-1", "vc-2-2"]},
                {"day": 7, "title": "Final Vision", "verse_ids": ["nar-3-1", "vs-1-1", "ar-3-1"]}
            ]
        },
        {
            "plan_id": "yoga-path",
            "title": "The Yoga Path",
            "description": "Follow Patanjali's systematic guide to yoga and meditation — from practice to liberation.",
            "is_prebuilt": True, "created_by": "system", "total_days": 4,
            "days": [
                {"day": 1, "title": "What is Yoga?", "verse_ids": ["ys-1-1", "ys-1-2", "ys-1-3"]},
                {"day": 2, "title": "Practice & Detachment", "verse_ids": ["ys-1-12", "ys-1-33"]},
                {"day": 3, "title": "The Eight Limbs", "verse_ids": ["ys-2-1", "ys-2-29", "ys-2-46"]},
                {"day": 4, "title": "Meditation & Liberation", "verse_ids": ["ys-3-1", "ys-3-2", "ys-4-34"]}
            ]
        },
        {
            "plan_id": "divine-feminine",
            "title": "The Divine Feminine",
            "description": "Explore the power and grace of the Goddess through the Devi Mahatmyam, Lalita Sahasranama, and Soundarya Lahari.",
            "is_prebuilt": True, "created_by": "system", "total_days": 5,
            "days": [
                {"day": 1, "title": "Mahamaya", "verse_ids": ["dm-1-2", "dm-1-3"]},
                {"day": 2, "title": "Durga's Battle", "verse_ids": ["dm-2-3", "dm-3-2"]},
                {"day": 3, "title": "Shakti in All", "verse_ids": ["dm-4-2", "dm-4-3", "dm-4-7"]},
                {"day": 4, "title": "Thousand Names", "verse_ids": ["ls-1-1", "ls-1-2", "ls-2-1"]},
                {"day": 5, "title": "Waves of Beauty", "verse_ids": ["sl-1-1", "sl-1-2", "dm-11-2"]}
            ]
        },
        {
            "plan_id": "karkkidakam-30",
            "title": "Karkkidakam - 30 Days of Ramayana",
            "description": "The traditional Kerala practice of reading the Adhyatma Ramayanam during Karkkidakam (July-August). Every Kerala household reads the Ramayana during this monsoon month for spiritual purification.",
            "is_prebuilt": True, "created_by": "system", "total_days": 30,
            "tags": ["karkkidakam", "kerala", "seasonal"],
            "days": [
                {"day": 1, "title": "Invocation", "verse_ids": ["ar-1-1"]},
                {"day": 2, "title": "Hari Nama Keerthanam", "verse_ids": ["ar-1-2"]},
                {"day": 3, "title": "The Essence of Ramayana", "verse_ids": ["ar-2-1"]},
                {"day": 4, "title": "Rama's Qualities", "verse_ids": ["ram-1-3", "ram-1-4"]},
                {"day": 5, "title": "The First Verse of Poetry", "verse_ids": ["ram-1-5"]},
                {"day": 6, "title": "The Ideal Man", "verse_ids": ["ram-1-2"]},
                {"day": 7, "title": "Exile & Duty", "verse_ids": ["ram-2-1", "ram-2-2"]},
                {"day": 8, "title": "Serving Rama", "verse_ids": ["ram-2-3"]},
                {"day": 9, "title": "Selflessness", "verse_ids": ["ram-2-4"]},
                {"day": 10, "title": "Dharma Protects", "verse_ids": ["ram-3-1"]},
                {"day": 11, "title": "Protection from Sin", "verse_ids": ["ram-3-2"]},
                {"day": 12, "title": "Sita's Abduction", "verse_ids": ["ram-3-3"]},
                {"day": 13, "title": "Alliance with Sugriva", "verse_ids": ["ram-4-1"]},
                {"day": 14, "title": "Rama's Grief", "verse_ids": ["ram-4-2"]},
                {"day": 15, "title": "Hanuman's Quest", "verse_ids": ["ram-5-1"]},
                {"day": 16, "title": "Five Virtues", "verse_ids": ["ram-5-2"]},
                {"day": 17, "title": "Sita's Endurance", "verse_ids": ["ram-5-3"]},
                {"day": 18, "title": "Sita's Sorrow", "verse_ids": ["ram-5-4"]},
                {"day": 19, "title": "Righteousness Prevails", "verse_ids": ["ram-6-1"]},
                {"day": 20, "title": "Motherland Over Heaven", "verse_ids": ["ram-6-2", "ar-3-1"]},
                {"day": 21, "title": "Conquering Evil", "verse_ids": ["ram-6-3"]},
                {"day": 22, "title": "Aditya Hridayam", "verse_ids": ["ram-6-4"]},
                {"day": 23, "title": "Victory of Rama", "verse_ids": ["ram-7-1"]},
                {"day": 24, "title": "Salutations to Rama", "verse_ids": ["ram-7-2"]},
                {"day": 25, "title": "Merit of Reading", "verse_ids": ["ram-7-3"]},
                {"day": 26, "title": "Bhakti - Nine Forms", "verse_ids": ["sb-4-1"]},
                {"day": 27, "title": "Chanting Krishna's Name", "verse_ids": ["sb-3-1"]},
                {"day": 28, "title": "Guruvayurappan", "verse_ids": ["nar-1-1", "nar-3-1"]},
                {"day": 29, "title": "Shankaracharya's Teaching", "verse_ids": ["vc-2-1"]},
                {"day": 30, "title": "Final Blessings", "verse_ids": ["ar-1-1", "vs-1-2", "ls-2-1"]}
            ]
        }
    ]
    for p in plans:
        await db.reading_plans.update_one(
            {"plan_id": p["plan_id"]}, {"$set": p}, upsert=True
        )
    logger.info(f"Seeded {len(plans)} reading plans")

@app.on_event("startup")
async def startup():
    await seed_admin()
    await seed_scriptures()
    await seed_reading_plans()
    # Write test credentials
    os.makedirs("/app/memory", exist_ok=True)
    with open("/app/memory/test_credentials.md", "w") as f:
        f.write("# Test Credentials\n\n")
        f.write("## Admin Account\n")
        f.write("- Email: admin@example.com\n")
        f.write("- Password: admin123\n")
        f.write("- Role: admin\n\n")
        f.write("## Auth Endpoints\n")
        f.write("- POST /api/auth/register\n")
        f.write("- POST /api/auth/login\n")
        f.write("- POST /api/auth/logout\n")
        f.write("- GET /api/auth/me\n")
        f.write("- POST /api/auth/refresh\n")

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()

# Include router and middleware
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
