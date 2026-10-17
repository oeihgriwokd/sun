# Aussie USBs product pages

One template + one catalogue file = one static HTML page per product.

```
catalog/products.json   <- the ONLY place product data lives
template/product.html   <- page layout (shared)
assets/product.css      <- shared styling
assets/product.js       <- shared gallery / variations / buy-button logic
build.py                <- generator (Python 3, no installs; included with Ubuntu)
dist/                   <- finished site: upload this folder (pages + assets/)
```

Build: `python3 build.py` (checks every product first, writes nothing if anything is wrong).
Each page is dist/<id>.html. Open a page directly in a browser to test; no server needed.

## Add product number 301
1. Copy any block inside "products" in catalog/products.json and change `id` (lowercase, hyphens), `title`, `price`, `currency`, `condition`, `ebayUrl`, `images`.
2. Run `python3 build.py`. Any missing or invalid field is listed by product.
3. Upload `dist/`. The new page is dist/<id>.html.

Other edits (price, image, eBay URL) are the same: change the value, rebuild, upload.
Images can be plain URLs or `{ "src": "...", "alt": "..." }` for custom alt text. Any number of images works, including one.
Optional fields: `description` (meta description only), `condition`.
`site.baseUrl` (e.g. "https://example.com") adds canonical links; leave "" until the real address is known.

## Change styling for all products
Edit assets/product.css (colours and sizes are variables at the top) or template/product.html, then rebuild and upload `dist/`.

## Variations
Add to a product (and remove its top-level `price` and `ebayUrl`):
```
"variationAttributes": [ { "name": "Storage", "options": ["A", "B"] } ],
"variations": [
  { "options": { "Storage": "A" }, "price": 0.00, "ebayUrl": "<eBay URL for option A>" },
  { "options": { "Storage": "B" }, "available": false }
]
```
Use several attributes for several selectors; list one `variations` row per valid combination.
A combination with no row, or `"available": false`, shows "Not available" and the button is disabled.
The first available row is selected on load.
Real data needed per variation: its exact option names as on eBay, its real price, and its eBay URL.
On eBay, select the option on the listing and copy the address bar: variation links usually carry a `?var=` number. Check each link opens the right option.

## Limits
- Prices are typed into the catalogue. Nothing syncs with eBay. Live prices/stock would need the eBay API plus a server, which static hosting cannot do.
- Build checks cover structure and URLs, not whether a listing or image still exists on eBay.
