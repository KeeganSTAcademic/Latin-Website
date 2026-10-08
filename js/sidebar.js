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
  document.body.prepend(opener);
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
      const open = k.has || store.get(openKey(k.key), section === "grammar");
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
    box.querySelectorAll(".sb-group").forEach(d => d.addEventListener("toggle", () => store.set(openKey(d.dataset.g), d.open)));
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
    // grammar pages: with the sidebar showing, "Highlight a pattern" stays in it; when the sidebar is hidden
    // (narrow windows, phones), the pattern buttons go directly above the charts instead of the top of the page
    if(section === "grammar"){
      const pats = document.getElementById("patterns"), work = document.querySelector(".work");
      if(pats && work){
        const inSidebar = !!pats.closest("#sb-tools");
        if(!inSidebar){ pats.classList.add("above"); work.before(pats); }
        else pats.classList.remove("above");
      }
    }
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
    placeTools(wide);
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
    drawLevel(); drawList(); drawBar();
    const clr = q("#sb-combine-clear");
    if(clr) clr.onclick = () => { picked.clear(); store.set("sb:picked", []); drawList(); drawBar(); };
    window.addEventListener("site:level", () => { drawLevel(); drawList(); });
  })();
})();
