/* Sidebar for the grammar pages and flashcards.
   On wide screens (1100px and up) a fixed sidebar on the left holds:
     - links to the three sections (Grammar · Flashcards · Games)   [off for now: see SITE_NAV]
     - the level switcher (shared with the lists; see js/levels.js)   [off for now: see SITE_NAV]
     - every grammar page or deck, grouped, filtered by level, with the current one marked
   A second tab, "This page" / "This deck", holds the page's own controls, moved there from the page
   (a grammar page's pattern buttons and view toggles; a deck's Settings), so the page itself is just
   the charts or the card. On narrower screens the page keeps its usual layout (controls back in place)
   and a menu button opens the list as a drawer.
   Needs js/common.js and js/levels.js first; styles in css/sidebar.css. */
(function(){
  const { esc, store, loadJSON, levels, param } = window.Site;
  const base = document.currentScript.src.replace(/js\/sidebar\.js.*$/, "");
  const section = document.body.dataset.sb || (/\/flashcards\//.test(location.pathname) ? "flashcards" : "grammar");
  const WIDE = matchMedia("(min-width:1100px)");
  // Section links (Grammar · Flashcards · Games) and the level switcher at the top of the sidebar.
  // Off while the site is reached through Google Sites, which does that navigation; set true to bring them back.
  // With it off, the lists still honour ?level=N in the link (and a level saved earlier).
  const SITE_NAV = false;
  const root = document.documentElement;

  const words = section === "flashcards"
    ? { list:"Decks", all:"All decks", tools:"This deck" }
    : { list:"Pages", all:"All grammar", tools:"This page" };

  // ---------- the list: grammar pages or decks ----------
  let items = [];
  const page = location.pathname.split("/").pop().replace(/\.html$/, "") || "index";
  const deck = param("deck"), view = param("view");
  function entries(){
    if(section === "grammar") return items.map(g => ({
      path: g.path || [g.group], title: g.title, short: g.short, keys: [g.page],
      href: `${base}grammar/${encodeURIComponent(g.page)}.html`, current: g.page === page }));
    return items.flatMap(d => {
      const e = { path: d.path || [d.course], title: d.title, short: d.short, solo: d.solo, keys: [d.view && d.id + "/" + d.view, d.id], n: d.count,
        ck: d.id + (d.view ? "." + d.view : ""),   // combine key (?decks=id.view,…)
        href: `${base}flashcards/index.html?deck=${encodeURIComponent(d.id)}${d.view ? "&view=" + encodeURIComponent(d.view) : ""}`,
        current: d.id === deck && (d.view || null) === (view || null) };
      if(!d.split || combining) return [e];   // combining takes the whole list, not one week
      // a deck split into parts (a vocabulary list's weeks): a sub-menu of links that preset that filter
      const f = d.split.field, chosen = param(f);
      return d.split.values.map(v => ({ ...e, path: [...e.path, e.short || e.title], title: `${d.title}: ${v.label}`, short: v.label,
        href: `${e.href}&${f}=${encodeURIComponent(v.v)}`, current: e.current && chosen === String(v.v), part: true }));
    });
  }
  const onIndex = section === "grammar" ? page === "index" : !deck && !param("decks") && !param("review");

  // ---------- combine decks (flashcards): tick decks in the list, then "Study together" (?decks=…) ----------
  let combining = section === "flashcards" && store.get("sb:combining", false);
  const fromLink = (param("decks") || "").split(",").filter(Boolean);
  const picked = new Set(fromLink.length ? fromLink : store.get("sb:picked", []));
  function drawBar(){
    const bar = q("#sb-combine-bar"); if(!bar) return;
    bar.hidden = !combining;
    const n = picked.size;
    q("#sb-combine-n").textContent = n ? `${n} deck${n > 1 ? "s" : ""} chosen` : "Tick the decks to study together";
    const go = q("#sb-combine-go");
    go.hidden = n < 2;
    go.href = `${base}flashcards/index.html?decks=${[...picked].map(encodeURIComponent).join(",")}`;
  }

  // ---------- build ----------
  const nav = document.createElement("nav");
  nav.className = "sb"; nav.id = "sb"; nav.setAttribute("aria-label", "Site");
  nav.innerHTML = `
    ${SITE_NAV ? `    <div class="sb-head">
      <div class="sb-sections">
        <a href="${base}grammar/index.html"${section === "grammar" ? ' aria-current="true"' : ""}>Grammar</a>
        <a href="${base}flashcards/index.html"${section === "flashcards" ? ' aria-current="true"' : ""}>Flashcards</a>
        <a href="${base}games/index.html">Games</a>
      </div>
      <div class="sb-level" role="group" aria-label="Level"></div>
    </div>` : ""}
    <div class="sb-drawer-bar"><span>Menu</span><button type="button" class="sb-close" aria-label="Close menu">×</button></div>
    <div class="sb-tabs" role="tablist">
      <button type="button" role="tab" id="sb-tab-list" aria-controls="sb-list">${words.list}</button>
      <button type="button" role="tab" id="sb-tab-tools" aria-controls="sb-tools">${words.tools}</button>
    </div>
    <div class="sb-panel" id="sb-list" role="tabpanel" aria-labelledby="sb-tab-list"></div>
    <div class="sb-panel" id="sb-tools" role="tabpanel" aria-labelledby="sb-tab-tools"></div>
    ${section === "flashcards" ? `<div class="sb-combine-bar" id="sb-combine-bar" role="region" aria-label="Combine decks" hidden>
      <span id="sb-combine-n" aria-live="polite"></span>
      <span class="sb-combine-btns"><button type="button" id="sb-combine-clear">Clear</button><a id="sb-combine-go" hidden>Study together →</a></span>
    </div>` : ""}`;
  document.body.prepend(nav);
  const q = s => nav.querySelector(s);

  const opener = document.createElement("button");
  opener.type = "button"; opener.className = "sb-open"; opener.setAttribute("aria-controls", "sb"); opener.setAttribute("aria-expanded", "false");
  opener.innerHTML = `<span class="sb-burger" aria-hidden="true"></span>${words.list}`;
  let bar = null;   // grammar pages on narrow screens: the Pages button in a sticky bar
  if(section === "grammar"){
    bar = document.createElement("div"); bar.className = "sb-bar";
    bar.prepend(opener); document.body.prepend(bar);
  } else document.body.prepend(opener);
  const scrim = document.createElement("div"); scrim.className = "sb-scrim"; document.body.prepend(scrim);

  // ---------- level ----------
  function drawLevel(){
    const box = q(".sb-level"); if(!box) return;
    const names = (levels.data && levels.data.levels) || [];
    const short = ["All", "I", "II", "III", "IV"];
    box.innerHTML = ["All levels", ...names].map((n, i) =>
      `<button type="button" data-i="${i}" aria-pressed="${levels.current === i}" title="${esc(n)}" aria-label="${esc(n)}">${short[i] || i}</button>`).join("");
    box.querySelectorAll("button").forEach(b => b.onclick = () => levels.set(+b.dataset.i));
  }

  // ---------- list ----------
  // groups nest by each item's path (data files: "path": ["Verbs", "Incomplete", "Active"]; default [group])
  const openKey = path => `sb:open:${section}:${path}`;
  function tree(es){
    const root = { kids: [], n: 0 };
    es.forEach(e => {
      let node = root; node.n++;
      e.path.forEach((name, i) => {
        let g = node.kids.find(k => k.group && k.name === name);
        if(!g){ g = { group: true, name, key: e.path.slice(0, i + 1).join("/"), kids: [], n: 0, has: false, solo: e.solo && e.part && i === e.path.length - 1 }; node.kids.push(g); }
        g.n++; if(e.current) g.has = true; node = g;
      });
      node.kids.push(e);
    });
    return root;
  }
  function drawNode(node, depth){
    const link = (e, label) => combining && e.ck
      ? `<li><label class="sb-pick"${label !== e.title ? ` title="${esc(e.title)}"` : ""}><input type="checkbox" data-ck="${esc(e.ck)}"${picked.has(e.ck) ? " checked" : ""}> <span>${esc(label)}</span></label></li>`
      : `<li><a href="${e.href}"${e.current ? ' aria-current="page"' : ""}${label !== e.title ? ` title="${esc(e.title)}"` : ""}>${esc(label)}</a></li>`;
    return node.kids.map(k => {
      // "short": the title without what the headings above it already say (Present, not Present Active Indicative)
      if(!k.group) return link(k, k.short || k.title);
      // "solo": a group left with one item (Vocab, once a level is chosen) is shown as that item, named after the group
      if(k.kids.length === 1 && k.kids[0].solo && !k.kids[0].group) return depth ? link(k.kids[0], k.name) : `<ul class="sb-top">${link(k.kids[0], k.name)}</ul>`;
      if(k.kids.length === 1 && k.kids[0].group && k.kids[0].solo) k = { ...k, kids: k.kids[0].kids };   // Vocab › Week 1…, not Vocab › Latin II › Week 1…
      // grammar (a short list) starts fully open; flashcards (30+ decks) open only down to the current deck
      const open = k.has || store.get(openKey(k.key), false);
      const inner = `<details class="sb-group sb-d${depth}" data-g="${esc(k.key)}"${open ? " open" : ""}><summary>${esc(k.name)}<span>${k.n}</span></summary><ul>${drawNode(k, depth + 1)}</ul></details>`;
      return depth ? `<li class="sb-sub">${inner}</li>` : inner;
    }).join("");
  }
  function drawList(){
    const es = entries().filter(e => e.current || levels.shows(section, e.keys));
    const box = q("#sb-list");
    const all = `<a class="sb-all" href="${base}${section}/index.html"${onIndex ? ' aria-current="page"' : ""}>${words.all}</a>`;
    box.innerHTML =
      (section === "flashcards" ? `<div class="sb-allrow">${all}<button type="button" class="sb-combine" aria-pressed="${combining}" title="Pick several decks and study them as one">Combine</button></div>` : all) +
      drawNode(tree(es), 0) +
      (es.length ? "" : `<p class="sb-empty">Nothing for this level yet.</p>`);
    // remember only what the student opens or closes by hand (not the branch opened for the current page)
    box.querySelectorAll(".sb-group").forEach(d => d.querySelector("summary").addEventListener("click", () => setTimeout(() => store.set(openKey(d.dataset.g), d.open))));
    const cb = box.querySelector(".sb-combine");
    if(cb) cb.onclick = () => { combining = !combining; store.set("sb:combining", combining); drawList(); drawBar(); };
    box.querySelectorAll(".sb-pick input").forEach(i => i.onchange = () => {
      i.checked ? picked.add(i.dataset.ck) : picked.delete(i.dataset.ck);
      store.set("sb:picked", [...picked]); drawBar();
    });
    if(combining) box.querySelectorAll(".sb-pick input:checked").forEach(i => { for(let d = i.closest("details"); d; d = d.parentElement.closest("details")) d.open = true; });
    const cur = box.querySelector('[aria-current="page"]:not(.sb-all)');
    if(cur) requestAnimationFrame(() => {
      const y = cur.getBoundingClientRect().top - box.getBoundingClientRect().top + box.scrollTop;
      if(y > box.clientHeight - 60) box.scrollTop = y - box.clientHeight / 3;
    });
  }

  // ---------- grammar pages: breadcrumb (each step shows that section in the Pages list), Previous / Next ----------
  function decorate(){
    if(section !== "grammar") return;
    const es = entries().filter(e => e.current || levels.shows(section, e.keys));
    const i = es.findIndex(e => e.current), cur = es[i];
    if(!cur) return;
    const wrap = document.querySelector(".wrap");
    let c = document.getElementById("sb-crumbs");
    if(!c){
      c = document.createElement("nav"); c.id = "sb-crumbs"; c.className = "sb-crumbs"; c.setAttribute("aria-label", "Where this page is");
      const hd = wrap.querySelector(":scope > header"); hd ? hd.before(c) : wrap.prepend(c);
      c.addEventListener("click", e => { const b = e.target.closest("[data-crumb]"); if(b) showSection(b.dataset.crumb); });
    }
    c.innerHTML = `<a href="${base}grammar/index.html">Grammar</a>` + cur.path.map((p, i) =>
      `<i aria-hidden="true">\u203a</i><button type="button" data-crumb="${esc(cur.path.slice(0, i + 1).join("/"))}">${esc(p)}</button>`).join("");
    // flashcards for this page (the decks listed in data/grammar.json); overview pages list none
    loadJSON(base + "data/grammar.json").then(g => {
      const me = g.find(p => p.page === page);
      const ids = (me && me.decks) || [];
      if(!ids.length) return;
      return loadJSON(base + "data/decks/index.json").then(ds => {
        const links = ids.map(k => { const d = ds.find(x => x.id + (x.view ? "." + x.view : "") === k); if(!d) return "";
          return `<a href="${base}flashcards/index.html?deck=${encodeURIComponent(d.id)}${d.view ? "&view=" + encodeURIComponent(d.view) : ""}">${esc(d.title)}</a>`; }).filter(Boolean);
        if(!links.length) return;
        let f = document.getElementById("sb-practice");
        if(!f){ f = document.createElement("p"); f.id = "sb-practice"; f.className = "sb-practice"; const hd = wrap.querySelector(":scope > header"); hd ? hd.after(f) : c.after(f); }
        f.innerHTML = `Flashcards: ${links.map(l => l.replace("<a ", '<a class="sb-pbtn" ')).join(" \u00b7 ")}`;
      });
    }).catch(() => {});
  }

  // show a section of the Pages list: the list tab (or the drawer on narrow screens), that group open and in view
  function showSection(key){
    if(!WIDE.matches) drawer(true);
    enterDeck = false; showTab("list");
    const d = [...q("#sb-list").querySelectorAll("details.sb-group")].find(x => x.dataset.g === key);
    if(!d) return;
    for(let x = d; x; x = x.parentElement.closest("details")) x.open = true;
    const box = q("#sb-list"), s = d.querySelector("summary");
    requestAnimationFrame(() => {
      box.scrollTo({ top: d.getBoundingClientRect().top - box.getBoundingClientRect().top + box.scrollTop - 8, behavior: "smooth" });
      s.classList.remove("sb-flash"); void s.offsetWidth; s.classList.add("sb-flash");
    });
  }

  // ---------- tools: move the page's own controls into the sidebar ----------
  const moved = [];     // [node, placeholder]
  function toolNodes(){
    const out = [];
    if(section === "grammar"){
      const jumps = [["background", "Background"], ["charts", "Charts"], ["rules", "Rules"]]
        .filter(([id]) => document.getElementById(id));
      if(jumps.length > 1){
        const j = document.createElement("div"); j.className = "sb-jumps"; j.dataset.made = "1";
        j.innerHTML = `<span class="sb-label">On this page</span>` + jumps.map(([id, t]) => `<a href="#${id}">${t}</a>`).join("");
        out.push(j);
      }
      // the pattern row first, wherever it is (it sits above the charts while the sidebar is hidden)
      const pats = document.getElementById("patterns"); if(pats) out.push(pats);
      document.querySelectorAll(".toolbar > .tb-row, .toolbar > .legend").forEach(n => { if(n !== pats) out.push(n); });
      const toc = document.querySelector("header nav.toc"); if(toc) out.push(toc);
    } else if(!onIndex){   // a deck is open (not the deck list): its Settings
      document.querySelectorAll(".fc-side > *").forEach(n => out.push(n));
    }
    return out;
  }
  let made = null;
  // a script that loads after this one (pattern-notes.js) can ask for a box to sit under the pattern buttons
  window.Site.sidebarAdopt = node => {
    const pats = document.getElementById("patterns");
    made = made || toolNodes();
    const at = made.indexOf(pats); made.splice(at < 0 ? made.length : at + 1, 0, node);
    if(moved.length){
      const ph = document.createComment("sidebar"); node.before(ph);
      if(pats && pats.closest("#sb-tools")) pats.after(node); else q("#sb-tools").appendChild(node);
      moved.push([node, ph]);
    }
  };
  function placeTools(on){
    const box = q("#sb-tools");
    if(on && !moved.length){
      made = made || toolNodes();
      made.forEach(n => {
        if(n.dataset.made){ box.appendChild(n); moved.push([n, null]); return; }
        const ph = document.createComment("sidebar"); n.before(ph); box.appendChild(n); moved.push([n, ph]);
      });
    } else if(!on && moved.length){
      moved.splice(0).forEach(([n, ph]) => ph ? (ph.replaceWith(n)) : n.remove());
    }
    root.classList.toggle("sb-tools-out", on && moved.length > 0);
    if(section === "flashcards") placeSettings(!on);
  }

  // Grammar pages: the patterns, the view toggles and the key sit in one bar directly above the charts,
  // at every screen width (the sidebar is only for finding pages). On wide screens the bar stays in view while the charts scroll.
  function studyBar(){
    if(section !== "grammar") return;
    const tb = document.querySelector(".toolbar"), blk = document.querySelector(".block, #charts .work") ;
    if(!tb || tb.classList.contains("studybar")) return;
    if(tb.querySelector("#tabs")) return;   // case-usages: the case tabs choose which panel is shown, so they must stay above all the panels
    const h = document.querySelector(".block > h3"), work = document.querySelector(".work");
    tb.classList.add("studybar");
    const pats = document.getElementById("patterns"); if(pats) pats.classList.add("above");
    if(h) h.after(tb); else if(work) work.before(tb);
    root.classList.add("has-studybar");
  }

  // Flashcards: in the sidebar, Settings is always open (the tab already names it); without the sidebar
  // (phones, narrow windows) the Settings panel goes under the card, above "Show paradigms", so the card comes first.
  const side = document.querySelector(".fc-side"), settings = document.getElementById("settings");
  const sideHome = side && side.parentNode, sideNext = side && side.nextSibling;
  if(settings) settings.addEventListener("toggle", () => { if(root.classList.contains("sb-tools-out") && !settings.open) settings.open = true; });
  function placeSettings(narrow){
    if(!side || onIndex) return;
    const spot = document.getElementById("paradigms");
    if(narrow && spot && side.nextSibling !== spot) spot.before(side);
    else if(!narrow && side.parentNode !== sideHome) sideHome.insertBefore(side, sideNext);
    root.classList.toggle("sb-settings-below", narrow);
    if(!narrow && settings && root.classList.contains("sb-tools-out")) settings.open = true;
  }

  // ---------- tabs ----------
  const tabKey = "sb:tab:" + section;
  let enterDeck = !onIndex;   // opening a grammar page or a deck lands on its own tab; cleared once the student picks a tab
  function showTab(t){
    const tools = t === "tools" && root.classList.contains("sb-tools-out");
    q("#sb-tab-list").setAttribute("aria-selected", !tools); q("#sb-tab-tools").setAttribute("aria-selected", tools);
    q("#sb-list").hidden = tools; q("#sb-tools").hidden = !tools;
  }
  q("#sb-tab-list").onclick = () => { enterDeck = false; store.set(tabKey, "list"); showTab("list"); };
  q("#sb-tab-tools").onclick = () => { enterDeck = false; store.set(tabKey, "tools"); showTab("tools"); };

  // ---------- layout ----------
  function layout(){
    const wide = WIDE.matches;
    root.classList.toggle("has-sb", wide);
    root.classList.toggle("sb-narrow", !wide);
    root.classList.add("sb-sec-" + section);
    studyBar();
    placeTools(wide && section !== "grammar");
    q(".sb-tabs").hidden = !root.classList.contains("sb-tools-out");
    // opening a grammar page or deck lands on its "This page" / "This deck" tab; after that, the student's tab choice holds for the visit
    const want = enterDeck ? "tools" : store.get(tabKey, "tools");
    showTab(root.classList.contains("sb-tools-out") ? want : "list");
    if(wide) drawer(false);
  }
  WIDE.addEventListener("change", layout);

  // ---------- drawer (narrow screens) ----------
  function drawer(open){
    root.classList.toggle("sb-drawer", open);
    opener.setAttribute("aria-expanded", open);
    if(open) q(".sb-close").focus();
  }
  opener.onclick = () => drawer(true);
  q(".sb-close").onclick = () => { drawer(false); opener.focus(); };
  scrim.onclick = () => drawer(false);
  document.addEventListener("keydown", e => { if(e.key === "Escape" && root.classList.contains("sb-drawer")){ drawer(false); opener.focus(); } });

  layout();
  // ---------- data ----------
  (async () => {
    try{
      const [list] = await Promise.all([
        loadJSON(base + (section === "grammar" ? "data/grammar.json" : "data/decks/index.json")),
        levels.load(base)]);
      items = list;
    }catch(e){ q("#sb-list").innerHTML = `<p class="sb-empty">Couldn't load the list.</p>`; return; }
    drawLevel(); drawList(); drawBar(); decorate();
    const clr = q("#sb-combine-clear");
    if(clr) clr.onclick = () => { picked.clear(); store.set("sb:picked", []); drawList(); drawBar(); };
    window.addEventListener("site:level", () => { drawLevel(); drawList(); decorate(); });
  })();
})();
