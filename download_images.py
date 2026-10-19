#!/usr/bin/env python3
"""Download every eBay product photo into img_local/ so the site serves them from its own domain.

Why: Firefox Enhanced Tracking Protection (and some ad blockers) block images loaded from i.ebayimg.com.
Run this ONCE on your computer (it needs internet), then rebuild:

    python3 download_images.py
    python3 build.py

Re-run it any time you add products; photos already downloaded are skipped.
"""
import json, re, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "img_local"; OUT.mkdir(exist_ok=True)
urls = {}
def add(u):
    m = re.search(r"/images/g/([^/]+)/", u or "")
    if m: urls[m.group(1)] = f"https://i.ebayimg.com/images/g/{m.group(1)}/s-l500.jpg"
for f in (ROOT / "catalog").glob("*.json"):
    d = json.loads(f.read_text(encoding="utf-8"))
    if f.name == "images.json":
        for v in (d.values() if isinstance(d, dict) else d):
            if isinstance(v, str): urls[v] = f"https://i.ebayimg.com/images/g/{v}/s-l500.jpg"
        continue
    ps = d.get("products", []) if isinstance(d, dict) else d
    for p in ps:
        for i in p.get("images", []): add(i if isinstance(i, str) else i.get("src"))
def get(item):
    pid, u = item; dest = OUT / f"{pid}.jpg"
    if dest.exists() and dest.stat().st_size > 1000: return None
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read()
        if len(data) < 1000: raise ValueError("too small")
        dest.write_bytes(data); return None
    except Exception as e:
        return f"{pid}: {e}"
print(f"{len(urls)} photos to check...")
with ThreadPoolExecutor(8) as ex: bad = [r for r in ex.map(get, urls.items()) if r]
print(f"Done. {len(urls) - len(bad)} ready in img_local/, {len(bad)} failed.")
for b in bad[:20]: print("  failed", b)
print("Now run: python3 build.py")
