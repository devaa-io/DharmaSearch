#!/usr/bin/env python3
"""Merge the completed Mandukya Upanishad dataset into app_data.json (idempotent)."""
import json, shutil, pathlib

BASE = pathlib.Path("/mnt/c/Users/Devan Narayanan/Downloads/DharmaSearch/dharmasearch-handoff")
APP = BASE / "app_data.json"
DATA = BASE / "data" / "mandukya-upanishad.json"
TID = "mandukya-upanishad"
TN = "Mandukya Upanishad"

app = json.load(open(APP, encoding="utf-8"))
ds = json.load(open(DATA, encoding="utf-8"))
assert len(ds) == 12, f"expected 12 Mandukya verses, got {len(ds)}"

new_verses = []
for v in ds:
    vn, iast = v["verse"], v["iast"]
    new_verses.append({
        "id": f"mandukya-up-{vn}", "tid": TID, "tn": TN,
        "ch": 1, "cn": "Mandukya Upanishad", "vn": vn, "complete": True,
        "roman": iast, "dev": v["devanagari"], "iast": iast, "en": v["english"],
        "kw": "", "scripts": {k: v["scripts"][k] for k in ("ml", "ta", "te", "kn")}, "temple": "",
    })

for nv in new_verses:
    for f in ("dev", "iast", "en"):
        assert nv[f], f"{nv['id']} missing {f}"
    for s in ("ml", "ta", "te", "kn"):
        assert nv["scripts"][s], f"{nv['id']} missing script {s}"

text_entry = {"id": TID, "name": TN,
              "desc": ("12 verses, Atharva Veda - the shortest principal Upanishad. Analyses the "
                       "syllable Om into its matras (a/u/m/silence), mapped onto the four states "
                       "of consciousness: waking, dream, deep sleep, and the fourth (turiya) beyond "
                       "them. English by Robert Ernest Hume (Thirteen Principal Upanishads, Oxford "
                       "University Press, 1921, public domain)."),
              "lang": "Sanskrit", "tv": 12, "complete": True}
app["texts"] = [t for t in app["texts"] if t.get("id") != TID]
insert_at = next((i for i, t in enumerate(app["texts"]) if t.get("id") == "isha-upanishad"), -1) + 1
app["texts"].insert(insert_at, text_entry)

app["chapterMeta"][TID] = {"1": {"dev": "", "tr": TN, "mean": ""}}

app["verses"] = [v for v in app["verses"] if v.get("tid") != TID]
app["verses"].extend(new_verses)

shutil.copy2(APP, APP.with_suffix(".json.bak"))
json.dump(app, open(APP, "w", encoding="utf-8"), ensure_ascii=False)

print("MERGE OK")
print("  texts:", len(app["texts"]), "| mandukya complete:", next(t for t in app["texts"] if t["id"] == TID)["complete"])
print("  total verses:", len(app["verses"]), "| mandukya verses:", sum(1 for v in app["verses"] if v["tid"] == TID))
