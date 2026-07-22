#!/usr/bin/env python3
"""Legacy single-text merger. Prefer merge_upanishads.py for a full rebuild."""
import json, shutil, pathlib

BASE = pathlib.Path(__file__).resolve().parents[1]
APP = BASE / "app_data.json"
DATA = BASE / "data" / "katha-upanishad.json"
TID = "katha-upanishad"
TN = "Katha Upanishad"

VALLI_NAMES = {
    1: "Adhyaya I, Valli 1", 2: "Adhyaya I, Valli 2", 3: "Adhyaya I, Valli 3",
    4: "Adhyaya II, Valli 1", 5: "Adhyaya II, Valli 2", 6: "Adhyaya II, Valli 3",
}

app = json.load(open(APP, encoding="utf-8"))
ds = json.load(open(DATA, encoding="utf-8"))
assert len(ds) == 120, f"expected 120 Katha verses, got {len(ds)}"

new_verses = []
for v in ds:
    ch, vn, iast = v["chapter"], v["verse"], v["iast"]
    new_verses.append({
        "id": f"katha-up-{ch}-{vn}", "tid": TID, "tn": TN,
        "ch": ch, "cn": VALLI_NAMES[ch], "vn": vn, "complete": True,
        "roman": iast, "dev": v["devanagari"], "iast": iast, "en": v["english"],
        "kw": "", "scripts": {k: v["scripts"][k] for k in ("ml", "ta", "te", "kn")}, "temple": "",
    })

for nv in new_verses:
    for f in ("dev", "iast", "en"):
        assert nv[f], f"{nv['id']} missing {f}"
    for s in ("ml", "ta", "te", "kn"):
        assert nv["scripts"][s], f"{nv['id']} missing script {s}"

text_entry = {"id": TID, "name": TN,
              "desc": ("120 verses in 6 vallis (2 adhyayas), Krishna Yajurveda. The boy Naciketas "
                       "questions Death itself and receives the teaching on the immortal Self beyond "
                       "the body. English by Max Muller (SBE Vol. 15, 1884, public domain)."),
              "lang": "Sanskrit", "tv": 120, "complete": True}
app["texts"] = [t for t in app["texts"] if t.get("id") != TID]
insert_at = next((i for i, t in enumerate(app["texts"]) if t.get("id") == "kena-upanishad"), -1) + 1
app["texts"].insert(insert_at, text_entry)

app["chapterMeta"][TID] = {str(ch): {"dev": "", "tr": name, "mean": ""} for ch, name in VALLI_NAMES.items()}

app["verses"] = [v for v in app["verses"] if v.get("tid") != TID]
app["verses"].extend(new_verses)

shutil.copy2(APP, APP.with_suffix(".json.bak"))
json.dump(app, open(APP, "w", encoding="utf-8"), ensure_ascii=False)

print("MERGE OK")
print("  texts:", len(app["texts"]), "| katha complete:", next(t for t in app["texts"] if t["id"] == TID)["complete"])
print("  total verses:", len(app["verses"]), "| katha verses:", sum(1 for v in app["verses"] if v["tid"] == TID))
by_ch = {}
for v in app["verses"]:
    if v["tid"] == TID: by_ch[v["ch"]] = by_ch.get(v["ch"], 0) + 1
print("  verses per valli:", by_ch)
