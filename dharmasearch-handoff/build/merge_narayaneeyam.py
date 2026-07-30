#!/usr/bin/env python3
"""Merge the completed Narayaneeyam dataset into app_data.json."""
import json, shutil, pathlib

BASE = pathlib.Path(__file__).resolve().parents[1]
APP = BASE / "app_data.json"
DATA = BASE / "data" / "narayaneeyam.json"
TID = "narayaneeyam"
TN = "Narayaneeyam"

app = json.load(open(APP, encoding="utf-8"))
ds = json.load(open(DATA, encoding="utf-8"))
assert len(ds) == 1033, f"expected 1033 Narayaneeyam verses, got {len(ds)}"

new_verses = []
for v in ds:
    ch, vn, iast = v["chapter"], v["verse"], v["iast"]
    new_verses.append({
        "id": f"nym-{ch}-{vn}", "tid": TID, "tn": TN,
        "ch": ch, "cn": f"Dasakam {ch}", "vn": vn, "complete": True,
        "roman": iast, "dev": v["devanagari"], "iast": iast, "en": v["english"],
        "kw": "", "scripts": {k: v["scripts"][k] for k in ("ml", "ta", "te", "kn")}, "temple": "",
    })

for nv in new_verses:
    for f in ("dev", "iast", "en"):
        assert nv[f], f"{nv['id']} missing {f}"
    for s in ("ml", "ta", "te", "kn"):
        assert nv["scripts"][s], f"{nv['id']} missing script {s}"

text_entry = {
    "id": TID, "name": TN,
    "desc": (
        "Melpathur Narayana Bhattatiri's 100-canto devotional condensation of "
        "the Bhagavata Purana, in praise of Krishna at Guruvayoor - 1033 "
        "verses. Devanagari from sanskritdocuments.org; English by "
        "P. R. Ramachander."
    ),
    "lang": "Sanskrit", "tv": 1033, "complete": True,
}
app["texts"] = [t for t in app["texts"] if t.get("id") != TID]
insert_at = next((i for i, t in enumerate(app["texts"]) if t.get("id") == "hanuman-chalisa"), -1) + 1
app["texts"].insert(insert_at, text_entry)

app["chapterMeta"][TID] = {
    str(ch): {"dev": "", "tr": f"Dasakam {ch}", "mean": ""} for ch in range(1, 101)
}

app["verses"] = [v for v in app["verses"] if v.get("tid") != TID]
app["verses"].extend(new_verses)

shutil.copy2(APP, APP.with_suffix(".json.bak"))
json.dump(app, open(APP, "w", encoding="utf-8"), ensure_ascii=False)

print("MERGE OK")
print("  texts:", len(app["texts"]), "| narayaneeyam complete:", next(t for t in app["texts"] if t["id"] == TID)["complete"])
print("  total verses:", len(app["verses"]), "| narayaneeyam verses:", sum(1 for v in app["verses"] if v["tid"] == TID))
