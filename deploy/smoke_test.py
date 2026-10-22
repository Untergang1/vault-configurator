"""End-to-end smoke test of a running VAULT configurator, local or on the NAS.

    python -X utf8 deploy/smoke_test.py http://<nas>:8765

Checks, against the real server and the real archive it mounts:
  1. /api/meta answers and the archive is indexed (733 STL files for the full VAULT archive)
  2. a demo stack resolves to parts that all have a file
  3. the plan places every piece that fits a printer (placed + unplaceable == pieces)
  4. an export runs to completion, writes one 3MF per printer used, and reading each file back the way
     the slicer does finds every piece entirely on its plate
Stdlib only, so it runs anywhere Python does. Exits non-zero on the first failure."""
import json
import sys
import time
import urllib.parse
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765").rstrip("/")
DEMO = {"name": "smoke", "depth": 4,
        "layers": [{"type": "Drawers", "layout": "S", "height": 2, "facades": [[1, 1]], "interior": "baseplate", "key": "key", "labels": True},
                   {"type": "Sustainers", "layout": "S", "height": 1}],
        "roof": {"type": "grid", "topHandle": True}, "mods": {"backbone": "none", "pegboard": "none"}}


def call(path, body=None, timeout=600):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Content-Type": "application/json"} if body is not None else {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())


def main():
    t0 = time.time()
    meta = call("/api/meta")
    assert meta["files"] > 0, f"no STL files indexed: is the archive mounted? ({BASE})"
    print(f"1 ok  {meta['files']} STL files indexed{'' if meta['files'] == 733 else '  (expected 733 for the full archive)'}")
    for _ in range(40):  # the pictures are generated in the background at start-up
        a = call("/api/meta").get("assets") or {}
        if a.get("help", 0) >= 26 and a.get("sheets", 0) >= 14:
            break
        time.sleep(3)
    assert a.get("help", 0) >= 26 and a.get("sheets", 0) >= 14, f"pictures missing: {a}"
    with urllib.request.urlopen(BASE + "/thumb/" + urllib.parse.quote("01. DRAWERS\\07. Universal\\Key Cap.stl"), timeout=120) as r:  # fixed path, Windows separators
        assert r.status == 200 and r.headers.get("Content-Type") == "image/png"
    print(f"1b ok {a['help']} help pages, {a['sheets']} render sheets, part pictures by fixed path")
    settings = meta["defaults"]
    bom = call("/api/bom", {"stack": DEMO, "settings": settings, "overrides": {}})
    missing = [p["name"] for p in bom["parts"] if not p.get("file")]
    assert bom["parts"] and not missing, f"parts without a file: {missing}"
    print(f"2 ok  {len(bom['parts'])} part lines, {sum(int(p['qty']) for p in bom['parts'])} pieces, every part has a file")
    plan = call("/api/plan", {"stack": DEMO, "settings": settings, "overrides": {}})["plan"]
    left = sum(u.get("qty", 1) for u in plan["unplaceable"])
    assert plan["placed"] + left == plan["pieces"], f"pieces unaccounted for: {plan['pieces']} pieces, {plan['placed']} placed, {left} unplaceable"
    print(f"3 ok  {plan['placed']}/{plan['pieces']} pieces on {len(plan['plates'])} plates, {left} reported unplaceable")
    assert call("/api/export", {"stack": DEMO, "settings": settings, "overrides": {}}).get("started"), "export did not start"
    while True:
        time.sleep(3)
        st = call("/api/export_status")
        if st.get("error"):
            raise AssertionError(f"export failed: {st['error']}")
        if not st.get("running") and st.get("result"):
            break
    files = st["result"]["files"]
    assert files and all(f["plates"] > 0 for f in files), files
    outside = [(f["file"], o) for f in files for o in f.get("outside", [])]
    assert not outside, f"pieces not entirely on their plate (read back from the 3MF): {outside[:5]}"
    assert sum(f["items"] for f in files) == plan["placed"], "the files hold a different number of pieces than the plan placed"
    names = [f"{f['file'].replace(chr(92), '/').split('/')[-1]} ({f['plates']} plates)" for f in files]
    print(f"4 ok  export wrote {', '.join(names)}; every piece read back on its plate")
    print(f"smoke test passed against {BASE} in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
