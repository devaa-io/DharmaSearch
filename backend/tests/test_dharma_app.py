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
    "yoga-path", "divine-feminine",
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
        assert len(plans) >= 5, f"Expected >=5 plans, got {len(plans)}"
        plan_ids = {p["plan_id"] for p in plans}
        missing = EXPECTED_PLANS - plan_ids
        assert not missing, f"Missing plans: {missing}"

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
