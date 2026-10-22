"""Does every stack the UI can compose resolve all of its parts in the archive, and which archive
files can never be reached? Needs the archive (set VAULT_ARCHIVE or keep it next to vault-configurator).

Run:  python -X utf8 vault-configurator/tests/test_stack_parts.py
Plain asserts, no framework: it fails loudly on the first stack whose parts are missing."""
import collections
import itertools
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import catalog  # noqa: E402

ROOT = os.path.abspath(os.environ.get("VAULT_ARCHIVE") or os.path.dirname(os.path.dirname(HERE)))
# the designer never made these, so the catalog is right to leave them out
KNOWN_MISSING = {"Baseplate_With 1 Handle", "Baseplate_With 2 Handles"}


def every_stack():
    """Every layout × height × option the Stack tab offers, as single-layer stacks (+ roofs and mods on each base)."""
    for depth in (3, 4, 5, 6, 7):
        for layout in catalog.LAYOUTS:
            heights = (1,) if catalog.LAYOUT_FAMILY[layout] == "XL" else (1, 2, 4)
            for h in heights:
                fams = catalog.LAYOUTS[layout]
                for pats in itertools.product(catalog.PATTERNS[h], repeat=len(fams)):
                    for key, interior, rails, ms in itertools.product(("key", "hidden", "none"), ("none", "baseplate", "baseplate1h", "baseplate2h", "grid"), (0, 1), (0, 1)):
                        yield {"depth": depth, "layers": [{"type": "Drawers", "layout": layout, "height": h, "facades": list(pats), "key": key,
                                                           "interior": interior, "rails": rails, "manualSupports": ms, "gridW": 2, "gridD": 2}]}
                for variant, divs, bp in itertools.product(("Flat", "Dividers", "Sealed"), (0, 1), (0, 1)):
                    yield {"depth": depth, "layers": [{"type": "Sustainers", "layout": layout, "height": h, "variant": variant, "dividers": divs, "baseplate": bp}]}
                base = {"type": "Drawers", "layout": layout, "height": h, "facades": [[h] for _ in fams]}
                for roof in ("grid", "table", "bowl", "undertable", "heavyweight"):
                    yield {"depth": depth, "layers": [base], "roof": {"type": roof, "topHandle": True}}
                for bb, pb in itertools.product(("none", "wide", "universal"), ("none", "ussa", "ikea")):
                    yield {"depth": depth, "layers": [base, dict(base)], "mods": {"base": 1, "wheels": 1, "feet": 1, "casters": 1, "backbone": bb,
                                                                                   "pullout": 1, "stationary": 1, "connectors": 1, "pegboard": pb, "wallmount": 1}}


def main():
    assert os.path.isdir(os.path.join(ROOT, "01. DRAWERS")), f"archive not found under {ROOT}"
    idx = catalog.Index(ROOT)
    site = catalog.load_site_data(os.path.join(os.path.dirname(HERE), "site_print_data.json"))
    used, n_stacks, failures = set(), 0, collections.Counter()
    for stack in every_stack():
        n_stacks += 1
        for whole_fits in (True, False):  # split versions of big parts are used when the one-piece file fits no printer
            bom = catalog.Bom(idx, site, lambda rel, ok=whole_fits: ok).build(stack)
            for p in bom["parts"]:
                if p["file"]:
                    used.add(p["file"])
                else:
                    failures[p["name"]] += 1
            for w in bom["warnings"]:
                if "does not exist" in w and not any(k in w for k in KNOWN_MISSING):
                    failures[w] += 1
    bad = {k: v for k, v in failures.items() if not any(k2 in k for k2 in KNOWN_MISSING)}
    assert not bad, f"parts without a file in some stacks: {bad}"
    allf = sorted(rel for _, _, rel in idx.files)
    unused = [f for f in allf if f not in used]
    print(f"{n_stacks} stacks composed, every part resolved; {len(used)}/{len(allf)} archive files reachable")
    by = collections.defaultdict(list)
    for f in unused:
        by[os.path.dirname(f)].append(os.path.basename(f))
    for d in sorted(by):
        print(f"  never used: {d}  ({len(by[d])} files: {', '.join(by[d][:4])}{' …' if len(by[d]) > 4 else ''})")
    # the only files the tool never offers are alternatives of parts it does offer
    for f in unused:
        base = os.path.basename(f)
        assert ("Grid Dividers" in f or "Connector For Split Roof" in base or "Universal\\Facades" in f or "Universal/Facades" in f
                or "Connector for Modules 2F" in base), f"unexpected unused file: {f}"
    print("test_stack_parts ok")


if __name__ == "__main__":
    main()
