/* Site search: instant suggestions with product photos, categories and systems. */
(function () {
  "use strict";
  var form = document.querySelector(".site-search");
  if (!form) return;
  var input = form.querySelector("input");
  var box = document.createElement("div");
  box.className = "suggest"; box.id = "suggest"; box.setAttribute("role", "listbox"); box.setAttribute("aria-label", "Search suggestions");
  form.appendChild(box);
  input.setAttribute("role", "combobox"); input.setAttribute("aria-controls", "suggest"); input.setAttribute("aria-expanded", "false");
  input.setAttribute("aria-autocomplete", "list"); input.setAttribute("autocomplete", "off");
  var data = null, loading = false, active = -1, POP = ["Ubuntu", "Linux Mint", "Zorin OS", "Debian", "Kali Linux", "Raspberry Pi", "Clonezilla", "Windows alternative", "Retro gaming", "Rescue tools"];
  function load(cb) {
    if (data) return cb();
    if (loading) return; loading = true;
    fetch("assets/search.json").then(function (r) { return r.json(); }).then(function (d) { data = d; cb(); }).catch(function () { loading = false; });
  }
  function score(e, ws) {
    var t = e.t.toLowerCase(), k = e.k || "", s = 0;
    for (var i = 0; i < ws.length; i++) {
      var w = ws[i];
      if (t.indexOf(w) === 0) s += 6; else if (t.indexOf(" " + w) > -1) s += 4; else if (t.indexOf(w) > -1) s += 3; else if (k.indexOf(w) > -1) s += 1; else return 0;
    }
    return s;
  }
  function el(tag, cls, txt) { var n = document.createElement(tag); if (cls) n.className = cls; if (txt) n.textContent = txt; return n; }
  function link(href, title, sub, img) {
    var a = el("a"); a.href = href; a.setAttribute("role", "option");
    if (img) { var im = el("img"); im.src = img; im.alt = ""; im.width = 44; im.height = 44; im.loading = "lazy"; a.appendChild(im); }
    var d = el("span"); d.appendChild(document.createTextNode(title));
    if (sub) d.appendChild(el("small", "", sub));
    a.appendChild(d); return a;
  }
  function close() { box.classList.remove("open"); input.setAttribute("aria-expanded", "false"); active = -1; }
  function open() { box.classList.add("open"); input.setAttribute("aria-expanded", "true"); }
  function render() {
    var q = input.value.trim().toLowerCase(); box.textContent = ""; active = -1;
    if (!q) {
      box.appendChild(el("div", "sg-h", "Popular searches"));
      POP.forEach(function (p) { box.appendChild(link("shop.html?q=" + encodeURIComponent(p), p)); });
      return open();
    }
    var ws = q.split(/\s+/);
    var cs = data.c.map(function (e) { return [score(e, ws), e]; }).filter(function (x) { return x[0]; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 3);
    var ps = data.p.map(function (e) { return [score(e, ws), e]; }).filter(function (x) { return x[0]; }).sort(function (a, b) { return b[0] - a[0]; }).slice(0, 7);
    if (cs.length) { box.appendChild(el("div", "sg-h", "Browse")); cs.forEach(function (x) { box.appendChild(link(x[1].u, x[1].t)); }); }
    if (ps.length) { box.appendChild(el("div", "sg-h", "Products")); ps.forEach(function (x) { box.appendChild(link(x[1].i + ".html", x[1].t, x[1].p || "", x[1].m)); }); }
    if (!cs.length && !ps.length) box.appendChild(el("div", "sg-h", "No quick matches. Try fewer words."));
    var all = link("shop.html?q=" + encodeURIComponent(input.value.trim()), "See all results for \u201c" + input.value.trim() + "\u201d"); all.className = "sg-all"; box.appendChild(all);
    open();
  }
  function items() { return box.querySelectorAll("a"); }
  function move(d) {
    var l = items(); if (!l.length) return;
    if (active > -1) l[active].removeAttribute("aria-selected");
    active = (active + d + l.length) % l.length; l[active].setAttribute("aria-selected", "true"); l[active].scrollIntoView({ block: "nearest" });
  }
  input.addEventListener("input", function () { load(render); });
  input.addEventListener("focus", function () { load(render); });
  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); move(1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); move(-1); }
    else if (e.key === "Escape") close();
    else if (e.key === "Enter" && active > -1) { e.preventDefault(); items()[active].click(); }
  });
  document.addEventListener("click", function (e) { if (!form.contains(e.target)) close(); });
  /* shop page: apply ?q= from the header search */
  var qs = new URLSearchParams(location.search).get("q"), f = document.getElementById("q");
  if (qs && f) { f.value = qs; f.dispatchEvent(new Event("input", { bubbles: true })); }
})();
