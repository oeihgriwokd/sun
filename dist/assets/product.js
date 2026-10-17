/* Shared behaviour for every product page. Product data comes from the
   <script id="product-data"> block that build.py writes into each page. */
(function () {
  "use strict";

  var data;
  try { data = JSON.parse(document.getElementById("product-data").textContent); }
  catch (e) { return; } /* page still shows its server-rendered title, price and Buy link */

  var $ = function (id) { return document.getElementById(id); };
  var PREFIX = { AUD: "AU $" };

  function formatPrice(amount, currency) {
    return (PREFIX[currency] || currency + " ") + amount.toFixed(2);
  }
  function isEbayUrl(value) {
    try {
      var u = new URL(value);
      return u.protocol === "https:" && /(^|\.)ebay\.(com|com\.au)$/.test(u.hostname);
    } catch (e) { return false; }
  }
  function announce(message) { $("status").textContent = message; }

  /* ---------- Gallery ---------- */
  var images = (data.images || []).filter(function (img) { return img && /^https:\/\//.test(img.src); });
  var total = images.length;
  var current = 0, loadToken = 0, thumbButtons = [];
  var main = $("mainImage"), thumbs = $("thumbnails"), counter = $("galleryCounter"), errorEl = $("imageError");
  var lightbox = $("lightbox"), lightboxImage = $("lightboxImage");

  function altFor(i) { return images[i].alt || data.title + ", image " + (i + 1) + " of " + total; }

  function showImage(index, silent) {
    current = (index + total) % total;
    var token = ++loadToken, item = images[current];
    main.classList.add("is-loading");
    errorEl.hidden = true;
    var probe = new Image();
    probe.onload = function () {
      if (token !== loadToken) { return; }
      main.hidden = false; main.src = item.src; main.alt = altFor(current);
      main.classList.remove("is-loading");
    };
    probe.onerror = function () {
      if (token !== loadToken) { return; }
      main.hidden = true; errorEl.hidden = false;
      main.classList.remove("is-loading");
    };
    probe.src = item.src;

    thumbButtons.forEach(function (b, i) { b.setAttribute("aria-current", i === current ? "true" : "false"); });
    var b = thumbButtons[current], bar = thumbs.getBoundingClientRect(), r = b.getBoundingClientRect();
    if (r.left < bar.left) { thumbs.scrollLeft += r.left - bar.left; }
    else if (r.right > bar.right) { thumbs.scrollLeft += r.right - bar.right; }

    counter.textContent = (current + 1) + " / " + total;
    if (!silent) { announce("Image " + (current + 1) + " of " + total); }
  }

  if (total === 0) {
    $("gallery").hidden = true;
  } else {
    images.forEach(function (item, i) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "thumbnail-button";
      b.setAttribute("aria-label", "Show image " + (i + 1) + " of " + total);
      b.setAttribute("aria-current", i === 0 ? "true" : "false");
      var t = document.createElement("img");
      t.src = item.src; t.alt = ""; t.width = 64; t.height = 64; t.decoding = "async";
      if (i > 0) { t.loading = "lazy"; }
      b.appendChild(t);
      b.addEventListener("click", function () { showImage(i); });
      thumbs.appendChild(b); thumbButtons.push(b);
    });
    counter.textContent = "1 / " + total;

    if (total > 1) {
      thumbs.hidden = false; counter.hidden = false;
      $("prevImage").hidden = false; $("nextImage").hidden = false;
      $("prevImage").addEventListener("click", function () { showImage(current - 1); });
      $("nextImage").addEventListener("click", function () { showImage(current + 1); });
      $("gallery").addEventListener("keydown", function (e) {
        if (e.key === "ArrowLeft") { showImage(current - 1); }
        else if (e.key === "ArrowRight") { showImage(current + 1); }
      });
      var startX = null, wrap = document.querySelector(".main-image-wrap");
      wrap.addEventListener("touchstart", function (e) { startX = e.changedTouches[0].clientX; }, { passive: true });
      wrap.addEventListener("touchend", function (e) {
        if (startX === null) { return; }
        var dx = e.changedTouches[0].clientX - startX; startX = null;
        if (Math.abs(dx) > 50) { showImage(dx < 0 ? current + 1 : current - 1); }
      }, { passive: true });
    }

    /* Full-size viewer: native <dialog> traps focus, closes on Esc and returns focus to the opener */
    var openBtn = $("openViewer");
    function fillViewer() { lightboxImage.src = images[current].src; lightboxImage.alt = altFor(current); }
    if (typeof lightbox.showModal === "function") {
      openBtn.addEventListener("click", function () { fillViewer(); lightbox.showModal(); });
      $("closeViewer").addEventListener("click", function () { lightbox.close(); });
      lightbox.addEventListener("click", function (e) { if (e.target === lightbox) { lightbox.close(); } });
      lightbox.addEventListener("keydown", function (e) {
        if (total > 1 && (e.key === "ArrowLeft" || e.key === "ArrowRight")) {
          showImage(current + (e.key === "ArrowRight" ? 1 : -1)); fillViewer();
        }
      });
    } else {
      openBtn.disabled = true; openBtn.style.cursor = "default";
    }
  }

  /* ---------- Price, variations and Buy button ---------- */
  var priceEl = $("productPrice"), buyEl = $("buyButton");

  function enableBuy(url) {
    buyEl.href = url; buyEl.classList.remove("is-disabled");
    buyEl.removeAttribute("aria-disabled"); buyEl.removeAttribute("role");
  }
  function disableBuy() {
    buyEl.removeAttribute("href"); buyEl.classList.add("is-disabled");
    buyEl.setAttribute("aria-disabled", "true"); buyEl.setAttribute("role", "link");
  }

  var attrs = data.variationAttributes || [], variations = data.variations || [];
  if (attrs.length && variations.length) {
    var start = variations.filter(function (v) { return v.available !== false; })[0] || variations[0];
    var selection = Object.assign({}, start.options);
    var holder = $("variations");

    var update = function () {
      var match = variations.filter(function (v) {
        return attrs.every(function (a) { return v.options[a.name] === selection[a.name]; });
      })[0];
      if (match && match.available !== false && typeof match.price === "number" && isEbayUrl(match.ebayUrl)) {
        var text = formatPrice(match.price, data.currency);
        priceEl.textContent = text; enableBuy(match.ebayUrl); announce("Price " + text);
      } else {
        priceEl.textContent = "Not available"; disableBuy();
        announce("This combination is not available.");
      }
    };

    attrs.forEach(function (attr, n) {
      var set = document.createElement("fieldset"); set.className = "variation-group";
      var legend = document.createElement("legend"); legend.textContent = attr.name; set.appendChild(legend);
      var row = document.createElement("div"); row.className = "variation-options"; set.appendChild(row);
      attr.options.forEach(function (option) {
        var label = document.createElement("label"); label.className = "variation-option";
        var input = document.createElement("input");
        input.type = "radio"; input.name = "variation-" + n; input.value = option;
        input.checked = selection[attr.name] === option;
        input.addEventListener("change", function () { selection[attr.name] = option; update(); });
        var text = document.createElement("span"); text.textContent = option;
        label.appendChild(input); label.appendChild(text); row.appendChild(label);
      });
      holder.appendChild(set);
    });
    update(); announce("");
  } else if (typeof data.price !== "number" || !isEbayUrl(data.ebayUrl)) {
    disableBuy();
  }
})();
