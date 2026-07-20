#!/usr/bin/env python3
"""Merge the completed Mundaka Upanishad dataset into app_data.json (idempotent)."""
import json, shutil, pathlib

BASE = pathlib.Path("/mnt/c/Users/Devan Narayanan/Downloads/DharmaSearch/dharmasearch-handoff")
APP = BASE / "app_data.json"
DATA = BASE / "data" / "mundaka-upanishad.json"
TID = "mundaka-upanishad"
TN = "Mundaka Upanishad"

SECTION_NAMES = {
    1: "Mundaka I, Khanda 1", 2: "Mundaka I, Khanda 2",
    3: "Mundaka II, Khanda 1", 4: "Mundaka II, Khanda 2",
    5: "Mundaka III, Khanda 1", 6: "Mundaka III, Khanda 2",
}

app = json.load(open(APP, encoding="utf-8"))
ds = json.load(open(DATA, encoding="utf-8"))
assert len(ds) == 64, f"expected 64 Mundaka verses, got {len(ds)}"

new_verses = []
for v in ds:
    ch, vn, iast = v["chapter"], v["verse"], v["iast"]
    new_verses.append({
        "id": f"mundaka-up-{ch}-{vn}", "tid": TID, "tn": TN,
        "ch": ch, "cn": SECTION_NAMES[ch], "vn": vn, "complete": True,
        "roman": iast, "dev": v["devanagari"], "iast": iast, "en": v["english"],
        "kw": "", "scripts": {k: v["scripts"][k] for k in ("ml", "ta", "te", "kn")}, "temple": "",
    })

for nv in new_verses:
    for f in ("dev", "iast", "en"):
        assert nv[f], f"{nv['id']} missing {f}"
    for s in ("ml", "ta", "te", "kn"):
        assert nv["scripts"][s], f"{nv['id']} missing script {s}"

text_entry = {"id": TID, "name": TN,
              "desc": ("64 verses in 3 mundakas of 2 khandas each, Atharva Veda. Distinguishes lower "
                       "knowledge (the sciences and scriptures) from the higher knowledge of the "
                       "imperishable Brahman, in the famous image of two birds on one tree. English "
                       "by Max Muller (SBE Vol. 15, 1884, public domain)."),
              "lang": "Sanskrit", "tv": 64, "complete": True}
app["texts"] = [t for t in app["texts"] if t.get("id") != TID]
insert_at = next((i for i, t in enumerate(app["texts"]) if t.get("id") == "katha-upanishad"), -1) + 1
app["texts"].insert(insert_at, text_entry)

app["chapterMeta"][TID] = {str(ch): {"dev": "", "tr": name, "mean": ""} for ch, name in SECTION_NAMES.items()}

app["verses"] = [v for v in app["verses"] if v.get("tid") != TID]
app["verses"].extend(new_verses)

shutil.copy2(APP, APP.with_suffix(".json.bak"))
json.dump(app, open(APP, "w", encoding="utf-8"), ensure_ascii=False)

print("MERGE OK")
print("  texts:", len(app["texts"]), "| mundaka complete:", next(t for t in app["texts"] if t["id"] == TID)["complete"])
print("  total verses:", len(app["verses"]), "| mundaka verses:", sum(1 for v in app["verses"] if v["tid"] == TID))
by_ch = {}
for v in app["verses"]:
    if v["tid"] == TID: by_ch[v["ch"]] = by_ch.get(v["ch"], 0) + 1
print("  verses per section:", by_ch)
