
# loaders/gita.py
import requests

VERSE_URL = "https://raw.githubusercontent.com/gita/gita/main/data/verse.json"
TRANS_URL = "https://raw.githubusercontent.com/gita/gita/main/data/translation.json"

def load():
    verse_response = requests.get(VERSE_URL, timeout=30)
    verse_response.raise_for_status()
    translation_response = requests.get(TRANS_URL, timeout=30)
    translation_response.raise_for_status()
    verses = verse_response.json()
    trans = translation_response.json()
    # pick one complete public-domain English translation
    english = {t["verse_id"]: t["description"]
               for t in trans
               if t["lang"] == "english" and t["authorName"] == "Swami Sivananda"}
    rows = []
    for v in verses:
        rows.append({
            "text": v["text"],                     # Devanagari (with inline tags, cleaned by pipeline)
            "transliteration": v["transliteration"],  # proper IAST with diacritics
            "translation": english.get(v["id"], ""),
            "chapter": v["chapter_number"],
            "verse": v["verse_number"],
        })
    return rows
