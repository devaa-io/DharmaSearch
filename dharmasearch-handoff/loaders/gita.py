
# loaders/gita.py
import requests

VERSE_URL = "https://raw.githubusercontent.com/gita/gita/main/data/verse.json"
TRANS_URL = "https://raw.githubusercontent.com/gita/gita/main/data/translation.json"

def load():
    verses = requests.get(VERSE_URL, timeout=30).json()
    trans  = requests.get(TRANS_URL, timeout=30).json()
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
