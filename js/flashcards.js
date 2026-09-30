/* =========================================================
   Flashcard engine
   One player for every deck. A deck is a JSON file in
   data/decks/ — see README for the format.
   Page: flashcards/index.html?deck=<id>
   ========================================================= */
(function(){
  const { $, esc, shuffle, store, param, loadJSON, chip, srs } = window.Site;
  const DATA = "../data/decks/";

  const MODE_LABELS = { le:"Latin → English", el:"English → Latin", pp:"Principal parts" };
  const TIMER_CHOICES = [0, 5, 10, 20];           // seconds; 0 = off
  const PPL = ["1st","2nd","3rd","4th"];

  let deck, st, timerId = null;

  // Collapsible sections remember whether the student left them open.
  // Desktop and phone are remembered separately: something closed on a phone stays open on a laptop.
  const wide = () => matchMedia("(min-width: 980px)").matches;
  function remember(el, name, dflt){
    const k = `ui:${name}:${wide() ? "wide" : "narrow"}`, v = store.get(k, null);
    el.open = v === null ? dflt : v;
    el.addEventListener("toggle", () => store.set(k, el.open));
  }

  // Search ignores macrons and case: "fero" finds ferō. Every word of the query must appear.
  const fold = x => String(x ?? "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const terms = q => fold(q).split(/[^a-z0-9]+/).filter(Boolean);
  // Each query word must start a word on the card, so "war" finds war and warfare but not toward
  const haystack = c => c._hay || (c._hay = " " + fold([c.la, c.en, c.pp, c.parse, c.pn, c.tl, c.lemma, c.gloss, c.tag].filter(Boolean).join(" ")).replace(/[^a-z0-9]+/g, " "));
  const matches = (c, ts) => ts.every(t => haystack(c).includes(" " + t));
  // Best matches first: the Latin starts with the query, then a Latin word does, then an English word does
  function score(c, q){
    const la = fold(c.la), en = fold(c.en), words = s => s.split(/[\s,;()/.\-]+/);
    if(la === q || la.startsWith(q + " ") || la.startsWith(q + ",")) return 0;
    if(la.startsWith(q)) return 1;
    if(words(la).some(w => w.startsWith(q))) return 2;
    if(words(en).includes(q)) return 3;
    if(words(en).some(w => w.startsWith(q))) return 4;
    return 5;
  }

  /* ---------- entry ---------- */
  // (started at the bottom of this file, once every helper is defined)

  async function showPicker(){
    $("player").hidden = true; $("picker").hidden = false;
    document.title = "Flashcards";
    try{
      const decks = await loadJSON(DATA+"index.json");
      const groups = {};
      decks.forEach(d => (groups[d.course] = groups[d.course] || []).push(d));
      $("deck-groups").innerHTML = Object.entries(groups).map(([course, ds]) =>
        `<details class="deck-sec" data-course="${esc(course)}"><summary><h2 class="label deck-group">${esc(course)}</h2><span class="deck-sec-n">${ds.length} deck${ds.length > 1 ? "s" : ""}</span></summary><ul class="deck-list">` +
        ds.map((d, j) => `<li><a class="panel" href="?deck=${encodeURIComponent(d.id)}${d.view ? "&view="+encodeURIComponent(d.view) : ""}"><span class="t">${esc(d.title)}</span><span class="n"><span class="due" data-entry="${decks.indexOf(d)}" hidden></span>${d.count} cards</span></a></li>`).join("") +
        `</ul></details>`).join("");
      const secs = [...document.querySelectorAll(".deck-sec")];
      secs.forEach(d => remember(d, "group:" + d.dataset.course, true));
      $("expand-all").onclick = () => secs.forEach(d => d.open = true);
      $("collapse-all").onclick = () => secs.forEach(d => d.open = false);
      remember($("srs-panel"), "progress", false);
      wireProgressPanel();
      showDueCounts(decks);
      wireSearch(decks, secs);
    }catch(e){ $("deck-groups").innerHTML = `<p class="callout">Couldn't load the deck list. (${esc(e.message)})</p>`; }
  }

  // Due counts on the deck list. Only decks this student has studied are fetched.
  async function showDueCounts(entries){
    const db = srs.load(), day = srs.today();
    const studied = new Set(Object.keys(db.cards).map(k => k.split(":")[0]));
    let total = 0;
    for(const id of studied){
      let d; try{ d = await loadJSON(DATA+encodeURIComponent(id)+".json"); }catch(e){ continue; }
      const dueIn = cards => cards.filter(c => srs.isDue(db.cards[srs.key(d.id, c)], day)).length;
      total += dueIn(d.cards);
      entries.forEach((en, j) => {
        if(en.id !== id) return;
        const v = en.view && d.views && d.views[en.view];
        const cards = v ? d.cards.filter(c => Object.entries(v.sel || {}).every(([f, vals]) => c[f] === undefined || vals.includes(c[f]))) : d.cards;
        const n = dueIn(cards), el = document.querySelector(`.due[data-entry="${j}"]`);
        if(n && el){ el.textContent = `${n} due`; el.hidden = false; }
      });
    }
    $("srs-due").textContent = total ? `${total} card${total > 1 ? "s" : ""} due today` : Object.keys(db.cards).length ? "Nothing due today" : "Not started yet";
    $("srs-start").hidden = !total;
    $("srs-start-n").textContent = total;
    $("srs-idle").hidden = !!total;
    $("srs-idle").textContent = Object.keys(db.cards).length ? "Nothing due today. To learn new cards, open a deck in Spaced repetition." : "Want spaced repetition? In any deck, choose Settings → Study → Spaced repetition: each card then comes back just before you'd forget it.";
    $("srs-stats").textContent = `${Object.keys(db.cards).length} cards studied with spaced repetition on this device.`;
  }

  /* Search on the deck list: narrows the decks by title and lists matching words from every deck */
  function wireSearch(entries, secs){
    const box = $("search"), out = $("search-results");
    let all = null, timer = null, before = null;
    // every deck file once, on the first search
    const loadAll = () => all || (all = Promise.all([...new Set(entries.map(e => e.id))].map(id =>
      loadJSON(DATA+encodeURIComponent(id)+".json").catch(() => null))).then(ds => ds.filter(Boolean)));
    async function run(){
      const raw = box.value.trim(), q = fold(raw), ts = terms(raw);
      if(!ts.length){
        out.hidden = true; out.innerHTML = "";
        document.querySelectorAll(".deck-list li").forEach(li => li.hidden = false);
        secs.forEach((d, j) => { d.hidden = false; if(before) d.open = before[j]; });
        before = null; return;
      }
      if(!before) before = secs.map(d => d.open);
      // decks whose name (or group) matches
      secs.forEach(d => {
        const course = fold(d.dataset.course); let any = false;
        d.querySelectorAll("li").forEach(li => { const hit = ts.every(t => (course + " " + fold(li.textContent)).includes(t)); li.hidden = !hit; any = any || hit; });
        d.hidden = !any; if(any) d.open = true;
      });
      const nDecks = secs.reduce((n, d) => n + d.querySelectorAll("li:not([hidden])").length, 0);
      // words from every deck, grouped by deck
      out.hidden = false; out.innerHTML = '<p class="fc-sub">Searching…</p>';
      const decks = await loadAll();
      if(box.value.trim() !== raw) return;          // the student kept typing
      const groups = decks.map(d => {
        const hits = d.cards.filter(c => matches(c, ts)).map(c => ({ c, s: score(c, q) })).sort((a, b) => a.s - b.s);
        return { d, hits, best: hits.length ? hits[0].s : 9 };
      }).filter(g => g.hits.length).sort((a, b) => a.best - b.best || a.hits.length - b.hits.length);
      const total = groups.reduce((n, g) => n + g.hits.length, 0);
      const link = d => `?deck=${encodeURIComponent(d.id)}&q=${encodeURIComponent(raw)}&study=practice`;
      const line = c => `<li><span class="la" lang="la">${esc(c.la)}</span> <span class="en">${esc(c.en)}</span>` +
        ((c.pn || c.tl || c.parse) ? ` <span class="ps">${esc(c.parse || [c.pn, c.tl].filter(Boolean).join(", "))}</span>` : "") + `</li>`;
      out.innerHTML = `<h2 class="label deck-group">Words</h2>` + (groups.length
        ? `<p class="fc-sub">${total} card${total > 1 ? "s" : ""} in ${groups.length} deck${groups.length > 1 ? "s" : ""}${nDecks ? "" : " · no deck names match"}</p>` +
          groups.map(g => `<div class="panel fc-hitdeck"><a class="fc-hithead" href="${link(g.d)}"><b>${esc(g.d.title)}</b><span>${g.hits.length > 1 ? `study these ${g.hits.length} cards →` : "study this card →"}</span></a>` +
            `<ul class="fc-hits">${g.hits.slice(0, 5).map(h => line(h.c)).join("")}</ul>` +
            (g.hits.length > 5 ? `<p class="fc-sub">and ${g.hits.length - 5} more</p>` : "") + `</div>`).join("")
        : `<p class="fc-sub">No cards contain “${esc(raw)}”.${nDecks ? "" : " No deck names match either."}</p>`);
    }
    box.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(run, 180); });
    box.addEventListener("keydown", e => { if(e.key === "Escape"){ box.value = ""; run(); } });
    if(box.value) run();                            // the browser kept the text after Back
  }

  // Export / import / reset of this browser's review history
  function wireProgressPanel(){
    const msg = t => $("srs-msg").textContent = t;
    $("srs-export").onclick = () => {
      const a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([srs.exportText()], { type:"application/json" }));
      a.download = `latin-flashcards-progress-${new Date().toISOString().slice(0,10)}.json`;
      document.body.appendChild(a); a.click(); a.remove();
      msg("Progress file downloaded. Load it on another device to carry on there.");
    };
    $("srs-import").onclick = () => $("srs-file").click();
    $("srs-file").onchange = async e => {
      const f = e.target.files[0]; if(!f) return;
      try{ const r = srs.importText(await f.text()); msg(`Loaded: ${r.added} new cards, ${r.updated} updated.`); showDueCounts(await loadJSON(DATA+"index.json")); }
      catch(err){ msg("Couldn't read that file. " + err.message); }
      e.target.value = "";
    };
    let armed = false;
    $("srs-reset").onclick = () => {
      if(!armed){ armed = true; $("srs-reset").textContent = "Click again to erase all progress"; setTimeout(() => { armed = false; $("srs-reset").textContent = "Reset progress"; }, 4000); return; }
      srs.reset(); armed = false; $("srs-reset").textContent = "Reset progress";
      document.querySelectorAll(".due").forEach(el => el.hidden = true);
      msg("Progress erased on this device."); $("srs-due").textContent = "Not started yet"; $("srs-stats").textContent = "";
      $("srs-start").hidden = true; $("srs-idle").hidden = false;
      $("srs-idle").textContent = "Want spaced repetition? In any deck, choose Settings → Study → Spaced repetition: each card then comes back just before you'd forget it.";
    };
  }

  async function loadDeck(id){
    try{ deck = await loadJSON(DATA+encodeURIComponent(id)+".json"); }
    catch(e){ $("player").innerHTML = `<p class="callout">No deck called “${esc(id)}”. <a href="./">See all decks</a>.</p>`; return; }

    document.title = deck.title + " · Flashcards";
    $("title").textContent = deck.title;
    $("subtitle").textContent = deck.subtitle || "";

    // grammar note and paradigm tables are written by us, so they're inserted as HTML
    if(deck.intro){ $("intro-body").innerHTML = deck.intro; $("intro").hidden = false; }
    if(deck.introTitle) $("intro").querySelector("summary").textContent = deck.introTitle;
    if(deck.paradigm){ $("paradigms").hidden = false; $("paradigm-note").innerHTML = deck.paradigmNote || ""; }

    deck.cards.forEach((c, i) => c._i = i);
    if(deck.lookalikes) markLookalikes(deck.cards);

    // restore saved settings for THIS deck (each deck has its own slot)
    const saved = store.get("fc:"+deck.id, {});
    st = { sel:{}, mode: deck.modes.includes(saved.mode) ? saved.mode : deck.modes[0],
           timer: store.get("fc:timer", 0), order:[], i:0, flipped:false, known:{}, finished:false };
    deck.filters.forEach(f => {
      const all = f.values.map(v => v.v);
      const keep = (saved.sel && saved.sel[f.field] || []).filter(v => all.includes(v));
      st.sel[f.field] = new Set(keep.length ? keep : all);
    });

    // A link can preset filters and mode, e.g. ?deck=noun-declensions&decl=3,4&mode=el
    // Presets apply to that visit only and aren't saved over the student's own settings.
    deck.filters.forEach(f => {
      const q = param(f.field); if(!q) return;
      const want = q.split(","), vals = f.values.map(v => v.v).filter(v => want.includes(String(v)));
      if(vals.length){ st.sel[f.field] = new Set(vals); st.preset = true; }
    });
    // a search from the deck list: every card that matches, whatever this deck's saved filters are (never saved)
    st.q = param("q") || "";
    if(st.q){ deck.filters.forEach(f => { if(!param(f.field)) st.sel[f.field] = new Set(f.values.map(v => v.v)); }); st.preset = true; }
    const m = param("mode"); if(m && deck.modes.includes(m)){ st.mode = m; st.preset = true; }
    st.study = param("study") || store.get("fc:study:"+deck.id, "practice");   // Standard by default; spaced repetition is opt-in

    // A view is a named slice of the deck with its own entry on the deck list (?deck=participles&view=pres).
    // It fixes some filters, hides their rows, and hides rows that none of its cards use (adverbs have no gender).
    st.hidden = new Set();
    const vname = param("view"), view = vname && deck.views && deck.views[vname];
    if(view){
      st.view = view; st.preset = true;
      Object.entries(view.sel || {}).forEach(([field, vals]) => {
        const f = filterOf(field); if(!f) return;
        st.sel[field] = new Set(f.values.map(v => v.v).filter(v => vals.includes(v)));
        st.hidden.add(field);
      });
      const fixed = deck.filters.filter(f => st.hidden.has(f.field));
      const inView = deck.cards.filter(c => passes(c, fixed));
      deck.filters.forEach(f => { if(!inView.some(c => c[f.field] !== undefined)) st.hidden.add(f.field); });
      st.inView = inView;   // used to hide chips that would match nothing in this view
      document.title = view.title + " · Flashcards";
      $("title").textContent = view.title;
      $("subtitle").textContent = view.subtitle || deck.subtitle || "";
      if(view.paradigmNote !== undefined) $("paradigm-note").innerHTML = view.paradigmNote;
    }

    remember($("settings"), "settings", wide());           // open on desktop, a one-line summary on phones
    remember($("intro"), "intro:" + deck.id, wide());      // open beside the card on desktop; tucked away on phones
    remember($("paradigms"), "paradigms:" + deck.id, false);

    buildControlRows();
    wireEvents();
    reset();
  }

  /* ---------- spaced repetition across every deck (?review=all) ---------- */
  async function loadAllReview(){
    const db = srs.load(), day = srs.today();
    const ids = [...new Set(Object.keys(db.cards).map(k => k.split(":")[0]))];
    const pool = [];
    for(const id of ids){
      let d; try{ d = await loadJSON(DATA+encodeURIComponent(id)+".json"); }catch(e){ continue; }
      d.cards.forEach((c, i) => { c._i = id + ":" + i; c._deck = d; });
      if(d.lookalikes) markLookalikes(d.cards);
      d.cards.forEach(c => { if(srs.isDue(db.cards[srs.key(d.id, c)], day)) pool.push(c); });
    }
    // a stand-in "deck" for the settings panel: just direction and timer
    deck = { id:"all", title:"Spaced repetition", modes:["le","el"], filters:[], cards:[] };
    const saved = store.get("fc:all", {});
    st = { all:true, pool, sel:{}, hidden:new Set(), study:"review", mode: ["le","el"].includes(saved.mode) ? saved.mode : "le",
           timer: store.get("fc:timer", 0), order:[], i:0, flipped:false, known:{}, finished:false };
    document.title = "Spaced repetition · Flashcards";
    $("title").textContent = "Spaced repetition";
    $("subtitle").textContent = "Everything due today, from every deck you've studied";
    remember($("settings"), "settings", wide());
    buildControlRows(); wireEvents(); reset();
  }

  /* ---------- data helpers ---------- */
  function markLookalikes(cards){
    const by = {};
    cards.forEach(c => (by[c.la] = by[c.la] || []).push(c));
    cards.forEach(c => { const o = by[c.la].filter(x => x !== c); if(o.length) c.also = o.map(x => x.parse).join("; "); });
  }
  const filterOf = (field, dk = deck) => dk.filters.find(f => f.field === field);
  const valueInfo = (field, v, dk) => { const f = filterOf(field, dk); return f && f.values.find(x => x.v === v); };
  const fillMeta = (tpl, c, dk) => tpl.replace(/\{(\w+)\}/g, (_, k) => { const i = valueInfo(k, c[k], dk); return i ? (i.short || i.label) : (c[k] ?? ""); });
  // In the all-decks session each card carries its own deck (c._deck); otherwise it's the open deck
  const deckOf = c => c._deck || deck;
  const cardKey = c => srs.key(deckOf(c).id, c);
  // a card without a filter's field (e.g. an adverb has no gender) ignores that filter
  const passes = (c, fields) => fields.every(f => c[f.field] === undefined || st.sel[f.field].has(c[f.field]));

  function currentDeck(){
    if(st.all) return st.pool;
    const ts = terms(st.q);
    return deck.cards.filter(c => passes(c, deck.filters) && (st.mode !== "pp" || c.pp) && (!ts.length || matches(c, ts)));
  }

  /* ---------- controls ---------- */
  function buildControlRows(){
    const box = $("controls"); box.innerHTML = "";
    const row = (key, label) => { const r = document.createElement("div"); r.className = "fc-row"; r.id = "row-"+key;
      r.innerHTML = `<span class="label">${esc(label)}</span>`; box.appendChild(r); };
    if(!st.all) row("search", "Search");
    if(!st.all) row("study", "Study");
    if(deck.modes.length > 1) row("mode", "Mode");
    deck.filters.forEach(f => { if(!st.hidden.has(f.field)) row(f.field, f.label); });
    row("timer", "Timer");
    if(!st.all){
      // search this deck: Latin, English, principal parts or parse
      const inp = document.createElement("input");
      inp.type = "search"; inp.id = "fc-q"; inp.className = "fc-q"; inp.value = st.q;
      inp.placeholder = "Latin or English"; inp.setAttribute("aria-label", "Search this deck");
      let t = null;
      inp.addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => { st.q = inp.value.trim(); reset(); }, 200); });
      inp.addEventListener("keydown", e => { if(e.key === "Escape" && inp.value){ inp.value = ""; st.q = ""; reset(); } });
      $("row-search").appendChild(inp);
    }
  }

  function renderControls(){
    document.querySelectorAll("#controls .chip").forEach(c => c.remove());
    deck.filters.forEach(f => {
      if(st.hidden.has(f.field)) return;
      const r = $("row-"+f.field), all = f.values.map(v => v.v), set = st.sel[f.field], isAll = set.size === all.length;
      chip(r, "All", isAll, () => { st.sel[f.field] = new Set(all); reset(); });
      f.values.forEach(v => (st.inView && !st.inView.some(c => c[f.field] === v.v)) || chip(r, v.label, !isAll && set.has(v.v), () => {
        const s = st.sel[f.field];
        if(s.size === all.length) st.sel[f.field] = new Set([v.v]);   // first click narrows to one
        else if(s.has(v.v) && s.size > 1) s.delete(v.v);
        else s.add(v.v);
        reset();
      }));
    });
    const due = reviewCounts();
    if(!st.all){
      chip($("row-study"), "Standard", st.study === "practice", () => setStudy("practice"));
      chip($("row-study"), due.due + due.fresh ? `Spaced repetition · ${due.due} due${due.fresh ? `, ${due.fresh} new` : ""}` : "Spaced repetition · nothing due", st.study === "review", () => setStudy("review"));
    }
    if(deck.modes.length > 1)
      deck.modes.forEach(m => chip($("row-mode"), (deck.modeLabels && deck.modeLabels[m]) || MODE_LABELS[m], st.mode === m, () => {
        st.mode = m; save(); renderControls(); render();   // same cards and history in either direction
      }));
    TIMER_CHOICES.forEach(s => chip($("row-timer"), s ? s+" s" : "Off", st.timer === s, () => {
      st.timer = s; store.set("fc:timer", s); renderControls(); render();
    }));
    summarise();
  }

  // One line describing the current settings, shown when the Settings panel is collapsed
  function summarise(){
    const parts = [st.study === "review" ? "Spaced repetition" : "Standard"];
    if(deck.modes.length > 1) parts.push((deck.modeLabels && deck.modeLabels[st.mode]) || MODE_LABELS[st.mode]);
    deck.filters.forEach(f => {
      if(st.hidden.has(f.field) || st.sel[f.field].size === f.values.length) return;
      const labels = f.values.filter(v => st.sel[f.field].has(v.v)).map(v => v.label);
      parts.push(labels.length > 2 ? `${f.label}: ${labels.length} chosen` : labels.join(", "));
    });
    if(st.timer) parts.push(`${st.timer} s timer`);
    if(st.q) parts.push(`“${st.q}”`);
    $("settings-summary").textContent = parts.join(" · ");
  }

  function save(){
    if(st.all){ store.set("fc:all", { mode: st.mode }); return; }
    if(st.preset) return;
    const sel = {}; for(const k in st.sel) sel[k] = [...st.sel[k]];
    store.set("fc:"+deck.id, { sel, mode: st.mode });
  }

  /* ---------- card rendering ---------- */
  // Latin form, with the ending highlighted when the card splits stem + ending
  const formHTML = c => c.end ? esc(c.stem) + `<span class="end">${esc(c.end)}</span>` : esc(c.la);

  function ppGrid(pp){
    return '<div class="fc-pp">' + pp.split(/,\s*/).map((p,k) =>
      `<div><small class="label">${PPL[k]}</small>${k === 0 ? esc(p) : "<strong>"+esc(p)+"</strong>"}</div>`).join("") + '</div>';
  }
  const meta = ([l, r]) => `<div class="fc-meta label"><span>${esc(l)}</span><b>${esc(r)}</b></div>`;
  const cap = s => s ? s[0].toUpperCase() + s.slice(1) : "";

  function faces(c){
    const dk = deckOf(c);
    const la = `<div class="fc-main la" lang="la">${formHTML(c)}</div>`;
    const en = `<div class="fc-main en">${esc(c.en)}</div>`;
    const parseText = c.parse || [c.pn, c.tl].filter(Boolean).join(" · ");
    const parse = parseText ? `<div class="parse">${esc(parseText)}</div>` : "";
    const pp = c.pp ? ppGrid(c.pp) : "";
    const detail = c.detail ? `<div class="fc-sub">${esc(c.detail)}</div>` : "";
    const also = c.also ? `<div class="fc-also">Same spelling: ${esc(c.also)}</div>` : "";
    const note = c.note ? `<div class="fc-also">${esc(c.note)}</div>` : "";
    // Forms that need parsing (verb and noun cards) get a prompt on the Latin side
    const cue = c.pn ? `<div class="fc-sub">${dk.cue || (dk.allReadings ? "Translate: give every possible case" : "Translate and parse")}</div>` : "";
    switch(st.mode){
      case "le": {
        if(dk.allReadings){
          // every card of the same word with the same spelling (e.g. equī = gen. sg. AND nom. pl.)
          const f = dk.allReadings, same = dk.cards.filter(x => x.la === c.la && x[f] === c[f]);
          const head = same.length > 1 ? `<div class="fc-also">${same.length} possibilities</div>` : "";
          return [la + cue, la + head +
                  `<ul class="fc-readings">${same.map(x => `<li><b>${esc(x.pn)}</b>${x.tl ? ` · ${esc(x.tl)}` : ""} <span>— ${esc(x.en)}</span></li>`).join("")}</ul>`];
        }
        return [la + cue, en + parse + pp + detail + also + note];
      }
      case "el": return [en + parse, la + pp + detail + also + note];
      case "pp": return [`<div class="fc-main la" lang="la">${esc(c.pp.split(",")[0])}</div><div class="fc-sub">${esc(c.en)}</div><div class="fc-sub">Give the principal parts</div>`,
                         ppGrid(c.pp) + `<div class="fc-sub">${esc(c.en)}</div>`];
    }
  }

  function renderStatus(){
    if(st.study === "review"){
      const db = srs.load(), left = st.order.length, fresh = st.order.filter(c => !db.cards[cardKey(c)]).length;
      $("count").textContent = st.finished ? "Session complete" : `${left - fresh} due · ${fresh} new`;
      $("score").textContent = `Reviewed: ${st.reviewed}`;
      $("prog").style.width = (st.reviewed + left) ? (st.reviewed / (st.reviewed + left) * 100) + "%" : "100%";
      return;
    }
    const n = st.order.length, got = st.order.filter(c => st.known[c._i] === true).length;
    $("count").textContent = st.finished ? "Round complete" : (n ? `Card ${st.i+1} of ${n}` : "0 cards");
    $("score").textContent = n ? `Got it: ${got} / ${n}` : "";
    $("prog").style.width = n ? (got/n*100) + "%" : "0";
  }

  function render(){
    stopTimer();
    renderStatus();
    $("stage").hidden = st.finished; $("done").hidden = !st.finished;
    if(st.finished) return renderDone();

    const d = st.order, card = $("card");
    card.classList.toggle("flipped", st.flipped);
    if(!d.length){
      showButtons(null);
      $("front").innerHTML = `<p class="fc-empty">${st.q ? `No cards match “${esc(st.q)}” with these settings.` : "No cards match these filters."}</p>`; $("back").innerHTML = ""; return;
    }
    const c = d[st.i], dk = deckOf(c), m = dk.meta || { front:["",""], back:["",""] };
    showButtons(c);
    const [f, b] = faces(c);
    $("front").innerHTML = meta(m.front.map(t => fillMeta(t, c, dk))) + f +
      (st.timer ? '<div class="fc-timer"><i id="timer-bar"></i></div>' : '<span class="fc-hint">tap to flip</span>');
    $("back").innerHTML  = meta(m.back.map(t => fillMeta(t, c, dk))) + b;
    sizeCard(card);
    if(st.timer && !st.flipped) startTimer();
  }

  function renderDone(){
    if(st.study === "review") return renderReviewDone();
    $("restart").textContent = "Start over";
    const n = st.order.length, missed = st.order.filter(c => st.known[c._i] !== true);
    $("done-title").textContent = missed.length ? "Bene!" : "Optimē!";
    $("done-text").textContent = `You got ${n - missed.length} of ${n}.`;
    $("review").hidden = !missed.length;
    $("review").textContent = `Review the ${missed.length} missed`;
    $("review").onclick = () => startRound(missed);
  }

  // grow the card to fit whichever face is taller
  function sizeCard(card){
    requestAnimationFrame(() => {
      const h = Math.max(300, ...[...card.children].map(x => { x.style.position = "static"; const v = x.offsetHeight; x.style.position = ""; return v; }));
      card.style.minHeight = h + "px";
    });
  }

  /* ---------- paradigm tables (built from the cards themselves) ---------- */
  function renderParadigms(){
    const P = deck.paradigm; if(!P) return;
    const keep = deck.filters.filter(f => f.field === P.group || f.field === P.table);
    const cards = deck.cards.filter(c => passes(c, keep) && c.pi !== undefined);
    // group by a filter's values, or (for a field with no filter, e.g. mood + tense) by the values in card order
    const groups = !P.group ? [null]
      : filterOf(P.group) ? filterOf(P.group).values.map(v => v.v)
      : [...new Set(cards.map(c => c[P.group]).filter(v => v !== undefined))];
    const tables = filterOf(P.table).values;
    const shown = st.view && st.view.groups ? groups.filter(g => st.view.groups.includes(g)) : groups;
    $("paradigm").innerHTML = shown.map(g => {
      const inG = cards.filter(c => g === null || c[P.group] === g);
      if(!inG.length) return "";
      const head = g !== null ? `<h3 class="fc-tensehead">${esc((P.headings && P.headings[g]) || g)}</h3>` : "";
      return head + '<div class="fc-grid">' + tables.map(tv => {
        // rows, columns and row heading can differ per group (e.g. imperatives vs. infinitives)
        const by = (k, dflt) => (P[k+"By"] && P[k+"By"][g]) || P[k] || dflt;
        const R = by("rows", ["1st","2nd","3rd"]), C = by("cols", ["Singular","Plural"]), n = R.length;
        const six = inG.filter(c => c[P.table] === tv.v).sort((a,b) => a.pi - b.pi);
        if(six.length < n*2) return "";
        const cell = i => `<td lang="la">${formHTML(six[i])}</td>`;
        const rows = R.map((p,i) => `<tr><td>${esc(p)}</td>${cell(i)}${cell(i+n)}</tr>`).join("");
        return `<div><div class="label">${esc(tv.label)}${P.tableSuffix ?? " conjugation"}</div>
          <h4><span lang="la">${esc(six[0].lemma)}</span> <small>${esc(six[0].gloss)}</small></h4>` +
          (six[0].tnote ? `<div class="fc-tnote">${esc(six[0].tnote)}</div>` : "") +
          `<table><thead><tr><th class="label">${esc(by("rowLabel", "Person"))}</th><th class="label">${esc(C[0])}</th><th class="label">${esc(C[1])}</th></tr></thead><tbody>${rows}</tbody></table></div>`;
      }).join("") + "</div>";
    }).join("");
  }

  /* ---------- timer ---------- */
  function startTimer(){
    const bar = $("timer-bar");
    if(bar){
      bar.style.transition = "none"; bar.style.transform = "scaleX(1)";
      requestAnimationFrame(() => requestAnimationFrame(() => {
        bar.style.transition = `transform ${st.timer}s linear`; bar.style.transform = "scaleX(0)";
      }));
    }
    timerId = setTimeout(() => { timerId = null; st.flipped = true; render(); }, st.timer * 1000);
  }
  function stopTimer(){ if(timerId){ clearTimeout(timerId); timerId = null; } }

  /* ---------- spaced repetition (Review) ---------- */
  const slot = () => deck.id;

  // Due / new counts for the current filters and direction (shown on the Review chip)
  function reviewCounts(){
    const db = srs.load(), day = srs.today(); let due = 0, fresh = 0;
    currentDeck().forEach(c => { const e = db.cards[cardKey(c)]; if(!e) fresh++; else if(srs.isDue(e, day)) due++; });
    return { due, fresh: Math.max(0, Math.min(fresh, srs.newLeft(db, slot(), day))) };
  }

  // Queue: cards still being learned, then due reviews (shuffled), then today's allowance of new cards in deck order
  function startReview(){
    const db = srs.load(), day = srs.today(), learning = [], due = [], fresh = [];
    currentDeck().forEach(c => {
      const e = db.cards[cardKey(c)];
      if(!e) fresh.push(c); else if(e.s === "l") learning.push(c); else if(e.d <= day) due.push(c);
    });
    st.order = [...learning, ...shuffle(due), ...fresh.slice(0, Math.max(0, srs.newLeft(db, slot(), day)))];
    st.i = 0; st.flipped = false; st.reviewed = 0; st.finished = !st.order.length;
    render();
  }

  function grade(g){
    if(st.study !== "review" || st.finished || !st.order.length || !st.flipped) return;
    const db = srs.load(), day = srs.today(), c = st.order[0], k = cardKey(c);
    const res = srs.answer(db.cards[k], g, day);
    db.cards[k] = res.entry;
    if(res.wasNew) srs.countNew(db, slot(), day);
    srs.save(db);
    st.order.shift(); st.reviewed++;
    if(res.again) st.order.splice(Math.min(st.order.length, g === 1 ? 3 : 6), 0, c);   // comes back a few cards later
    st.flipped = false; st.finished = !st.order.length;
    renderControls(); render();
  }

  function renderReviewDone(){
    const db = srs.load(), day = srs.today();
    const days = currentDeck().map(c => db.cards[cardKey(c)]).filter(e => e && e.s === "r").map(e => e.d);
    const next = days.length ? Math.min(...days) : null, nextN = days.filter(d => d === next).length;
    const when = next === null ? "" : next <= day ? "Some cards are due again now." : next === day + 1 ? `Next review: tomorrow (${nextN} card${nextN > 1 ? "s" : ""}).` : `Next review: in ${next - day} days (${nextN} card${nextN > 1 ? "s" : ""}).`;
    $("done-title").textContent = st.reviewed ? "Optimē!" : "Nothing due";
    $("done-text").textContent = (st.reviewed ? `You reviewed ${st.reviewed} card${st.reviewed > 1 ? "s" : ""}. ` : "You're all caught up on these cards. ") + when +
      (st.all ? " New cards come from studying a deck." : "");
    $("review").hidden = true;
    $("restart").textContent = st.all ? "Back to the decks" : "Standard mode instead";
  }

  function setStudy(v){ st.study = v; store.set("fc:study:"+deck.id, v); reset(); }

  // Practice shows Prev / Next / Got it; Review shows Flip, then Again / Hard / Good / Easy once the answer is showing
  function showButtons(c){
    const review = st.study === "review";
    $("nav-practice").hidden = review; $("keys-practice").hidden = review; $("keys-review").hidden = !review;
    $("prev").hidden = $("next").hidden = review;
    $("nav-grade").hidden = !review || !st.flipped || !c;
    $("flip").hidden = review && st.flipped;
    if(review && c && st.flipped){
      const labels = srs.preview(srs.load().cards[cardKey(c)], srs.today());
      labels.forEach((t, i) => $("g"+(i+1)).textContent = t);
    }
  }

  /* ---------- actions ---------- */
  function startRound(cards){ st.order = cards; st.i = 0; st.flipped = false; st.known = {}; st.finished = false; render(); }
  function reset(){ save(); renderControls(); renderParadigms(); if(st.study === "review") startReview(); else startRound(currentDeck()); }
  function flip(){ if(st.finished || !st.order.length) return; st.flipped = !st.flipped; render(); }
  function go(n){
    if(st.study === "review" || st.finished || !st.order.length) return;
    const j = st.i + n;
    if(j < 0) return;
    if(j >= st.order.length){ st.finished = true; render(); return; }
    st.i = j; st.flipped = false; render();
  }
  function mark(v){ if(st.study === "review" || st.finished || !st.order.length) return; st.known[st.order[st.i]._i] = v; go(1); }
  function doShuffle(){ if(st.study !== "review") startRound(shuffle(currentDeck())); }

  function wireEvents(){
    $("card").onclick = flip;
    $("flip").onclick = flip;
    $("next").onclick = () => go(1);
    $("prev").onclick = () => go(-1);
    $("again").onclick = () => mark(false);
    $("knew").onclick = () => mark(true);
    $("shuffle").onclick = doShuffle;
    $("restart").onclick = () => st.all ? location.href = "./" : st.study === "review" ? setStudy("practice") : startRound(currentDeck());
    [1,2,3,4].forEach(g => $("grade"+g).onclick = () => grade(g));
    document.addEventListener("keydown", e => {
      const tag = e.target.tagName;
      if(tag === "SUMMARY" || tag === "INPUT") return;
      if(tag === "BUTTON" && (e.key === " " || e.key === "Enter")) return;
      if(e.key === " " || e.key === "Enter"){ e.preventDefault(); flip(); }
      else if(e.key === "ArrowRight") go(1);
      else if(e.key === "ArrowLeft") go(-1);
      else if(st.study === "review" && /^[1-4]$/.test(e.key)) grade(+e.key);
      else if(e.key === "1") mark(false);
      else if(e.key === "2") mark(true);
      else if(e.key.toLowerCase() === "s") doShuffle();
    });
    // don't let the timer run out while the tab is hidden
    document.addEventListener("visibilitychange", () => { if(document.hidden) stopTimer(); else if(st.timer && !st.flipped && !st.finished) render(); });
  }

  const id = param("deck");
  if(param("review") === "all") loadAllReview(); else if(id) loadDeck(id); else showPicker();
})();
