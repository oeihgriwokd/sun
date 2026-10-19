import re,glob,json,os,collections
from html.parser import HTMLParser
D="dist/"; files=sorted(glob.glob(D+"*.html")); names={os.path.basename(f) for f in files}
titles=collections.defaultdict(list); descs=collections.defaultdict(list); issues=collections.defaultdict(list)
class P(HTMLParser):
    def __init__(s): super().__init__(); s.l=[];s.ids=set();s.h1=0;s.noalt=0;s.imgs=0;s.stack=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        if a.get("id"): s.ids.add(a["id"])
        if t=="a" and a.get("href"): s.l.append(a["href"])
        if t=="h1": s.h1+=1
        if t=="img":
            s.imgs+=1
            if "alt" not in a: s.noalt+=1
for f in files:
    n=os.path.basename(f); h=open(f,encoding="utf-8").read(); p=P(); p.feed(h)
    t=re.search(r"<title>(.*?)</title>",h,re.S); t=t.group(1) if t else ""
    d=re.search(r'<meta name="description" content="(.*?)"',h); d=d.group(1) if d else ""
    titles[t].append(n); descs[d].append(n)
    if not t: issues["no title"].append(n)
    elif len(t)>65: issues["title>65"].append(n)
    if not d: issues["no desc"].append(n)
    elif len(d)>165: issues["desc>165"].append(n)
    elif len(d)<50: issues["desc<50"].append(n)
    if p.h1!=1: issues[f"h1={p.h1}"].append(n)
    if p.noalt: issues["img no alt"].append(n)
    if n!="404.html" and 'rel="canonical"' not in h: issues["no canonical"].append(n)
    if 'rel="canonical"' in h and n not in("index.html","404.html"):
        c=re.search(r'rel="canonical" href="(.*?)"',h).group(1)
        if not c.endswith("/"+n): issues["canonical mismatch"].append(n)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>',h,re.S):
        try: json.loads(m.group(1))
        except Exception as e: issues["bad jsonld"].append(n)
    for l in set(p.l):
        if l.startswith(("http","mailto","#","javascript")): continue
        tgt=l.split("#")[0].split("?")[0]
        if tgt and tgt not in names and not os.path.exists(D+tgt): issues["broken link"].append(f"{n} -> {l}")
    if h.count('<main')!=1: issues["main count"].append(n)
    if 'lang="en"' not in h: issues["no lang"].append(n)
for t,v in titles.items():
    if len(v)>1: issues["dup title"].append(f"{t[:60]} x{len(v)}: {v[:3]}")
for t,v in descs.items():
    if len(v)>1 and t: issues["dup desc"].append(f"{t[:50]} x{len(v)}")
sm=open(D+"sitemap.xml").read(); 
for u in re.findall(r"<loc>https://linuxonusb.com/?(.*?)</loc>",sm):
    if u and u not in names: issues["sitemap 404"].append(u)
for f in names:
    if f!="404.html" and f"/{f}<" not in sm and f!="index.html": issues["not in sitemap"].append(f)
print(len(files),"pages")
for k,v in issues.items(): print(k,len(v),v[:4])
