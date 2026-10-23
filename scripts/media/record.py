"""Short MP4 clips of the interface for posts (Reddit, the landing page), driven like a user would.

    python -X utf8 scripts/media/record.py [http://127.0.0.1:8765] [clip ...]

Needs playwright + chromium, ffmpeg on PATH and a running server with the archive. Writes
docs/media/<clip>.mp4 plus tour.mp4, all clips joined (shown on the landing page). Frames come from Chrome's
screencast as JPEG (Playwright's own video is too blurry for text); a drawn cursor, click ripples and a
caption bar make the clips readable without sound."""
import base64
import os
import shutil
import subprocess
import sys
import tempfile

from playwright.sync_api import sync_playwright

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shoot import DEMO, settled  # noqa: E402  same demo stack as the screenshots

APP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(APP, "docs", "media")
URL = next((a for a in sys.argv[1:] if a.startswith("http")), "http://127.0.0.1:8765")
VIEW, SCALE = {"width": 1280, "height": 720}, 1.5  # 1920 x 1080 frames, text big enough for a phone
MAX_HOLD = 2.5  # seconds: no frame stays longer, so waiting on the server never shows as dead air

OVERLAY = """addEventListener('DOMContentLoaded', () => { if (window.__rec) return; window.__rec = 1;
  const css = document.createElement('style'); css.textContent = `
   #rc{position:fixed;width:22px;height:22px;margin:-11px 0 0 -11px;border-radius:50%;background:rgba(255,255,255,.85);
       border:2px solid #222;box-shadow:0 1px 6px rgba(0,0,0,.5);pointer-events:none;z-index:99999;left:-50px;top:-50px}
   .rr{position:fixed;width:16px;height:16px;margin:-8px 0 0 -8px;border-radius:50%;border:3px solid #f59e0b;pointer-events:none;
       z-index:99998;animation:rr .6s ease-out forwards}
   @keyframes rr{to{transform:scale(3.5);opacity:0}}
   #rcap{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);background:rgba(15,15,18,.88);color:#fff;
       font:600 22px/1.3 system-ui,sans-serif;padding:12px 24px;border-radius:12px;pointer-events:none;z-index:99997;
       box-shadow:0 4px 20px rgba(0,0,0,.4);transition:opacity .3s;opacity:0;white-space:nowrap}`;
  document.head.append(css);
  const c = document.createElement('div'); c.id = 'rc'; document.body.append(c);
  const cap = document.createElement('div'); cap.id = 'rcap'; document.body.append(cap);
  addEventListener('mousemove', e => { c.style.left = e.clientX + 'px'; c.style.top = e.clientY + 'px'; }, true);
  addEventListener('mousedown', e => { const r = document.createElement('div'); r.className = 'rr';
    r.style.left = e.clientX + 'px'; r.style.top = e.clientY + 'px'; document.body.append(r); setTimeout(() => r.remove(), 700); }, true);
  window.caption = t => { cap.textContent = t || ''; cap.style.opacity = t ? 1 : 0; };
})"""


class Recorder:
    """Chrome screencast frames -> ffmpeg concat list with each frame's real duration."""

    def __init__(self, page, name):
        self.page, self.name, self.frames = page, name, []
        self.dir = tempfile.mkdtemp(prefix="vault-frames-")  # local disk: synced folders (Google Drive) drop writes
        self.cdp = page.context.new_cdp_session(page)
        self.cdp.on("Page.screencastFrame", self.frame)
        self.resume()

    def resume(self):
        self.cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 92, "maxWidth": 1920, "maxHeight": 1080})

    def pause(self):  # long waits (export, BOM) collapse to MAX_HOLD in the video
        self.cdp.send("Page.stopScreencast")

    def frame(self, p):
        path = os.path.join(self.dir, f"{len(self.frames):05d}.jpg")
        with open(path, "wb") as f:
            f.write(base64.b64decode(p["data"]))
        self.frames.append((p["metadata"]["timestamp"], path))
        self.cdp.send("Page.screencastFrameAck", {"sessionId": p["sessionId"]})

    def finish(self):
        self.page.wait_for_timeout(1200)
        self.cdp.send("Page.stopScreencast")
        lst = os.path.join(self.dir, "list.txt")
        with open(lst, "w") as f:
            for (t, path), nxt in zip(self.frames, self.frames[1:] + [(self.frames[-1][0] + 1.0, None)]):
                f.write(f"file '{path.replace(os.sep, '/')}'\nduration {min(max(nxt[0] - t, 0.001), MAX_HOLD):.4f}\n")
            f.write(f"file '{self.frames[-1][1].replace(os.sep, '/')}'\n")  # concat needs the last file twice
        mp4 = os.path.join(OUT, self.name + ".mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-fps_mode", "cfr", "-r", "30",
                        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
                        "-c:v", "libx264", "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", mp4], check=True)
        shutil.rmtree(self.dir)
        print("wrote", mp4, f"({len(self.frames)} frames)")
        return mp4


def say(page, text, ms=0):
    page.evaluate("t => caption(t)", text)
    if ms:
        page.wait_for_timeout(ms)


def go(page, target, ms=700):
    """Glide the cursor to an element (selector or locator) without clicking."""
    loc = page.locator(target).first if isinstance(target, str) else target
    loc.scroll_into_view_if_needed()
    b = loc.bounding_box()
    page.mouse.move(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2, steps=28)
    page.wait_for_timeout(ms)
    return loc


def click(page, target, ms=900):
    go(page, target, 250)
    page.mouse.down()
    page.mouse.up()
    page.wait_for_timeout(ms)


def pick(page, select, value, ms=1400):
    """Point at a <select> and choose a value (native dropdowns don't show in screencasts)."""
    loc = go(page, select, 350)
    page.mouse.down()
    page.mouse.up()
    loc.select_option(value)
    page.wait_for_timeout(ms)


def busy_done(page, timeout=240000):
    page.wait_for_function("typeof bom !== 'undefined' && bom && bom.parts && bom.parts.length > 0", timeout=timeout)
    settled(page)


def scroll(page, dy, steps=12, ms=60):
    for _ in range(steps):
        page.mouse.wheel(0, dy / steps)
        page.wait_for_timeout(ms)


def layer(page, i_from_top, help_key):
    return page.locator("#layers .layer").nth(i_from_top).locator(f"[data-help={help_key}] select")


def clip_stack(page, rec):
    say(page, "Compose your VAULT stack", 1800)
    click(page, "#addLayer", 1500)
    say(page, "Add layers: drawers or sustainers, any width and height")
    pick(page, layer(page, 0, "type"), "Sustainers")
    pick(page, layer(page, 0, "height"), "1")
    click(page, "#addLayer", 1500)
    pick(page, layer(page, 0, "width"), "SS", 1800)
    say(page, "The drawing follows every change, to scale")
    go(page, "#schematic", 1800)
    pick(page, "#roofType", "grid", 1800)
    say(page, "Click any option for help from the manuals")
    click(page, page.locator("#layers .layer").nth(0).locator("[data-help=interior]"), 400)
    go(page, "#helpPanel", 2600)
    say(page, "")


def clip_parts(page, rec):
    click(page, "[data-tab=parts]", 1200)
    busy_done(page)
    say(page, "Every part your stack needs, with filament and print time", 2200)
    go(page, "#parts", 400)
    scroll(page, 900, 18, 90)
    page.wait_for_timeout(1200)
    scroll(page, -900, 10, 50)
    say(page, "Click a part to see it in 3D")
    click(page, page.locator("#parts .thumb").nth(1), 4000)  # the latch: small enough to orbit smoothly in headless Chrome
    say(page, "Drag to turn it around")
    canvas = page.locator("#viewerCanvas").bounding_box()
    cx, cy = canvas["x"] + canvas["width"] / 2, canvas["y"] + canvas["height"] / 2
    page.mouse.move(cx - 150, cy, steps=15)
    page.mouse.down()
    page.mouse.move(cx + 180, cy - 60, steps=45)
    page.mouse.move(cx - 60, cy + 40, steps=35)
    page.mouse.up()
    page.wait_for_timeout(1200)
    click(page, "#viewerClose", 800)
    say(page, "")


def clip_export(page, rec):
    click(page, "[data-tab=plates]", 1200)
    say(page, "Your printers, filaments and colours, set once", 2000)
    go(page, "#roles", 300)
    scroll(page, 500, 10, 80)
    page.wait_for_timeout(1500)
    say(page, "Preview the plates: one colour per plate, packed tight")
    click(page, "#planBtn", 400)
    page.wait_for_function("document.querySelectorAll('#plates .plate').length > 0", timeout=240000)
    settled(page)
    go(page, "#plates", 1500)
    scroll(page, 700, 14, 90)
    page.wait_for_timeout(1500)
    say(page, "Export one ready-to-print 3MF per printer")
    click(page, "#exportBtn", 4000)  # a few seconds of the progress bar, then skip to the end
    rec.pause()
    page.wait_for_function("/done in|Error|bad/.test(document.querySelector('#exportStatus').textContent)", timeout=600000)
    rec.resume()
    go(page, "#exportStatus", 400)
    say(page, "Every piece checked on its plate. Opens in Bambu Studio, OrcaSlicer, Anycubic Slicer Next", 4000)
    say(page, "")


CLIPS = {"stack": clip_stack, "parts": clip_parts, "export": clip_export}


def main():
    os.makedirs(OUT, exist_ok=True)
    wanted = [a for a in sys.argv[1:] if a in CLIPS] or list(CLIPS)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        prep = browser.new_context(viewport=VIEW)  # demo stack minus the layers the stack clip adds on camera
        page = prep.new_page()
        page.goto(URL)
        page.wait_for_function("typeof state !== 'undefined' && state && typeof META !== 'undefined' && META")
        start = {**DEMO, "layers": DEMO["layers"][:1], "roof": {"type": "none", "topHandle": True}}
        page.evaluate("(demo) => { state.stack = {...state.stack, ...demo}; state.overrides = {}; save(); }", start)
        storage = prep.storage_state()
        prep.close()
        for name in wanted:
            ctx = browser.new_context(viewport=VIEW, device_scale_factor=SCALE, storage_state=storage)
            ctx.add_init_script(OVERLAY)
            page = ctx.new_page()
            page.goto(URL)
            busy_done(page)
            if name != "stack":  # later clips start from the finished demo stack
                page.evaluate("(demo) => { state.stack = {...state.stack, ...demo}; changed(true); }", DEMO)
                busy_done(page)
            page.evaluate("showTab('stack'); window.scrollTo(0, 0)")
            page.wait_for_timeout(5000)  # render sheets in the drawing give no load event
            page.mouse.move(VIEW["width"] / 2, VIEW["height"] / 2)
            rec = Recorder(page, name)
            CLIPS[name](page, rec)
            rec.finish()
            ctx.close()
        browser.close()
    made = [m for m in (os.path.join(OUT, n + ".mp4") for n in CLIPS) if os.path.exists(m)]  # re-recording one clip keeps the tour whole
    if len(made) > 1:
        lst = os.path.join(OUT, "tour.txt")
        with open(lst, "w") as f:
            f.writelines(f"file '{m.replace(os.sep, '/')}'\n" for m in made)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", "-movflags", "+faststart",
                        os.path.join(OUT, "tour.mp4")], check=True)
        os.remove(lst)
        print("wrote", os.path.join(OUT, "tour.mp4"))


if __name__ == "__main__":
    main()
