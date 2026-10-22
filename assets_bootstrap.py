"""Pictures the UI needs but the repository must not ship: manual pages come out of the PDFs in the
owner's archive, the composer render sheets are fetched from ussadesign.com. Runs once at start-up and
fills `assets/`; anything that fails is just missing (the UI copes), and is retried next start."""
import glob
import io
import os
import re
import time
import urllib.error
import urllib.request

# help topic -> (manual number, 1-based page) in the archive PDFs (01_Instructions Manual, 02_Drawer Assembly, 04_Modifications, 05_Mounting Instructions)
HELP_PAGES = {
    "two-types": ("01", 5), "sizes": ("01", 6), "variants": ("01", 7), "stacking": ("01", 8), "interiors": ("01", 9), "roofs": ("01", 10),
    "drawer-parts": ("01", 11), "sustainer-parts": ("01", 12), "mods-overview": ("01", 13), "facade-files": ("01", 16), "manual-supports": ("01", 20),
    "key-lock": ("02", 1), "manual-supports-remove": ("02", 3), "geared-rails": ("02", 4), "labels": ("02", 5), "facade-assembly": ("02", 6),
    "backbone": ("04", 1), "wheels": ("04", 3), "wheels-feet": ("04", 6), "connectors": ("04", 9), "stationary-handle": ("04", 12),
    "pullout-handle": ("04", 14), "pegboard": ("04", 15), "casters": ("04", 17), "wall-mount": ("05", 1), "under-table": ("05", 10),
}
SHEETS = ["facade-only-s1", "facade-only-s2", "facade-only-s4", "facade-only-m1", "facade-only-m2", "facade-only-m4", "facade-only-l1",
          "facade-only-l2", "facade-only-l4", "facade-only-xl1", "sustainer-sheets-s", "sustainer-sheets-m", "sustainer-sheets-l", "sustainer-sheets-xl"]
SITE = "https://www.ussadesign.com"
PAGE = SITE + "/pages/vault?view=vault-stack"
STATUS = {"help": 0, "sheets": 0, "errors": []}  # shown in /api/meta so a missing picture has a visible reason


def count(assets_dir):
    STATUS["help"] = len([t for t in HELP_PAGES if os.path.exists(os.path.join(assets_dir, "help", t + ".jpg"))])
    STATUS["sheets"] = len([s for s in SHEETS if os.path.exists(os.path.join(assets_dir, s + ".png"))])
    return STATUS


def help_pages(archive, out_dir, log=print):
    """Extract the manual pages listed in HELP_PAGES from the owner's PDFs (each page is one JPEG)."""
    todo = {k: v for k, v in HELP_PAGES.items() if not os.path.exists(os.path.join(out_dir, k + ".jpg"))}
    if not todo:
        return
    try:
        from pypdf import PdfReader
    except ImportError:
        STATUS["errors"].append("pypdf is not installed: no manual pages for the help")
        log("assets: " + STATUS["errors"][-1])
        return
    os.makedirs(out_dir, exist_ok=True)
    pdfs = {os.path.basename(p)[:2]: p for p in glob.glob(os.path.join(archive, "*.pdf"))}
    if not pdfs:
        STATUS["errors"].append(f"no PDF manuals found in the archive folder ({archive})")
    readers = {}
    for topic, (num, page) in todo.items():
        src = pdfs.get(num)
        if not src:
            continue
        try:
            reader = readers.setdefault(src, PdfReader(src))
            img = reader.pages[page - 1].images[0]  # needs Pillow
            with open(os.path.join(out_dir, topic + ".jpg"), "wb") as f:
                f.write(img.data)
        except Exception as e:  # a page without an image, a locked PDF, Pillow missing: say so
            msg = f"help picture {topic} ({os.path.basename(src)} p.{page}): {type(e).__name__}: {e}"
            STATUS["errors"].append(msg)
            log("assets: " + msg)
    log(f"assets: manual pages extracted for {len(todo)} help topics")


def render_sheets(out_dir, log=print):
    """Download the composer render sheets ussadesign.com serves to everyone's browser."""
    todo = [s for s in SHEETS if not os.path.exists(os.path.join(out_dir, s + ".png"))]
    if not todo:
        return
    os.makedirs(out_dir, exist_ok=True)
    def get(url, t, tries=4):
        for i in range(tries):
            try:
                return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (vault-configurator)"}), timeout=t).read()
            except urllib.error.HTTPError as e:  # 429: the site asks us to slow down, so wait as told and retry
                if e.code != 429 or i == tries - 1:
                    raise
                wait = e.headers.get("Retry-After", "")
                time.sleep(min(int(wait) if wait.isdigit() else 30 * (i + 1), 120))
    try:
        html = get(PAGE, 20).decode("utf-8", "replace")
    except Exception as e:
        STATUS["errors"].append(f"cannot reach {SITE} ({type(e).__name__}: {e}); the drawing shows plain boxes")
        log("assets: " + STATUS["errors"][-1])
        return
    found = {m.group(1): m.group(0).replace("\\/", "/") for m in re.finditer(r"(?:https?:)?(?:\\?/){2}www\.ussadesign\.com(?:\\?/)[^\"' ]*?vault-composer-images-([a-z0-9-]+)\.png[^\"' ]*", html)}
    for s in todo:
        url = found.get(s)
        if not url:
            STATUS["errors"].append(f"render sheet {s} not found on {PAGE}")
            continue
        if url.startswith("//"):
            url = "https:" + url
        try:
            data = get(url, 30)
            with open(os.path.join(out_dir, s + ".png"), "wb") as f:
                f.write(data)
        except Exception as e:
            STATUS["errors"].append(f"render sheet {s}: {type(e).__name__}: {e}")
            log("assets: " + STATUS["errors"][-1])
    log(f"assets: {len(todo)} render sheets fetched from ussadesign.com")


def bootstrap(archive, assets_dir, log=print):
    STATUS["errors"] = []
    for step in (lambda: help_pages(archive, os.path.join(assets_dir, "help"), log), lambda: render_sheets(assets_dir, log)):
        try:
            step()
        except Exception as e:  # never take the server down over pictures
            STATUS["errors"].append(f"{type(e).__name__}: {e}")
            log("assets: " + STATUS["errors"][-1])
    return count(assets_dir)


if __name__ == "__main__":
    import sys
    import tempfile
    tmp = tempfile.mkdtemp()
    bootstrap(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__))), tmp)
    got = sorted(os.listdir(tmp)), sorted(os.listdir(os.path.join(tmp, "help"))) if os.path.isdir(os.path.join(tmp, "help")) else []
    print(tmp, len(got[0]), "sheets,", len(got[1]), "help pages")
