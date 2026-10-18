# Launch checklist for linuxonusb.com
1. Upload the contents of `dist/` (it already has CNAME, robots.txt, sitemap.xml, favicon). Point the domain's DNS at your host.
2. Google Search Console: add the domain, then Sitemaps > submit `https://linuxonusb.com/sitemap.xml`.
3. Bing Webmaster Tools: add the site (import from Search Console) and submit the same sitemap.
4. In Search Console use URL Inspection > Request indexing for the home page and your top 10 products and guides.
5. Add a new guide: copy a block in `guides_extra.py`, run `python3 build.py`, upload `dist/`. Sitemap updates itself.
