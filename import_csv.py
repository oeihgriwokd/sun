#!/usr/bin/env python3
"""Turns an eBay Seller Hub "active listings" CSV into catalog/imported.json.
Usage: python3 import_csv.py path/to/report.csv
Only public listing facts are kept (item number, title, condition, prices, option names)."""
import csv, json, re, sys
from pathlib import Path

def slug(t): return re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")

def price(row):
    for k in ("Start price", "Current price"):
        try: return float(row.get(k, "").replace(",", ""))
        except ValueError: pass
    return None

def main(src):
    rows = list(csv.DictReader(open(src, encoding="utf-8-sig", newline="")))
    items, order, warn = {}, [], []
    for r in rows:
        n = r["Item number"].strip()
        if n not in items: items[n] = []; order.append(n)
        items[n].append(r)
    out = []
    for n in order:
        rs = items[n]; first = rs[0]; title = first["Title"].strip()
        p = {"id": f"{slug(title)[:50].strip('-')}-{n[-6:]}", "title": title, "currency": first["Currency"] or "AUD",
             "ebayUrl": f"https://www.ebay.com.au/itm/{n}"}
        cond = first.get("Condition", "").strip()
        if cond: p["condition"] = cond[0].upper() + cond[1:].lower() if cond.lower() == "brand new" else cond
        details = [(r["Variation details"].strip(), r) for r in rs if r["Variation details"].strip()]
        if not details:
            pr = price(first)
            if pr is None: warn.append(f"{n}: no price, skipped"); continue
            p["price"] = pr
        else:
            def parse(d):
                return {k.strip(): [x.strip() for x in v.split(";") if x.strip()] for k, _, v in (part.partition("=") for part in d.split("|"))}
            parent = parse(max((d for d, _ in details), key=lambda d: d.count(";")))
            names = list(parent)
            variations = []
            for d, r in details:
                c = parse(d)
                if list(c) != names or any(len(v) != 1 or v[0] not in parent[k] for k, v in c.items()): continue
                pr = price(r)
                if pr is None: warn.append(f"{n}: an option has no price, skipped"); continue
                variations.append({"options": {k: v[0] for k, v in c.items()}, "price": pr, "ebayUrl": p["ebayUrl"]})
            if not variations:
                pr = price(first)
                if pr is None: warn.append(f"{n}: no price, skipped"); continue
                p["price"] = pr; warn.append(f"{n}: options unreadable, used a single price")
            else:
                p["variationAttributes"] = [{"name": k, "options": [o for o in parent[k] if any(v["options"][k] == o for v in variations)]} for k in names]
                p["variations"] = variations
        out.append(p)
    Path(__file__).resolve().parent.joinpath("catalog", "imported.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"{len(out)} listings written to catalog/imported.json ({sum(1 for p in out if 'variations' in p)} with options)")
    for w in warn: print("  note:", w)

if __name__ == "__main__":
    if len(sys.argv) != 2: sys.exit("Usage: python3 import_csv.py path/to/report.csv")
    main(sys.argv[1])
