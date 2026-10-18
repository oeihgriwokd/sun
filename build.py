#!/usr/bin/env python3
"""Builds one static HTML page per product: python3 build.py
Reads catalog/products.json + template/product.html, writes dist/. Python 3 standard library only.
Stops with a list of problems (and writes nothing) if any product is invalid."""
import collections, hashlib, html, json, re, shutil, sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
PREFIX = {"AUD": "AU $"}
errors = []
ASSET_V = ""  # changes whenever the CSS or JS changes, so browsers never keep stale copies

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

def esc(s): return html.escape(str(s), quote=True)

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026") + "</script>"

def prices_of(p):
    pr = [v["price"] for v in p.get("variations", []) if is_price(v.get("price"))] or ([p["price"]] if is_price(p.get("price")) else [])
    return pr

def price_label(p):
    pr = prices_of(p)
    if not pr: return "Not available"
    s = fmt_price(max(pr), p["currency"])
    return f"Up to {s}" if (p.get("pricePrefix") or min(pr) < max(pr)) else s

def trim(text, n):
    if len(text) <= n: return text
    return text[:n].rsplit(" ", 1)[0].rstrip(" ,|-") + "…"

# ---- categories (matched on the listing title, first match wins; everything else is Linux) ----
CATS = [
    ("sandisk", "SanDisk bootable SD & microSD cards", r"sandisk", "Bootable SD and microSD cards for computers and small boards such as the Raspberry Pi."),
    ("music", "Music USB drives", r"music usb collection", "USB drives loaded with classical music collections."),
    ("bundles", "USB drive bundles", r"bundle|bsd collection", "Bundles that put several operating systems or tools on one USB drive."),
    ("installers", "App and game installer USBs", r"(installer|launcher) usb \|", "USB drives that carry an installer for a popular app or game."),
    ("other", "Other items", r"mazda|keychain", "Other items from the store."),
    ("android", "Android for PC", r"android|bliss|primeos|remixos", "Bootable USB drives for running Android-based systems on a PC."),
    ("retro", "Retro gaming and media centres", r"batocera|retro ?pie|lakka|libreelec|osmc|volumio", "Bootable systems for retro gaming, home theatre and music streaming."),
    ("bsd", "BSD, DOS and other operating systems", r"bsd|freedos|haiku|dragonfly", "Bootable USB drives for BSD, DOS and other alternative operating systems."),
    ("tools", "Disk, rescue and security tools", r"gparted|clonezilla|dban|rescatux|testdisk|memtest|system ?rescue|ultimate boot|nmap|wireshark|shredos|undelete|redo ?rescue|ventoy|bleachbit|glary|mcleaner|wifislax|backbox|ipfire|truenas|proxmox|httrack|linuxcnc|test tones|rescue", "Tools for disk cloning, partitioning, data recovery, network and security work."),
    ("apps", "Free software and creative apps", r"portable|audacity|vlc|gimp|inkscape|kdenlive|shotcut|openshot|blender|lmms|musescore|libreoffice|openoffice|scribus|pencil2d|handbrake|mixxx|losslesscut|kicad|7-zip|winmerge|firefox|eclipse|vscodium|posterazor|gramps|lazpaint|stepmania|zint|ispy|espeak|dvd creater|turbocash|wine|construct classic|rosegarden", "Free and open-source software on a USB drive, for office, design, audio, video and more."),
    ("linux", "Linux distributions", r"", "Bootable USB drives for Linux distributions, from beginner-friendly desktops to rescue and server systems."),
]
CAT = {c[0]: c for c in CATS}

def category_of(p):
    t = p["title"].lower()
    for slug_, _, rx, _ in CATS:
        if rx and re.search(rx, t): return slug_
    return "linux"

DISPLAY = ["linux", "tools", "apps", "sandisk", "installers", "retro", "android", "bsd", "bundles", "music", "other"]
STORE = "https://www.ebay.com.au/str/aussieusbs"
FEATURED = ["800016537860", "800016421272", "800016323704", "800034663198", "800016354792", "800016005122", "800016404515", "800016475643", "800140680095", "800141757027", "800141827441", "800062044539"]

def header():
    nav = "".join(f'<a href="category-{s}.html">{esc(n)}</a>' for s, n in [("linux", "Linux"), ("tools", "Tools"), ("apps", "Software"), ("sandisk", "SD cards"), ("installers", "Installers")])
    return ('<header class="site-header"><div class="site-header__inner"><a class="site-name" href="index.html">Aussie USBs</a>'
            '<form class="site-search" action="shop.html" role="search"><input name="q" type="search" placeholder="Search all products" aria-label="Search all products"><button type="submit">Search</button></form></div>'
            f'<nav class="site-nav" aria-label="Main"><a href="shop.html">All products</a>{nav}<a href="guides.html">Guides</a>'
            f'<a href="{STORE}" target="_blank" rel="noopener noreferrer">eBay store</a></nav></header>')

def footer():
    return ('<footer class="site-footer"><p>Aussie USBs sells on eBay Australia. You complete every purchase on eBay.</p>'
            f'<p><a href="index.html">Home</a> &middot; <a href="guides.html">Guides</a> &middot; <a href="{STORE}" target="_blank" rel="noopener noreferrer">Our eBay store</a></p></footer>')

def page(site, title, desc, name, body, extra="", og_image=""):
    base = (site.get("baseUrl") or "").rstrip("/")
    url = f"{base}/{name}" if base and name != "index.html" else (f"{base}/" if base else "")
    og = (f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="website">'
          f'<meta property="og:site_name" content="{esc(site["name"])}">' + (f'<meta property="og:url" content="{esc(url)}">' if url else "")
          + (f'<meta property="og:image" content="{esc(og_image)}">' if og_image else "") + '<meta name="twitter:card" content="summary">')
    return (f'<!DOCTYPE html>\n<html lang="en-AU">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{esc(title)}</title>\n<meta name="description" content="{esc(desc)}">\n'
            + (f'<link rel="canonical" href="{esc(url)}">\n' if url else "") + og + extra
            + f'\n<link rel="stylesheet" href="assets/product.css?v={ASSET_V}">\n</head>\n<body>\n{header()}\n<main class="product prose">\n{body}\n</main>\n{footer()}\n</body>\n</html>\n')

def cards(items, pages):
    out = []
    for p in items:
        img = f'<img src="{esc(p["images"][0]["src"])}" alt="" width="190" height="190" loading="lazy" decoding="async">' if p["images"] else ""
        out.append(f'<li><a class="card" href="{esc(p["id"])}.html">{img}<strong>{esc(p.get("display") or p["title"])}</strong><span class="card-price">{esc(price_label(p))}</span></a></li>')
    return '<ul class="card-grid">' + "".join(out) + "</ul>"

NOISE = re.compile(r"latest version|australian shipping|aussie shipping|australian|aussie|same day|shipping|high[- ]?speed|fast speed|fast|flash drive|installer recovery fix|installer fix|recovery fix|recovery|beginner easy|beginner|desktop ?& ?laptop|desktop laptop pc|desktop laptop|desktop pc|plug ?& ?play|pc laptop|live install|free|2026|and install guide|and guide|64 bit|windows, ?mac(?:, ?linux)?|windows,mac,linux|\bau\b|\baus\b|bootable usb|\bbootable\b|\bdrive\b|\busb\b|upgrade your computer with linux", re.I)
BOOTS = {"linux", "tools", "bsd", "android", "retro", "bundles", "sandisk"}
SUFFIX = {"linux", "tools", "bsd", "android", "retro"}

def clean_words(title):
    t = NOISE.sub(" ", title.split("|")[0])
    t = re.sub(r"[^A-Za-z0-9.+/&!()' -]", " ", t)
    return [w for w in t.replace("&", " ").split() if w.strip("-()'/")]

def display_name(p, n=7):
    words = clean_words(p["title"])[:n] or p["title"].split()[:6]
    name = " ".join(words).strip(" -")
    cat = category_of(p)
    if cat in SUFFIX and "usb" not in name.lower(): name += " Bootable USB Drive"
    elif cat == "apps" and "usb" not in name.lower(): name += " on USB"
    elif cat == "installers" and "usb" not in name.lower(): name += " USB"
    return name

def make_slug(p):
    words = clean_words(p["title"])[:8]
    s = re.sub(r"[^a-z0-9]+", "-", " ".join(words).lower()).strip("-")
    s = s[:58].rsplit("-", 1)[0] if len(s) > 58 else s
    if category_of(p) in SUFFIX and "usb" not in s: s += "-bootable-usb"
    elif category_of(p) == "installers" and "usb" not in s: s += "-usb"
    return s or "product"

def assign_ids(products, keep):
    used = {p["id"] for p in products if p["id"] in keep}
    for p in products:
        if p["id"] in keep: continue
        s = make_slug(p)
        if s in used: s = f"{s}-{(item_of(p) or '0000')[-4:]}"
        n = 2
        while s in used: s = f"{s}-{n}"; n += 1
        p["id"] = s; used.add(s)

ABOUT = {
    "linux": "{n} is a Linux operating system supplied on a bootable USB drive. Plug it into a computer that can start from USB, restart, and pick the USB drive from the boot menu. Many Linux systems let you try them in live mode before you install anything.",
    "tools": "{n} is a tool you run by starting your computer from the USB drive instead of its own disk. See the eBay listing for exactly what is included.",
    "apps": "{n} is free software supplied on a USB drive. See the eBay listing for exactly what is included and which systems it supports.",
    "sandisk": "{n} is a memory card prepared with a bootable system, for devices that can start from an SD or microSD card, such as the Raspberry Pi. Check that your device supports it before you buy.",
    "installers": "{n} is a USB drive that carries an installer. See the eBay listing for the systems it supports and what is included.",
    "bundles": "{n} puts several systems or tools on one USB drive. See the eBay listing for exactly what is included.",
    "music": "{n} is a USB drive loaded with music, for any car stereo or speaker that plays music from USB.",
    "retro": "{n} is a bootable system for retro gaming or media centres. Plug it into a compatible device, restart, and boot from the USB drive.",
    "android": "{n} lets you run an Android-based system on a PC by starting the computer from the USB drive.",
    "bsd": "{n} is a bootable USB drive for an alternative operating system. Start your computer from the USB drive to try or install it.",
    "other": "See the eBay listing for full details of this item.",
}

def faq_for(p, cat, name, lo, hi, nopt, site):
    q = []
    if cat in BOOTS:
        q.append(("How do I start my computer from this USB drive?", "Plug it in, restart the computer and open the boot menu. The key is often Esc, F2, F10, F12 or Del, and it varies by maker. Choose the USB drive, then follow the on-screen steps. Our guide on how to boot from a USB drive explains it in more detail."))
        q.append(("Will it work on my computer?", "It works on computers that can start from a USB drive or card, which includes many modern PCs. Compatibility depends on your hardware and settings, so check the details on the eBay listing or message the seller on eBay before you buy."))
    if nopt > 1 and lo is not None:
        q.append(("Which option should I choose?", f"This listing has {nopt} options with prices from {fmt_price(lo, p['currency'])} to {fmt_price(hi, p['currency'])}. Pick your option on the eBay listing; the price changes with the option."))
    q.append(("Where do I pay and check out?", f"Checkout and payment happen on eBay Australia. The Buy on eBay button opens the live listing, where you can see the current price, delivery options and return terms for {name}."))
    return q

def render(template, p, site, ctx):
    start = {"price": p.get("price"), "ebayUrl": p.get("ebayUrl")}
    if p.get("variations"):
        ok = [v for v in p["variations"] if v.get("available", True) is not False and is_price(v.get("price"))]
        v = max(ok, key=lambda v: v["price"]) if ok else p["variations"][0]
        start = {"price": v.get("price"), "ebayUrl": v.get("ebayUrl")}
    price = fmt_price(start["price"], p["currency"]) if is_price(start["price"]) else "Not available"
    if p.get("pricePrefix") and is_price(start["price"]): price = f"{p['pricePrefix']} {price}"
    base = (site.get("baseUrl") or "").rstrip("/")
    pr = prices_of(p); lo, hi = (min(pr), max(pr)) if pr else (None, None)
    nopt = len(p.get("variations", []))
    price_text = (f"from {fmt_price(lo, p['currency'])} to {fmt_price(hi, p['currency'])}" if lo != hi else f"for {fmt_price(hi, p['currency'])}") if pr else ""
    cat = CAT[category_of(p)]; name = p["display"]
    about = ABOUT[cat[0]].format(n=name)
    desc = p.get("description") or trim(f"{name}, {price_text}. {about.split('. ')[0]}. Buy on eBay Australia from {site['name']}.", 158)
    page_url = f"{base}/{p['id']}.html" if base else ""
    offer = {"@type": "Offer", "price": f"{hi:.2f}", "priceCurrency": p["currency"], "url": p.get("ebayUrl") or p["variations"][0]["ebayUrl"]} if pr and lo == hi else (
        {"@type": "AggregateOffer", "lowPrice": f"{lo:.2f}", "highPrice": f"{hi:.2f}", "priceCurrency": p["currency"], "offerCount": nopt, "url": p["variations"][0]["ebayUrl"]} if pr else None)
    prod = {"@context": "https://schema.org", "@type": "Product", "name": p["title"], "description": desc}
    if p["images"]: prod["image"] = [i["src"] for i in p["images"]]
    if offer: prod["offers"] = offer
    crumbs = [("Home", f"{base}/" if base else "index.html"), (cat[1], f"{base}/category-{cat[0]}.html" if base else f"category-{cat[0]}.html"), (name, page_url)]
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, **({"item": u} if u else {})} for i, (n, u) in enumerate(crumbs)]}
    faqs = faq_for(p, cat[0], name, lo, hi, nopt, site)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    og = (f'<meta property="og:title" content="{esc(trim(name, 90))}"><meta property="og:description" content="{esc(desc)}"><meta property="og:type" content="product">'
          f'<meta property="og:site_name" content="{esc(site["name"])}"><meta property="og:locale" content="en_AU">' + (f'<meta property="og:url" content="{esc(page_url)}">' if page_url else "")
          + (f'<meta property="og:image" content="{esc(p["images"][0]["src"])}">' if p["images"] else "") + '<meta name="twitter:card" content="summary_large_image">')
    pre = ('<link rel="preconnect" href="https://i.ebayimg.com">' + (f'<link rel="preload" as="image" href="{esc(p["images"][0]["src"])}">' if p["images"] else "")
           + '<meta name="robots" content="index,follow,max-image-preview:large">')
    sections = [f'<section class="details"><h2>About {esc(name)}</h2><p>{esc(about)}</p></section>']
    if cat[0] in BOOTS:
        sections.append('<section class="details"><h2>How it works</h2><ol><li>Plug the drive into your computer and restart it.</li><li>Open the boot menu (often Esc, F2, F10, F12 or Del) and choose the USB drive.</li><li>Follow the on-screen steps to try or install it. <a href="guide-how-to-boot-from-usb.html">Read the full boot guide</a>.</li></ol></section>')
    if p.get("variations"):
        items = []
        for v in p["variations"]:
            label = ", ".join(f"{k}: {x}" for k, x in v["options"].items())
            items.append(f"<li><span>{esc(label)}</span><strong>{esc(fmt_price(v['price'], p['currency'])) if is_price(v.get('price')) else 'Not available'}</strong></li>")
        sections.append(f'<section class="details"><h2>Options and prices</h2><p>{nopt} options available. Choose your option on eBay when you buy.</p><ul class="price-list">{"".join(items)}</ul></section>')
    sections.append('<section class="details"><h2>Frequently asked questions</h2>' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in faqs) + "</section>")
    sections.append(f'<section class="details"><h2>Listing details</h2><p>eBay listing title: {esc(p["title"])}</p>{"<p>Condition: " + esc(p["condition"]) + "</p>" if p.get("condition") else ""}<p>Sold by {esc(site["name"])} on eBay Australia.</p></section>')
    mates = ctx["by_cat"][cat[0]]; i = mates.index(p["id"]); rel = [ctx["by_id"][mates[(i + k) % len(mates)]] for k in range(1, min(9, len(mates)))]
    related = f'<section class="related"><h2>More in {esc(cat[1])}</h2>{cards(rel, ctx)}</section>' if rel else ""
    crumb_html = f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="category-{cat[0]}.html">{esc(cat[1])}</a> &rsaquo; {esc(trim(name, 60))}</nav>'
    template2 = template if p["images"] else re.sub(r"<!--GALLERY-->.*?<!--/GALLERY-->\n?", "", template, flags=re.S)
    p = dict(p, shortName=name)
    data_json = json.dumps(p, ensure_ascii=False).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    short_title = f"{name} | {site['name']}"
    if len(short_title) > 62: short_title = trim(name, 62 - len(site["name"]) - 3) + f" | {site['name']}"
    vals = {
        "PAGE_TITLE": esc(short_title), "DESCRIPTION": esc(desc),
        "CANONICAL": f'<link rel="canonical" href="{esc(page_url)}">' if page_url else "", "HEAD_EXTRA": pre + og + jsonld(prod) + jsonld(bc) + jsonld(faq_ld),
        "HEADER": header(), "FOOTER": footer(), "BREADCRUMB": crumb_html, "SECTIONS": "".join(sections), "RELATED": related,
        "LAYOUT_CLASS": "" if p["images"] else " product-layout--single",
        "FIRST_IMAGE": esc(p["images"][0]["src"]) if p["images"] else "",
        "FIRST_ALT": esc(p["images"][0]["alt"] or f"{name}, image 1 of {len(p['images'])}") if p["images"] else "",
        "TITLE": esc(p["title"]), "CONDITION_HTML": f'<p class="condition">Condition: {esc(p["condition"])}</p>' if p.get("condition") else "",
        "PRICE": esc(price), "EBAY_URL": esc(start["ebayUrl"] or "#"),
        "BUY_NOTE": "Opens the eBay listing in a new tab. Choose your option there to complete your purchase." if nopt else "Opens the eBay listing in a new tab, where you complete your purchase.",
        "DATA_JSON": data_json, "ASSET_V": ASSET_V,
    }
    return re.sub(r"\{\{(\w+)\}\}", lambda m: vals[m.group(1)], template2)

def item_of(p):
    m = re.search(r"/itm/(\d+)", str(p.get("ebayUrl", "")))
    return m.group(1) if m else None

def read_imported(path, curated):
    """catalog/imported.json (made by import_csv.py). Curated entries in products.json win; they only borrow options/prices."""
    if not path.exists(): return []
    imported = json.loads(path.read_text(encoding="utf-8"))
    by_item = {item_of(p): p for p in curated if item_of(p)}
    photos = {}
    if (path.parent / "images.json").exists():  # item number -> eBay picture id (from the Seller Hub pages)
        photos = json.loads((path.parent / "images.json").read_text(encoding="utf-8"))
    extra = []
    for q in imported:
        if item_of(q) in photos and not q.get("images"):
            q["images"] = [f"https://i.ebayimg.com/images/g/{photos[item_of(q)]}/s-l500.jpg"]
        c = by_item.get(item_of(q))
        if c is None: extra.append(q)
        elif q.get("variations") and not c.get("variations"):
            c["variationAttributes"], c["variations"] = q["variationAttributes"], q["variations"]
            c.pop("price", None); c.pop("pricePrefix", None); c.pop("ebayUrl", None)
    return extra


def guides(lk):
    return [
        ("how-to-boot-from-usb", "How to boot a computer from a USB drive",
         "Step-by-step guide to starting a PC from a bootable USB drive: boot menu keys, UEFI and BIOS settings, and what to check before you start.",
         f"""<p>A bootable USB drive lets a computer start from the USB instead of its own disk. It is how you try or install an operating system, or run a rescue tool. These are the usual steps. Exact keys and menus differ between computer makers, so check your computer's manual if something does not match.</p>
<h2>Before you start</h2>
<ul><li>Back up anything important. Installing an operating system can erase a disk.</li><li>Plug the USB drive straight into the computer, not into a hub.</li><li>Keep a laptop on charge.</li></ul>
<h2>Step by step</h2>
<ol><li>Insert the USB drive and restart the computer.</li>
<li>As it starts, press the boot menu key. It is often Esc, F2, F10, F12 or Del, and many computers show a hint on the first screen.</li>
<li>Choose the USB drive in the boot menu. You may see it listed twice, once with a UEFI label. Newer computers usually work best with the UEFI entry.</li>
<li>Wait for the system to load. Many Linux USB drives start in a live mode first, so you can try the system before installing anything.</li></ol>
<h2>If the USB drive does not appear</h2>
<ul><li>Try another USB port, ideally one directly on the computer.</li><li>Look in the BIOS or UEFI settings for a boot order option and move USB up.</li><li>Some computers have Secure Boot turned on, which can block some systems. Whether it matters depends on the operating system, so check that system's documentation before changing it.</li></ul>
<p>Looking for a USB drive to boot from? Start with {lk('800016537860','Ubuntu')}, {lk('800016421272','Linux Mint')} or browse <a href="index.html#browse">all categories</a>. Each one is bought on eBay.</p>"""),
        ("what-is-a-bootable-usb-drive", "What is a bootable USB drive?",
         "A plain-English explanation of bootable USB drives, live USB mode, and what people use them for.",
         f"""<p>A bootable USB drive is a USB flash drive set up so a computer can start from it. Instead of loading the system on the internal disk, the computer loads the system stored on the USB.</p>
<h2>What people use them for</h2>
<ul><li><strong>Trying an operating system.</strong> Many Linux systems have a live mode that runs from the USB without changing the computer's disk.</li>
<li><strong>Installing an operating system.</strong> The USB holds the installer.</li>
<li><strong>Repair and recovery.</strong> Tools such as {lk('800062044539','Clonezilla')} can be started from USB for disk cloning and backups.</li>
<li><strong>Older computers.</strong> A lightweight system can give an older machine a second life.</li></ul>
<h2>What you need</h2>
<p>A computer that can start from USB, a few minutes, and a backup of anything you cannot lose. Our guide on <a href="guide-how-to-boot-from-usb.html">how to boot from a USB drive</a> walks through the steps.</p>"""),
        ("choosing-a-linux-distribution", "Choosing a Linux distribution",
         "How to think about picking a Linux distribution, with links to popular options available as bootable USB drives.",
         f"""<p>Linux comes in many versions, called distributions. They share the same core but differ in looks, tools and how often they update. There is no single best choice, so it helps to know what you want.</p>
<h2>Popular starting points</h2>
<ul><li>{lk('800016537860','Ubuntu')} is widely used and has a large amount of online help.</li>
<li>{lk('800016421272','Linux Mint')} has a traditional desktop layout that many Windows users find familiar.</li>
<li>{lk('800034663198','Zorin OS')} is designed to feel familiar to people coming from Windows or macOS.</li>
<li>{lk('800016323704','Debian')} is known for stability and is the base for many other distributions.</li>
<li>{lk('800016354792','Fedora')} tends to include newer software and is a common choice for developers.</li></ul>
<h2>Things to consider</h2>
<ul><li>How much experience you have. Beginner-friendly distributions are usually easier to set up.</li>
<li>How old your computer is. Some distributions are built to run well on older hardware.</li>
<li>What you will use it for: everyday browsing, gaming, programming or servers.</li></ul>
<p>You can try most of these in live mode before installing. See <a href="guide-how-to-boot-from-usb.html">how to boot from a USB drive</a> to get started.</p>"""),
        ("live-usb-or-install", "Live USB or install: which should you choose?",
         "The difference between running an operating system from a live USB and installing it on your computer.",
         """<p>Many Linux USB drives can do two things: run the system straight from the USB (live mode), or install it onto the computer's disk.</p>
<h2>Live mode</h2>
<ul><li>Lets you try the system without changing the computer's disk.</li><li>Is usually slower than an installed system, because it runs from the USB.</li><li>Does not normally keep your changes unless the USB has been set up for that.</li></ul>
<h2>Installing</h2>
<ul><li>Puts the system on the computer's disk, so it starts faster and keeps your files and settings.</li><li>Can erase or change what is on the disk, so back up first.</li><li>Can sit beside Windows in a dual-boot setup, which needs careful partitioning.</li></ul>
<p>A sensible approach is to try live mode first, then install if you like it. If you are not sure how to start, read <a href="guide-how-to-boot-from-usb.html">how to boot from a USB drive</a>.</p>"""),
    ]

def main():
    catalog = json.loads((ROOT / "catalog" / "products.json").read_text(encoding="utf-8"))
    site, products = catalog.get("site", {"name": "Aussie USBs"}), catalog.get("products", [])
    curated_ids = {p.get("id") for p in products}
    products = products + read_imported(ROOT / "catalog" / "imported.json", products)
    for p in products: p.setdefault("title", "")
    assign_ids(products, curated_ids)
    seen = set()
    for i, p in enumerate(products): validate(p, i, seen)
    if errors:
        print("Build stopped. Fix these problems in catalog/products.json:\n")
        print("\n".join(" - " + e for e in errors)); sys.exit(1)
    template = (ROOT / "template" / "product.html").read_text(encoding="utf-8")
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(); shutil.copytree(ROOT / "assets", DIST / "assets")
    global ASSET_V
    ASSET_V = hashlib.md5(b"".join((ROOT / "assets" / f).read_bytes() for f in ("product.css", "product.js"))).hexdigest()[:8]
    products = [normalise(p) for p in products]
    for p in products: p["display"] = display_name(p)
    dupes = [n for n, c in collections.Counter(p["display"] for p in products).items() if c > 1]
    for p in products:
        if p["display"] in dupes: p["display"] = display_name(p, 12)
    dupes = [n for n, c in collections.Counter(p["display"] for p in products).items() if c > 1]
    for p in products:
        if p["display"] in dupes: p["display"] += f" ({(item_of(p) or '0000')[-4:]})"
    by_id = {p["id"]: p for p in products}
    by_cat = {c[0]: sorted([p["id"] for p in products if category_of(p) == c[0]], key=lambda i: by_id[i]["title"].lower()) for c in CATS}
    ctx = {"by_id": by_id, "by_cat": by_cat}
    base = (site.get("baseUrl") or "").rstrip("/")
    by_item = {item_of(p): p for p in products if item_of(p)}
    names = []
    for p in products:
        (DIST / f"{p['id']}.html").write_text(render(template, p, site, ctx), encoding="utf-8")
    shop_script = "<script>(function(){var i=document.getElementById('q'),items=[].slice.call(document.querySelectorAll('.card-grid li')),n=document.getElementById('count');function f(){var t=i.value.toLowerCase().trim(),c=0;items.forEach(function(li){var ok=li.textContent.toLowerCase().indexOf(t)>-1;li.hidden=!ok;if(ok)c++});n.textContent=c+' of '+items.length+' products'}var m=/[?&]q=([^&]*)/.exec(location.search);if(m){i.value=decodeURIComponent(m[1].replace(/\\+/g,' '))}i.addEventListener('input',f);f()})();</script>"
    allp = sorted(products, key=lambda p: p["title"].lower())
    shop_body = (f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; All products</nav><h1>All products</h1>'
                 f'<p>Search all {len(products)} bootable USB drives, SD cards and installers. Every purchase is completed on eBay.</p>'
                 f'<label class="visually-hidden" for="q">Filter products</label><input id="q" class="shop-filter" type="search" placeholder="Type to filter, e.g. ubuntu, mint, raspberry">'
                 f'<p id="count" class="crumbs" role="status"></p>{cards(allp, ctx)}{shop_script}')
    (DIST / "shop.html").write_text(page(site, f"All products ({len(products)}) | {site['name']}", trim(f"Browse and search all {len(products)} bootable USB drives, SD cards and software installers from {site['name']} on eBay Australia.", 158), "shop.html", shop_body), encoding="utf-8")
    names.append("shop.html")
    # category pages
    for slug_, name, _, intro in CATS:
        items = [by_id[i] for i in by_cat[slug_]]
        if not items: continue
        body = f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; {esc(name)}</nav><h1>{esc(name)}</h1><p>{esc(intro)} {len(items)} listing{"s" if len(items) != 1 else ""}. Every item is bought on eBay Australia.</p>{cards(items, ctx)}'
        title = f"{name} ({len(items)} listings) | {site['name']}"
        extra = jsonld({"@context": "https://schema.org", "@type": "CollectionPage", "name": name, "description": intro})
        (DIST / f"category-{slug_}.html").write_text(page(site, title, trim(f"{intro} Browse {len(items)} listings from {site['name']} on eBay Australia.", 158), f"category-{slug_}.html", body, extra), encoding="utf-8")
        names.append(f"category-{slug_}.html")
    # guides
    def lk(item, text):
        p = by_item.get(item); return f'<a href="{esc(p["id"])}.html">{esc(text)}</a>' if p else esc(text)
    g = guides(lk)
    for gslug, gtitle, gdesc, gbody in g:
        body = f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; <a href="guides.html">Guides</a></nav><h1>{esc(gtitle)}</h1>{gbody}'
        art = jsonld({"@context": "https://schema.org", "@type": "Article", "headline": gtitle, "description": gdesc, "publisher": {"@type": "Organization", "name": site["name"]}})
        (DIST / f"guide-{gslug}.html").write_text(page(site, f"{gtitle} | {site['name']}", gdesc, f"guide-{gslug}.html", body, art), encoding="utf-8")
        names.append(f"guide-{gslug}.html")
    gl = "".join(f'<li><a class="card" href="guide-{s}.html"><strong>{esc(t)}</strong><span>{esc(d)}</span></a></li>' for s, t, d, _ in g)
    (DIST / "guides.html").write_text(page(site, f"Guides: bootable USB drives and Linux | {site['name']}", "Guides on booting from USB, choosing a Linux distribution and live USB mode.", "guides.html", f'<nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> &rsaquo; Guides</nav><h1>Guides</h1><ul class="card-grid">{gl}</ul>'), encoding="utf-8")
    names.append("guides.html")
    # home page
    cat_cards = "".join(f'<li><a class="card" href="category-{s}.html"><strong>{esc(n)}</strong><span>{len(by_cat[s])} listing{"s" if len(by_cat[s]) != 1 else ""}</span></a></li>' for s, n, _, _ in sorted(CATS, key=lambda c: DISPLAY.index(c[0])) if by_cat[s])
    feat = [by_item[i] for i in FEATURED if i in by_item]
    body = (f'<h1>Bootable USB drives and software installers</h1><p>{esc(site["name"])} sells bootable USB drives, SD cards and software installers on eBay Australia, including Ubuntu, Linux Mint, Debian and Zorin OS. '
            f'Browse {len(products)} listings, then complete your purchase on eBay.</p><h2 id="browse">Browse by category</h2><ul class="card-grid">{cat_cards}</ul><p><a href="shop.html">See all {len(products)} products</a></p>'
            f'<h2>Popular picks</h2>{cards(feat, ctx)}<h2>Guides</h2><ul class="card-grid">{gl}</ul>')
    org = jsonld({"@context": "https://schema.org", "@type": "Organization", "name": site["name"], "url": (base + "/") if base else "", "sameAs": [STORE]})
    (DIST / "index.html").write_text(page(site, f"{site['name']} | Bootable USB Drives & Installers: Ubuntu, Linux Mint, Debian", trim(f"Browse {len(products)} bootable USB drives, SD cards and installers, including Ubuntu, Linux Mint, Debian and Zorin OS. Sold by {site['name']} on eBay Australia.", 158), "index.html", body, org), encoding="utf-8")
    if base:
        urls = [base + "/"] + [f"{base}/{n}" for n in names] + [f"{base}/{p['id']}.html" for p in products]
        (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(f"<url><loc>{esc(u)}</loc></url>" for u in urls) + "\n</urlset>\n", encoding="utf-8")
        (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {base}/sitemap.xml\n", encoding="utf-8")
    if site.get("domain"): (DIST / "CNAME").write_text(site["domain"] + "\n", encoding="utf-8")
    (DIST / "404.html").write_text(page(site, f"Page not found | {site['name']}", "This page could not be found.", "404.html", '<h1>Page not found</h1><p>That page does not exist. <a href="index.html">Go to the home page</a>.</p>', '<meta name="robots" content="noindex">'), encoding="utf-8")
    print(f"Built {len(products)} product pages, {len([c for c in by_cat.values() if c])} category pages, {len(g)} guides, a guides index, the home page and a sitemap with {len(urls) if base else 0} URLs into {DIST}")

if __name__ == "__main__":
    main()
