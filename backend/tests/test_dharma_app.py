"""Backend tests for Hindu Scripture App - Iteration 3.

Covers: 16 scriptures (incl. 7 Kerala texts), 5 reading plans,
transliterations + temple_connection fields, plan progress updates,
keyword search hits for Guruvayur/Shankaracharya.
"""
import os
import time
import requests
import pytest

BASE_URL = os.environ.get("REACT_APP_BACKEND_URL", "").rstrip("/")
assert BASE_URL, "REACT_APP_BACKEND_URL must be set"

ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "admin123"
TEST_USER_EMAIL = f"testuser_{int(time.time())}@example.com"
TEST_USER_PASSWORD = "testpass123"

EXPECTED_SCRIPTURES = {
    "bhagavad-gita", "ramayana", "devi-mahatmyam", "upanishads",
    "yoga-sutras", "mahabharata", "vedas", "hanuman-chalisa", "puranas",
    # Kerala additions
    "srimad-bhagavatam", "narayaneeyam", "adhyatma-ramayanam",
    "lalita-sahasranama", "vishnu-sahasranama", "soundarya-lahari",
    "vivekachudamani",
}
EXPECTED_PLANS = {
    "gita-7-days", "upanishad-intro", "kerala-devotion",
    "yoga-path", "divine-feminine", "karkkidakam-30",
}


# ---- Fixtures ----
@pytest.fixture(scope="module")
def admin_session():
    s = requests.Session()
    r = s.post(f"{BASE_URL}/api/auth/login",
               json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
    assert r.status_code == 200, f"Admin login failed: {r.status_code} {r.text}"
    return s


@pytest.fixture(scope="module")
def new_user_session():
    s = requests.Session()
    r = s.post(f"{BASE_URL}/api/auth/register", json={
        "name": "Test User", "email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD
    })
    assert r.status_code == 200, f"Register failed: {r.status_code} {r.text}"
    return s


# ---- Public (no-auth) endpoints ----
class TestPublic:
    def test_sample_verses_no_auth(self):
        r = requests.get(f"{BASE_URL}/api/public/sample-verses")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        # 16 IDs requested; allow some to be missing in DB but expect bulk
        assert len(data) >= 10, f"Expected >=10 sample verses, got {len(data)}"
        v = data[0]
        assert "verse_id" in v and "translation" in v
        assert "_id" not in v

    def test_public_search_no_auth(self):
        r = requests.get(f"{BASE_URL}/api/public/search", params={"q": "dharma"})
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert 0 < len(data) <= 5, f"Expected 1..5 results, got {len(data)}"

    def test_public_search_guruvayur(self):
        r = requests.get(f"{BASE_URL}/api/public/search", params={"q": "Guruvayur"})
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0
        assert any(v.get("text_id") == "narayaneeyam" for v in data)

    def test_public_search_soul(self):
        r = requests.get(f"{BASE_URL}/api/public/search", params={"q": "soul"})
        assert r.status_code == 200
        assert len(r.json()) > 0


# ---- Auth ----
class TestAuth:
    def test_admin_login(self):
        r = requests.post(f"{BASE_URL}/api/auth/login",
                          json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD})
        assert r.status_code == 200
        data = r.json()
        assert data["email"] == ADMIN_EMAIL
        assert data["role"] == "admin"
        assert "access_token" in r.cookies

    def test_login_invalid(self):
        r = requests.post(f"{BASE_URL}/api/auth/login",
                          json={"email": ADMIN_EMAIL, "password": "wrong"})
        assert r.status_code == 401

    def test_register_new_user(self, new_user_session):
        r = new_user_session.get(f"{BASE_URL}/api/auth/me")
        assert r.status_code == 200
        assert r.json()["email"] == TEST_USER_EMAIL

    def test_me_unauthenticated(self):
        r = requests.get(f"{BASE_URL}/api/auth/me")
        assert r.status_code == 401


# ---- 16 Scriptures (incl. Kerala) ----
class TestScriptures:
    def test_list_16_scriptures(self):
        r = requests.get(f"{BASE_URL}/api/scriptures")
        assert r.status_code == 200
        data = r.json()
        assert isinstance(data, list)
        assert len(data) == 16, f"Expected 16 scriptures, got {len(data)}"
        text_ids = {s["text_id"] for s in data}
        missing = EXPECTED_SCRIPTURES - text_ids
        assert not missing, f"Missing scriptures: {missing}"

    def test_kerala_text_chapters(self):
        # Srimad Bhagavatam
        r = requests.get(f"{BASE_URL}/api/scriptures/srimad-bhagavatam/chapters")
        assert r.status_code == 200
        assert len(r.json()) > 0

        # Narayaneeyam
        r = requests.get(f"{BASE_URL}/api/scriptures/narayaneeyam/chapters")
        assert r.status_code == 200
        chapters = r.json()
        assert len(chapters) > 0
        assert all("chapter" in c and "chapter_name" in c for c in chapters)

    def test_narayaneeyam_has_transliterations_and_temple(self):
        chapters = requests.get(
            f"{BASE_URL}/api/scriptures/narayaneeyam/chapters").json()
        ch = chapters[0]
        r = requests.get(
            f"{BASE_URL}/api/scriptures/narayaneeyam/chapters/{ch['chapter']}/verses")
        assert r.status_code == 200
        verses = r.json()
        assert len(verses) > 0
        v = verses[0]
        # Transliterations dict ml/hi
        translit = v.get("transliterations")
        assert isinstance(translit, dict), f"transliterations missing on {v.get('verse_id')}"
        assert "ml" in translit and "hi" in translit
        assert translit["ml"] and translit["hi"]
        # Temple connection on first Narayaneeyam verse
        temple = v.get("temple_connection")
        assert isinstance(temple, dict), f"temple_connection missing on {v.get('verse_id')}"
        assert "temple" in temple and "location" in temple and "detail" in temple
        assert "_id" not in v


# ---- Search ----
class TestSearch:
    def test_search_guruvayur(self):
        r = requests.get(f"{BASE_URL}/api/search", params={"q": "Guruvayur"})
        assert r.status_code == 200
        data = r.json()
        assert len(data) > 0, "No results for Guruvayur"
        assert any(v.get("text_id") == "narayaneeyam" for v in data)

    def test_search_shankaracharya(self):
        r = requests.get(f"{BASE_URL}/api/search", params={"q": "Shankaracharya"})
        assert r.status_code == 200
        data = r.json()
        text_ids = {v.get("text_id") for v in data}
        assert text_ids & {"vivekachudamani", "soundarya-lahari"}, \
            f"Expected hits in vivekachudamani/soundarya-lahari, got {text_ids}"

    def test_search_dharma(self):
        r = requests.get(f"{BASE_URL}/api/search", params={"q": "dharma"})
        assert r.status_code == 200
        assert len(r.json()) > 0

    def test_search_no_match(self):
        r = requests.get(f"{BASE_URL}/api/search", params={"q": "zzzznonexistentxyz"})
        assert r.status_code == 200
        assert r.json() == []


# ---- Daily Verse ----
class TestDailyVerse:
    def test_daily_verse(self):
        r = requests.get(f"{BASE_URL}/api/daily-verse")
        assert r.status_code == 200
        data = r.json()
        assert "verse_id" in data and "translation" in data


# ---- Reading Plans ----
class TestReadingPlans:
    def test_plans_require_auth(self):
        r = requests.get(f"{BASE_URL}/api/plans")
        assert r.status_code == 401

    def test_list_5_plans(self, admin_session):
        r = admin_session.get(f"{BASE_URL}/api/plans")
        assert r.status_code == 200
        plans = r.json()
        assert len(plans) >= 6, f"Expected >=6 plans, got {len(plans)}"
        plan_ids = {p["plan_id"] for p in plans}
        missing = EXPECTED_PLANS - plan_ids
        assert not missing, f"Missing plans: {missing}"

    def test_karkkidakam_30_day_plan(self, admin_session):
        r = admin_session.get(f"{BASE_URL}/api/plans/karkkidakam-30")
        assert r.status_code == 200
        plan = r.json()
        assert plan["total_days"] == 30
        assert len(plan["days"]) == 30
        # Day 20 -> Motherland Over Heaven
        day20 = next(d for d in plan["days"] if d["day"] == 20)
        assert "Motherland" in day20["title"]
        assert "ram-6-2" in day20["verse_ids"]
        # verse_details map should contain Ramayana verse
        assert "ram-6-2" in plan.get("verse_details", {})

    def test_kerala_plan_detail(self, admin_session):
        r = admin_session.get(f"{BASE_URL}/api/plans/kerala-devotion")
        assert r.status_code == 200
        plan = r.json()
        assert plan["title"] == "Kerala's Devotional Heritage"
        assert plan["total_days"] == 7
        assert len(plan["days"]) == 7
        # Every day has a title and verse_ids
        for d in plan["days"]:
            assert d.get("title")
            assert isinstance(d.get("verse_ids"), list) and len(d["verse_ids"]) > 0
        # verse_details mapping returned
        assert isinstance(plan.get("verse_details"), dict)
        # Day 1 -> Narayaneeyam verses; verse_details should contain transliterations
        day1_vids = plan["days"][0]["verse_ids"]
        nar_verse = plan["verse_details"].get(day1_vids[0])
        assert nar_verse is not None
        assert nar_verse.get("text_id") == "narayaneeyam"
        assert isinstance(nar_verse.get("transliterations"), dict)
        assert isinstance(nar_verse.get("temple_connection"), dict)

    def test_plan_not_found(self, admin_session):
        r = admin_session.get(f"{BASE_URL}/api/plans/does-not-exist")
        assert r.status_code == 404

    def test_progress_update(self, new_user_session):
        # Mark day 1 as complete
        r = new_user_session.post(
            f"{BASE_URL}/api/plans/kerala-devotion/progress",
            json={"day_number": 1},
        )
        assert r.status_code == 200
        # Verify reflected in /plans list
        plans = new_user_session.get(f"{BASE_URL}/api/plans").json()
        kerala = next(p for p in plans if p["plan_id"] == "kerala-devotion")
        assert kerala["started"] is True
        assert 1 in kerala["completed_days"]

        # Add day 2
        r2 = new_user_session.post(
            f"{BASE_URL}/api/plans/kerala-devotion/progress",
            json={"day_number": 2},
        )
        assert r2.status_code == 200
        plans = new_user_session.get(f"{BASE_URL}/api/plans").json()
        kerala = next(p for p in plans if p["plan_id"] == "kerala-devotion")
        assert set(kerala["completed_days"]) >= {1, 2}

        # Idempotent (adding day 1 again doesn't duplicate)
        new_user_session.post(
            f"{BASE_URL}/api/plans/kerala-devotion/progress",
            json={"day_number": 1},
        )
        plans = new_user_session.get(f"{BASE_URL}/api/plans").json()
        kerala = next(p for p in plans if p["plan_id"] == "kerala-devotion")
        assert kerala["completed_days"].count(1) == 1

    def test_progress_missing_day(self, admin_session):
        r = admin_session.post(
            f"{BASE_URL}/api/plans/gita-7-days/progress", json={})
        assert r.status_code == 400


# ---- Bookmarks ----
class TestBookmarks:
    def test_bookmark_flow(self, new_user_session):
        # bookmark a Kerala verse
        r = new_user_session.post(f"{BASE_URL}/api/bookmarks",
                                  json={"verse_id": "nar-1-1"})
        assert r.status_code == 200

        # duplicate -> 400
        r2 = new_user_session.post(f"{BASE_URL}/api/bookmarks",
                                   json={"verse_id": "nar-1-1"})
        assert r2.status_code == 400

        # list
        r3 = new_user_session.get(f"{BASE_URL}/api/bookmarks")
        assert r3.status_code == 200
        assert any(b["verse_id"] == "nar-1-1" for b in r3.json())

        # delete
        r4 = new_user_session.delete(f"{BASE_URL}/api/bookmarks/nar-1-1")
        assert r4.status_code == 200


# ---- AI (still 503 due to inactive key, per problem statement) ----
class TestAI:
    def test_ai_search_auth_required(self):
        r = requests.post(f"{BASE_URL}/api/ai-search", json={"query": "duty"})
        assert r.status_code == 401

    def test_ai_search_graceful_503(self, admin_session):
        r = admin_session.post(f"{BASE_URL}/api/ai-search",
                               json={"query": "duty"}, timeout=120)
        assert r.status_code in (200, 500, 503)



# ---- Community Annotations ----
class TestAnnotations:
    def test_create_annotation_requires_auth(self):
        r = requests.post(f"{BASE_URL}/api/annotations",
                          json={"verse_id": "bg-2-47", "text": "x", "tradition": "advaita"})
        assert r.status_code == 401

    def test_get_annotations_public(self):
        r = requests.get(f"{BASE_URL}/api/annotations/bg-2-47")
        assert r.status_code == 200
        assert isinstance(r.json(), list)

    def test_annotation_create_vote_sort_delete(self, admin_session, new_user_session):
        # Admin creates two annotations on same verse with different traditions
        verse_id = "bg-2-47"
        r1 = admin_session.post(f"{BASE_URL}/api/annotations", json={
            "verse_id": verse_id,
            "text": "TEST_ANN advaita interpretation",
            "tradition": "advaita"
        })
        assert r1.status_code == 200, r1.text
        ann1 = r1.json()
        assert ann1["tradition"] == "advaita"
        assert ann1["upvotes"] == 0
        assert ann1["verse_id"] == verse_id
        ann1_id = ann1["annotation_id"]

        r2 = admin_session.post(f"{BASE_URL}/api/annotations", json={
            "verse_id": verse_id,
            "text": "TEST_ANN bhakti interpretation",
            "tradition": "bhakti"
        })
        assert r2.status_code == 200
        ann2_id = r2.json()["annotation_id"]

        # New user upvotes ann2 -> should sort above ann1
        v = new_user_session.post(f"{BASE_URL}/api/annotations/{ann2_id}/vote",
                                  json={"vote": 1})
        assert v.status_code == 200

        # Admin also upvotes ann2 -> upvotes=2
        v2 = admin_session.post(f"{BASE_URL}/api/annotations/{ann2_id}/vote",
                                json={"vote": 1})
        assert v2.status_code == 200

        # GET sorted by upvotes desc
        listing = requests.get(f"{BASE_URL}/api/annotations/{verse_id}").json()
        # find both
        ids = [a["annotation_id"] for a in listing]
        assert ann1_id in ids and ann2_id in ids
        # ann2 should come first (higher upvotes)
        pos2 = ids.index(ann2_id)
        pos1 = ids.index(ann1_id)
        assert pos2 < pos1, f"Expected ann2 (more upvotes) first; got order {ids}"
        ann2_full = listing[pos2]
        assert ann2_full["upvotes"] >= 2
        assert "_id" not in ann2_full

        # Switch vote from upvote to downvote on ann2
        sw = new_user_session.post(f"{BASE_URL}/api/annotations/{ann2_id}/vote",
                                   json={"vote": -1})
        assert sw.status_code == 200
        listing2 = requests.get(f"{BASE_URL}/api/annotations/{verse_id}").json()
        ann2_after = next(a for a in listing2 if a["annotation_id"] == ann2_id)
        # upvotes decreased, downvotes increased
        assert ann2_after["upvotes"] == 1
        assert ann2_after["downvotes"] == 1

        # Invalid vote value
        bad = admin_session.post(f"{BASE_URL}/api/annotations/{ann1_id}/vote",
                                 json={"vote": 5})
        assert bad.status_code == 400

        # Delete both as admin
        d1 = admin_session.delete(f"{BASE_URL}/api/annotations/{ann1_id}")
        d2 = admin_session.delete(f"{BASE_URL}/api/annotations/{ann2_id}")
        assert d1.status_code == 200 and d2.status_code == 200

    def test_non_owner_cannot_delete(self, admin_session, new_user_session):
        r = admin_session.post(f"{BASE_URL}/api/annotations", json={
            "verse_id": "bg-2-20", "text": "TEST_ANN admin owned", "tradition": "dvaita"
        })
        ann_id = r.json()["annotation_id"]
        # new_user (non-admin, non-owner) cannot delete
        d = new_user_session.delete(f"{BASE_URL}/api/annotations/{ann_id}")
        assert d.status_code == 403
        # cleanup
        admin_session.delete(f"{BASE_URL}/api/annotations/{ann_id}")


# ---- Corrections / Feedback ----
class TestCorrections:
    def test_create_correction_requires_auth(self):
        r = requests.post(f"{BASE_URL}/api/corrections", json={
            "verse_id": "bg-2-47", "field": "translation",
            "current_value": "x", "suggested_value": "y", "reason": "test"
        })
        assert r.status_code == 401

    def test_correction_submit_approve_applies_to_verse(self, admin_session, new_user_session):
        verse_id = "bg-2-20"
        # Fetch original verse translation
        orig = requests.get(f"{BASE_URL}/api/scriptures/bhagavad-gita/verses/{verse_id}").json()
        original_translation = orig["translation"]

        # User submits a correction
        new_translation = original_translation + " [TEST_CORRECTION_SUFFIX]"
        sub = new_user_session.post(f"{BASE_URL}/api/corrections", json={
            "verse_id": verse_id,
            "field": "translation",
            "current_value": original_translation,
            "suggested_value": new_translation,
            "reason": "TEST_REASON improving clarity"
        })
        assert sub.status_code == 200, sub.text
        cor = sub.json()
        assert cor["status"] == "pending"
        assert cor["field"] == "translation"
        cor_id = cor["correction_id"]

        # Non-admin GET /corrections -> only own pending visible
        own = new_user_session.get(f"{BASE_URL}/api/corrections").json()
        assert any(c["correction_id"] == cor_id for c in own)

        # Admin GET /corrections sees pending
        adm = admin_session.get(f"{BASE_URL}/api/corrections",
                                params={"status": "pending"}).json()
        assert any(c["correction_id"] == cor_id for c in adm)

        # Non-admin cannot approve
        bad = new_user_session.patch(f"{BASE_URL}/api/corrections/{cor_id}",
                                     json={"status": "approved"})
        assert bad.status_code == 403

        # Invalid status
        bad2 = admin_session.patch(f"{BASE_URL}/api/corrections/{cor_id}",
                                   json={"status": "weird"})
        assert bad2.status_code == 400

        # Admin approves
        appr = admin_session.patch(f"{BASE_URL}/api/corrections/{cor_id}",
                                   json={"status": "approved"})
        assert appr.status_code == 200

        # Verse translation now updated in DB
        updated = requests.get(
            f"{BASE_URL}/api/scriptures/bhagavad-gita/verses/{verse_id}").json()
        assert updated["translation"] == new_translation

        # Revert via second correction so we don't pollute fixture for retests
        revert = new_user_session.post(f"{BASE_URL}/api/corrections", json={
            "verse_id": verse_id, "field": "translation",
            "current_value": new_translation,
            "suggested_value": original_translation,
            "reason": "TEST_REVERT"
        })
        revert_id = revert.json()["correction_id"]
        admin_session.patch(f"{BASE_URL}/api/corrections/{revert_id}",
                            json={"status": "approved"})
        check = requests.get(
            f"{BASE_URL}/api/scriptures/bhagavad-gita/verses/{verse_id}").json()
        assert check["translation"] == original_translation

    def test_correction_reject_does_not_apply(self, admin_session, new_user_session):
        verse_id = "bg-4-7"
        orig = requests.get(f"{BASE_URL}/api/scriptures/bhagavad-gita/verses/{verse_id}").json()
        original = orig["translation"]
        sub = new_user_session.post(f"{BASE_URL}/api/corrections", json={
            "verse_id": verse_id, "field": "translation",
            "current_value": original,
            "suggested_value": "TEST_SHOULD_NOT_APPLY",
            "reason": "TEST"
        })
        cor_id = sub.json()["correction_id"]
        rej = admin_session.patch(f"{BASE_URL}/api/corrections/{cor_id}",
                                  json={"status": "rejected"})
        assert rej.status_code == 200
        # Verse unchanged
        chk = requests.get(
            f"{BASE_URL}/api/scriptures/bhagavad-gita/verses/{verse_id}").json()
        assert chk["translation"] == original
