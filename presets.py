"""Read presets from the installed slicers (Bambu Studio, Anycubic Slicer Next, OrcaSlicer) and
build a 3MF `project_settings.config` from them.

A preset JSON stores only the keys it changes and `inherits` its parent; the chain ends in a
system preset whose `compatible_printers` names the printer and nozzle ("Bambu Lab H2C 0.4 nozzle").
System presets also `include` template presets (Bambu keeps every machine G-code in one); those
apply after the parent chain and before the preset's own keys.
A project config is the flattened machine + process presets plus every filament preset's vectors
concatenated in slot order (that is how Bambu Studio writes its own project files).
"""
import glob
import json
import os
import re
import sys


def config_root():
    """Where the slicers keep their settings: %APPDATA% on Windows (also how Docker points at a mounted
    folder), ~/Library/Application Support on macOS, $XDG_CONFIG_HOME or ~/.config on Linux."""
    if os.environ.get("APPDATA"):
        return os.environ["APPDATA"]
    if sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support")
    return os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")


APPDATA = config_root()
SLICERS = {
    "bambu": {"label": "Bambu Studio", "dir": os.path.join(APPDATA, "BambuStudio")},
    "anycubic": {"label": "Anycubic Slicer Next", "dir": os.path.join(APPDATA, "AnycubicSlicerNext")},
    "orca": {"label": "OrcaSlicer", "dir": os.path.join(APPDATA, "OrcaSlicer")},
}
KINDS = ("process", "filament", "machine")
# bookkeeping keys that are not print settings
META = {"name", "inherits", "from", "type", "version", "setting_id", "instantiation", "description", "compatible_printers",
        "compatible_printers_condition", "print_settings_id", "is_custom_defined", "updated_time", "filament_settings_id",
        "printer_settings_id", "base_id", "filament_id", "include"}
# project-level keys we do not copy per object
SKIP = META | {"print_extruder_id", "print_extruder_variant", "printer_model", "printer_variant"}

_cache = {}


def load_all(slicer, kind="process"):
    """name -> preset dict (with _user flag and _file) for every preset of one kind of one slicer."""
    d = SLICERS[slicer]["dir"]
    stamp = tuple(sorted((p, os.path.getmtime(p)) for p in glob.glob(os.path.join(d, "user", "*", kind, "*.json"))))
    key = (slicer, kind)
    if key in _cache and _cache[key][0] == stamp:
        return _cache[key][1]
    out = {}
    for user, pattern in ((False, os.path.join(d, "system", "*", kind, "*.json")), (True, os.path.join(d, "user", "*", kind, "*.json"))):
        for p in glob.glob(pattern):
            try:
                with open(p, encoding="utf-8") as f:
                    j = json.load(f)
            except (OSError, ValueError):
                continue
            if not j.get("name"):
                continue
            j["_user"], j["_file"] = user, p
            out[j["name"]] = j
    _cache[key] = (stamp, out)
    return out


def chain(name, all_presets):
    seen, cur = [], name
    while cur and cur in all_presets and cur not in seen:
        seen.append(cur)
        cur = all_presets[cur].get("inherits")
    return [all_presets[n] for n in seen]


def flatten(name, all_presets, _seen=()):
    """All keys of a preset: parent chain, then included templates, then its own (each part flattened the same way)."""
    if not name or name not in all_presets or name in _seen:
        return {}
    p, seen = all_presets[name], (*_seen, name)
    merged = flatten(p.get("inherits"), all_presets, seen)
    inc = p.get("include") or []
    for t in [inc] if isinstance(inc, str) else inc:
        merged.update(flatten(t, all_presets, seen))
    merged.update({k: v for k, v in p.items() if not k.startswith("_")})
    merged.pop("include", None)
    return merged


def compatible(name, all_presets):
    for p in chain(name, all_presets):
        c = p.get("compatible_printers")
        if c:
            return c if isinstance(c, list) else [c]
    return []


def nozzle_of(printers):
    for s in printers:
        m = re.search(r"(\d+(?:\.\d+)?)\s*nozzle", s)
        if m:
            return m.group(1)
    return ""


def catalog(slicer, profile="", kind="process"):
    """Instantiable presets of one kind, optionally only those compatible with a printer profile
    (substring match on compatible_printers or, for machines, on the preset name)."""
    allp = load_all(slicer, kind)
    rows = []
    for name, p in allp.items():
        if str(p.get("instantiation", "true")).lower() == "false":
            continue
        comp = compatible(name, allp) if kind != "machine" else [name]
        if profile and not any(profile.lower() in c.lower() for c in comp):
            continue
        row = {"name": name, "user": p["_user"], "nozzle": nozzle_of(comp), "printers": comp, "inherits": p.get("inherits", ""),
               "nkeys": len([k for k in p if not k.startswith("_") and k not in SKIP])}
        if kind == "filament":
            fl = flatten(name, allp)
            row["material"] = (fl.get("filament_type") or [""])[0]
            row["vendor"] = (fl.get("filament_vendor") or [""])[0]
        rows.append(row)
    rows.sort(key=lambda r: (not r["user"], r["nozzle"], r["name"]))
    return rows


def overrides(slicer, preset, base, all_presets=None):
    """Per-object settings: keys where `preset` differs from `base` (both flattened), as strings."""
    allp = all_presets or load_all(slicer, "process")
    if not preset or preset == base or preset not in allp:
        return {}
    a, b = flatten(preset, allp), flatten(base, allp) if base in allp else {}
    out = {}
    for k, v in a.items():
        if k in SKIP or k.startswith("_"):
            continue
        if b.get(k) != v:
            out[k] = ",".join(map(str, v)) if isinstance(v, list) else str(v)
    return out


NOZZLE_MAP = {"left": "1", "right": "2"}  # Bambu extruder 1 reaches the plate's left part, 2 (the master) the right


def project_config(slicer, machine, process, filaments, colours, nozzle_side=None):
    """Full project_settings.config dict: machine + process flattened, filament vectors concatenated
    per slot (variant-expanded keys get `filament_self_index` like Bambu Studio writes).
    nozzle_side "left"/"right" pins every filament to that nozzle of a dual-nozzle printer."""
    M = flatten(machine, load_all(slicer, "machine"))
    P = flatten(process, load_all(slicer, "process"))
    fil_all = load_all(slicer, "filament")
    Fs = [flatten(f, fil_all) for f in filaments]
    if not M or not P or any(not F for F in Fs):
        missing = [n for n, d in [(machine, M), (process, P)] + list(zip(filaments, Fs)) if not d]
        raise ValueError("preset not found: " + ", ".join(missing))
    cfg = {}
    for d in (M, P):
        cfg.update({k: v for k, v in d.items() if k not in META})
    fkeys = {k for F in Fs for k, v in F.items() if isinstance(v, list) and k not in META}
    for k in sorted(fkeys):
        vals = []
        for F in Fs:
            v = F.get(k, Fs[0].get(k))
            vals.extend(v if isinstance(v, list) else [v])
        cfg[k] = vals
    cfg["filament_self_index"] = [str(i + 1) for i, F in enumerate(Fs) for _ in range(len(F.get("filament_extruder_variant") or [1]))]
    cfg["filament_colour"] = list(colours)
    cfg["filament_settings_id"] = list(filaments)
    cfg["print_settings_id"] = process
    cfg["printer_settings_id"] = machine
    cfg["filament_ids"] = [(F.get("filament_id") or F.get("setting_id") or "") for F in Fs]
    cfg["default_filament_profile"] = M.get("default_filament_profile") or [filaments[0]]
    n = len(filaments)
    cfg.update({"name": "project_settings", "from": "project", "version": vendor_version(slicer),
                "filament_map": [NOZZLE_MAP.get(nozzle_side, "1")] * n, "filament_map_mode": "Manual" if nozzle_side in NOZZLE_MAP else "Auto For Flush", "nozzle_volume_type": ["Standard"] * len(M.get("nozzle_diameter") or [1]),
                "different_settings_to_system": [""] * (n + 2), "curr_bed_type": "Textured PEI Plate",
                "flush_volumes_vector": ["140"] * (2 * n), "flush_volumes_matrix": ["0" if i == j else "140" for i in range(n) for j in range(n)]})
    return cfg


def vendor_version(slicer):
    """Version string of the slicer's bundled vendor profiles (what the slicer itself stamps into project files)."""
    root = SLICERS[slicer]["dir"]
    for f in glob.glob(os.path.join(root, "system", "*.json")):
        try:
            with open(f, encoding="utf-8") as fh:
                v = json.load(fh).get("version")
            if v:
                return str(v)
        except (OSError, ValueError):
            pass
    return "02.08.00.06"


def default_filament(slicer, profile, nozzle, material, prefer_user=True):
    rows = [r for r in catalog(slicer, profile, "filament") if (not nozzle or r["nozzle"] in (nozzle, ""))]
    m = material.lower()
    mat = [r for r in rows if m in (r.get("material") or "").lower() or m in r["name"].lower()]
    # exact material first (PETG before PETG-CF), then a name that says the material (TPU95A before PEBA), then user presets
    pick = sorted(mat or rows, key=lambda r: ((r.get("material") or "").lower() != m, m not in r["name"].lower(), prefer_user and not r["user"], r["name"]))
    return pick[0]["name"] if pick else ""


if __name__ == "__main__":
    for s in SLICERS:
        for kind in KINDS:
            rows = catalog(s, kind=kind)
            print(f"{s}/{kind}: {len(rows)} presets, {sum(r['user'] for r in rows)} user")
    allb = load_all("bambu")
    user = [n for n, p in allb.items() if p["_user"]]
    if user:
        o = overrides("bambu", user[0], allb[user[0]].get("inherits"), allb)
        assert o and all(isinstance(v, str) for v in o.values())
        assert overrides("bambu", user[0], user[0], allb) == {}
    m = catalog("bambu", "Bambu Lab H2C", "machine")
    print("H2C machines:", [r["name"] for r in m][:6])
    f1 = default_filament("bambu", "Bambu Lab H2C", "0.4", "PETG")
    f2 = default_filament("bambu", "Bambu Lab H2C", "0.4", "TPU")
    print("default filaments:", f1, "|", f2)
    cfg = project_config("bambu", "Bambu Lab H2C 0.4 nozzle", "0.20mm Standard @BBL H2C", [f1, f1, f2], ["#AAAAAA", "#333333", "#111111"])
    n = len(cfg["filament_settings_id"])
    assert cfg["printable_height"] and len(cfg["filament_type"]) == n and len(cfg["filament_colour"]) == n and len(cfg["nozzle_diameter"]) == 2
    assert cfg["filament_self_index"][:1] == ["1"] and len(cfg["filament_self_index"]) == len(cfg["filament_extruder_variant"])
    right = project_config("bambu", "Bambu Lab H2C 0.4 nozzle", "0.20mm Standard @BBL H2C", [f1, f2], ["#AAAAAA", "#111111"], "right")
    assert right["filament_map"] == ["2", "2"] and right["filament_map_mode"] == "Manual" and cfg["filament_map_mode"] == "Auto For Flush"
    print("project keys:", len(cfg), "| filament_type", cfg["filament_type"], "| self_index", cfg["filament_self_index"])
    k = default_filament("anycubic", "Anycubic Kobra X", "0.4", "PETG")
    cfgk = project_config("anycubic", "Anycubic Kobra X 0.4 nozzle", "0.20mm Standard @Anycubic Kobra X 0.4 nozzle", [k, k], ["#AAAAAA", "#333333"])
    print("kobra project keys:", len(cfgk), "| filaments", cfgk["filament_settings_id"], "| printable_area", cfgk.get("printable_area"))
    print("presets.py self-check ok")
