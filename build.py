#!/usr/bin/env python3
"""Builds one static HTML page per product: python3 build.py
Reads catalog/products.json + template/product.html, writes dist/. Python 3 standard library only.
Stops with a list of problems (and writes nothing) if any product is invalid."""
import html, json, re, shutil, sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
PREFIX = {"AUD": "AU $"}
errors = []

def fmt_price(amount, currency):
    return f"{PREFIX.get(currency, currency + ' ')}{amount:.2f}"

def is_https(u):
    return isinstance(u, str) and urlparse(u).scheme == "https" and bool(urlparse(u).hostname)

def is_ebay(u):
    return is_https(u) and re.search(r"(^|\.)ebay\.(com|com\.au)$", urlparse(u).hostname) is not None

def is_price(n):
    return isinstance(n, (int, float)) and not isinstance(n, bool) and n > 0

def validate(p, index, seen):
    t = f"product #{index + 1} ({p.get('id', 'no id')})"
    def bad(msg): errors.append(f"{t}: {msg}")
    pid = p.get("id")
    if not isinstance(pid, str) or not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", pid):
        bad("'id' must be lowercase letters, numbers and hyphens, e.g. ubuntu-linux-usb")
    elif pid in seen:
        bad("duplicate 'id'")
    seen.add(pid)
    if not isinstance(p.get("title"), str) or not p["title"].strip(): bad("missing 'title'")
    if not re.fullmatch(r"[A-Z]{3}", str(p.get("currency", ""))): bad("'currency' must be a 3-letter code such as AUD")
    imgs = p.get("images", [])
    if not isinstance(imgs, list):
        bad("'images' must be a list")
    else:
        for i, img in enumerate(imgs):
            src = img.get("src") if isinstance(img, dict) else img
            if not is_https(src): bad(f"image {i + 1} must be an https URL")
    variations, attrs = p.get("variations") or [], p.get("variationAttributes") or []
    if variations:
        names = [a.get("name") for a in attrs]
        if not attrs or not all(isinstance(a.get("name"), str) and a.get("options") for a in attrs):
            bad("variations need 'variationAttributes', each with a 'name' and 'options'")
        else:
            combos = set()
            for n, v in enumerate(variations):
                o = v.get("options", {})
                if sorted(o) != sorted(names) or any(o[k] not in next(a["options"] for a in attrs if a["name"] == k) for k in o):
                    bad(f"variation {n + 1}: 'options' must give one listed value for each of {names}")
                    continue
                key = tuple(o[k] for k in names)
                if key in combos: bad(f"variation {n + 1}: duplicate combination {key}")
                combos.add(key)
                if v.get("available", True) is not False:
                    if not is_price(v.get("price")): bad(f"variation {n + 1}: needs a numeric 'price' (or \"available\": false)")
                    if not is_ebay(v.get("ebayUrl")): bad(f"variation {n + 1}: 'ebayUrl' must be an https eBay URL")
    else:
        if not is_price(p.get("price")): bad("'price' must be a number above 0")
        if not is_ebay(p.get("ebayUrl")): bad("'ebayUrl' must be an https eBay URL")

def normalise(p):
    p = dict(p)
    p["images"] = [{"src": i, "alt": ""} if isinstance(i, str) else {"src": i["src"], "alt": i.get("alt", "")} for i in p.get("images", [])]
    return p

def render(template, p, site):
    esc = lambda s: html.escape(str(s), quote=True)
    start = {"price": p.get("price"), "ebayUrl": p.get("ebayUrl")}
    if p.get("variations"):
        ok = [v for v in p["variations"] if v.get("available", True) is not False and is_price(v.get("price"))]
        v = max(ok, key=lambda v: v["price"]) if ok else p["variations"][0]
        start = {"price": v.get("price"), "ebayUrl": v.get("ebayUrl")}
    price = fmt_price(start["price"], p["currency"]) if is_price(start["price"]) else "Not available"
    if p.get("pricePrefix") and is_price(start["price"]):  # optional wording such as "Up to"
        price = f"{p['pricePrefix']} {price}"
    desc = p.get("description") or f"{p['title']}. Sold by {site['name']} on eBay."
    base = (site.get("baseUrl") or "").rstrip("/")
    data_json = json.dumps(p, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    vals = {
        "PAGE_TITLE": esc(f"{p['title']} | {site['name']}"),
        "DESCRIPTION": esc(desc),
        "CANONICAL": f'<link rel="canonical" href="{esc(base + "/" + p["id"] + ".html")}">' if base else "",
        "FIRST_IMAGE": esc(p["images"][0]["src"]) if p["images"] else "",
        "FIRST_ALT": esc(p["images"][0]["alt"] or f"{p['title']}, image 1 of {len(p['images'])}") if p["images"] else "",
        "TITLE": esc(p["title"]),
        "CONDITION_HTML": f'<p class="condition">Condition: {esc(p["condition"])}</p>' if p.get("condition") else "",
        "PRICE": esc(price),
        "EBAY_URL": esc(start["ebayUrl"] or "#"),
        "BUY_NOTE": "Opens the eBay listing in a new tab. Choose your option there to complete your purchase." if p.get("variations") else "Opens the eBay listing in a new tab, where you complete your purchase.",
        "DATA_JSON": data_json,
    }
    if not p["images"]:  # no photos yet: leave the gallery out of the page
        template = re.sub(r"<!--GALLERY-->.*?<!--/GALLERY-->\n?", "", template, flags=re.S)
    return re.sub(r"\{\{(\w+)\}\}", lambda m: vals[m.group(1)], template)

def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def item_of(p):
    m = re.search(r"/itm/(\d+)", str(p.get("ebayUrl", "")))
    return m.group(1) if m else None

def read_imported(path, curated):
    """catalog/imported.json (made by import_csv.py). Curated entries in products.json win; they only borrow options/prices."""
    if not path.exists(): return []
    imported = json.loads(path.read_text(encoding="utf-8"))
    by_item = {item_of(p): p for p in curated if item_of(p)}
    extra = []
    for q in imported:
        c = by_item.get(item_of(q))
        if c is None: extra.append(q)
        elif q.get("variations") and not c.get("variations"):
            c["variationAttributes"], c["variations"] = q["variationAttributes"], q["variations"]
            c.pop("price", None); c.pop("pricePrefix", None); c.pop("ebayUrl", None)
    return extra

def write_extras(products, site):
    esc = lambda s: html.escape(str(s), quote=True)
    base = (site.get("baseUrl") or "").rstrip("/")
    rows = []
    for p in sorted(products, key=lambda p: p["title"].lower()):
        prices = [v["price"] for v in p.get("variations", []) if is_price(v.get("price"))] or ([p["price"]] if is_price(p.get("price")) else [])
        pr = fmt_price(max(prices), p["currency"]) if prices else ""
        if pr and (p.get("pricePrefix") or (len(prices) > 1 and min(prices) < max(prices))): pr = f"Up to {pr}"
        rows.append(f'<li><a href="{esc(p["id"])}.html"><span>{esc(p["title"])}</span><span class="catalog-price">{esc(pr)}</span></a></li>')
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(site['name'])} | Bootable USB drives and installers</title>
<meta name="description" content="Bootable USB drives, installers and tools from {esc(site['name'])}. Each item is bought on eBay.">
{f'<link rel="canonical" href="{esc(base)}/">' if base else ''}
<link rel="stylesheet" href="assets/product.css">
</head>
<body>
<main class="product">
<h1>{esc(site['name'])}</h1>
<ul class="catalog-list">
{chr(10).join(rows)}
</ul>
</main>
</body>
</html>
"""
    (DIST / "index.html").write_text(page, encoding="utf-8")
    if base:
        urls = [base + "/"] + [f"{base}/{p['id']}.html" for p in products]
        (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"<url><loc>{esc(u)}</loc></url>" for u in urls) + "\n</urlset>\n", encoding="utf-8")
        (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")

def main():
    catalog = json.loads((ROOT / "catalog" / "products.json").read_text(encoding="utf-8"))
    site, products = catalog.get("site", {"name": "Aussie USBs"}), catalog.get("products", [])
    products = products + read_imported(ROOT / "catalog" / "imported.json", products)
    seen = set()
    for i, p in enumerate(products): validate(p, i, seen)
    if errors:
        print("Build stopped. Fix these problems in catalog/products.json:\n")
        print("\n".join(" - " + e for e in errors))
        sys.exit(1)
    template = (ROOT / "template" / "product.html").read_text(encoding="utf-8")
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir()
    shutil.copytree(ROOT / "assets", DIST / "assets")
    for p in products:
        p = normalise(p)
        (DIST / f"{p['id']}.html").write_text(render(template, p, site), encoding="utf-8")
    write_extras([normalise(p) for p in products], site)
    print(f"Built {len(products)} page(s) plus index, sitemap and robots into {DIST}")

if __name__ == "__main__":
    main()
