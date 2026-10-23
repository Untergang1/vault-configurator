"""Screenshots for the README and the landing page, taken from the running tool with a demo stack.

    python -X utf8 scripts/media/shoot.py [http://127.0.0.1:8765]

Needs `pip install playwright` + `playwright install chromium`, a running server with the archive, and
writes docs/media/{stack,help,parts,plates,colours,export,viewer}.jpg. Re-run after UI changes so the
pictures never lie about the version people download (same idea as lamina's scripts/media)."""
import json
import os
import sys
import time

from playwright.sync_api import sync_playwright

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765"
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "docs", "media")
SCALE = 1.5  # sharp enough to read on a phone when the pictures are shared in posts
DEMO = {  # an L5 cart: drawers, two-bay drawers, a sustainer, grid roof, base + wheels + feet, wide backbone, wall mounts
    "name": "demo-cart", "depth": 5,
    "layers": [{"type": "Drawers", "layout": "L", "height": 2, "facades": [[1, 1]], "interior": "baseplate", "key": "key", "labels": True, "rails": True},
               {"type": "Sustainers", "layout": "L", "height": 1, "variant": "Dividers", "divW": 1, "divD": 2},
               {"type": "Drawers", "layout": "SS", "height": 2, "facades": [[2], [1, 1]], "interior": "none", "key": "hidden", "labels": True}],
    "roof": {"type": "grid", "topHandle": True},
    "mods": {"base": True, "wheels": True, "feet": True, "backbone": "wide", "pullout": True, "wallmount": False, "pegboard": "none"},
}


def settled(page, timeout=120000):
    """Every visible <img> finished loading (thumbnails render on first request, ~1 s each); a broken
    picture counts as finished, and a timeout only costs that one screenshot its missing pictures."""
    try:
        page.wait_for_function("[...document.images].every(i => !i.src || i.complete || !i.getBoundingClientRect().height)", timeout=timeout)
    except Exception as e:  # playwright TimeoutError
        print("warning: pictures still loading:", page.evaluate("[...document.images].filter(i => i.src && !i.complete && i.getBoundingClientRect().height).map(i => i.src).slice(0, 5)"))


def shot(page, name, clip=None, full=False):
    settled(page)
    page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(OUT, name + ".jpg"), type="jpeg", quality=82, clip=clip, full_page=full)
    print("wrote", name)


def main():
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1500, "height": 950}, device_scale_factor=SCALE)
        page.goto(URL)
        page.wait_for_function("typeof state !== 'undefined' && state && typeof META !== 'undefined' && META")  # `let` globals: not on window
        page.evaluate("""(demo) => { state.stack = {...state.stack, ...demo}; state.overrides = {}; save(); location.reload(); }""", DEMO)
        page.wait_for_function("typeof bom !== 'undefined' && bom && bom.parts && bom.parts.length > 0", timeout=240000)
        page.evaluate("showTab('stack'); window.scrollTo(0, 0)")
        page.wait_for_timeout(6000)  # the SVG <image> render sheets give no load event
        shot(page, "stack")
        page.evaluate("document.querySelectorAll('#layers .layer')[2].querySelector('[data-help=key]').click()")
        time.sleep(3)
        page.evaluate("document.querySelector('#helpPanel').scrollIntoView()")
        shot(page, "help", clip=None)
        page.evaluate("showTab('parts'); window.scrollTo(0, 0)")
        time.sleep(3)
        shot(page, "parts")
        page.evaluate("document.querySelector('#parts .thumb').click()")
        time.sleep(12)  # three.js + a big STL
        shot(page, "viewer")
        page.evaluate("closeViewer()")
        page.evaluate("showTab('plates'); window.scrollTo(0, 0)")
        time.sleep(2)
        shot(page, "plates")
        page.evaluate("document.querySelector('#roles').scrollIntoView()")
        time.sleep(1)
        shot(page, "colours")
        page.evaluate("(async () => { const r = await api('/api/plan', {stack: state.stack, settings: state.settings, overrides: state.overrides}); renderPlan(r.plan); document.querySelector('#plates').scrollIntoView(); })()")
        page.wait_for_function("document.querySelectorAll('#plates .plate').length > 0", timeout=240000)
        time.sleep(1)
        shot(page, "export")
        browser.close()


if __name__ == "__main__":
    main()
