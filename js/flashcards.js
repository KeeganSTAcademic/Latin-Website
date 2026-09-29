/* =========================================================
   Flashcard engine
   One player for every deck. A deck is a JSON file in
   data/decks/ — see README for the format.
   Page: flashcards/index.html?deck=<id>
   ========================================================= */
(function(){
  const { $, esc, shuffle, store, param, loadJSON, chip } = window.Site;
  const DATA = "../data/decks/";

  const MODE_LABELS = { le:"Latin → English", el:"English → Latin", pp:"Principal parts" };
  const TIMER_CHOICES = [0, 5, 10, 20];           // seconds; 0 = off
  const PPL = ["1st","2nd","3rd","4th"];

  let deck, st, timerId = null;

  /* ---------- entry ---------- */
  const id = param("deck");
  if(id) loadDeck(id); else showPicker();

  async function showPicker(){
    $("player").hidden = true; $("picker").hidden = false;
    document.title = "Flashcards";
    try{
      const decks = await loadJSON(DATA+"index.json");
      const groups = {};
      decks.forEach(d => (groups[d.course] = groups[d.course] || []).push(d));
      $("deck-groups").innerHTML = Object.entries(groups).map(([course, ds]) =>
        `<h2 class="label deck-group">${esc(course)}</h2><ul class="deck-list">` +
        ds.map(d => `<li><a class="panel" href="?deck=${encodeURIComponent(d.id)}${d.view ? "&view="+encodeURIComponent(d.view) : ""}"><span class="t">${esc(d.title)}</span><span class="n">${d.count} cards</span></a></li>`).join("") +
        `</ul>`).join("");
    }catch(e){ $("deck-groups").innerHTML = `<p class="callout">Couldn't load the deck list. (${esc(e.message)})</p>`; }
  }

  async function loadDeck(id){
    try{ deck = await loadJSON(DATA+encodeURIComponent(id)+".json"); }
    catch(e){ $("player").innerHTML = `<p class="callout">No deck called “${esc(id)}”. <a href="./">See all decks</a>.</p>`; return; }

    document.title = deck.title + " · Flashcards";
    $("title").textContent = deck.title;
    $("subtitle").textContent = deck.subtitle || "";

    // grammar note and paradigm tables are written by us, so they're inserted as HTML
    if(deck.intro){ $("intro-body").innerHTML = deck.intro; $("intro").hidden = false; }
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
    const m = param("mode"); if(m && deck.modes.includes(m)){ st.mode = m; st.preset = true; }

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

    buildControlRows();
    wireEvents();
    reset();
  }

  /* ---------- data helpers ---------- */
  function markLookalikes(cards){
    const by = {};
    cards.forEach(c => (by[c.la] = by[c.la] || []).push(c));
    cards.forEach(c => { const o = by[c.la].filter(x => x !== c); if(o.length) c.also = o.map(x => x.parse).join("; "); });
  }
  const filterOf = field => deck.filters.find(f => f.field === field);
  const valueInfo = (field, v) => { const f = filterOf(field); return f && f.values.find(x => x.v === v); };
  const fillMeta = (tpl, c) => tpl.replace(/\{(\w+)\}/g, (_, k) => { const i = valueInfo(k, c[k]); return i ? (i.short || i.label) : (c[k] ?? ""); });
  // a card without a filter's field (e.g. an adverb has no gender) ignores that filter
  const passes = (c, fields) => fields.every(f => c[f.field] === undefined || st.sel[f.field].has(c[f.field]));

  function currentDeck(){
    return deck.cards.filter(c => passes(c, deck.filters) && (st.mode !== "pp" || c.pp));
  }

  /* ---------- controls ---------- */
  function buildControlRows(){
    const box = $("controls"); box.innerHTML = "";
    const row = (key, label) => { const r = document.createElement("div"); r.className = "fc-row"; r.id = "row-"+key;
      r.innerHTML = `<span class="label">${esc(label)}</span>`; box.appendChild(r); };
    if(deck.modes.length > 1) row("mode", "Mode");
    deck.filters.forEach(f => { if(!st.hidden.has(f.field)) row(f.field, f.label); });
    row("timer", "Timer");
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
    if(deck.modes.length > 1)
      deck.modes.forEach(m => chip($("row-mode"), (deck.modeLabels && deck.modeLabels[m]) || MODE_LABELS[m], st.mode === m, () => { st.mode = m; save(); renderControls(); render(); }));
    TIMER_CHOICES.forEach(s => chip($("row-timer"), s ? s+" s" : "Off", st.timer === s, () => {
      st.timer = s; store.set("fc:timer", s); renderControls(); render();
    }));
  }

  function save(){
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
    const la = `<div class="fc-main la" lang="la">${formHTML(c)}</div>`;
    const en = `<div class="fc-main en">${esc(c.en)}</div>`;
    const parseText = c.parse || [c.pn, c.tl].filter(Boolean).join(" · ");
    const parse = parseText ? `<div class="parse">${esc(parseText)}</div>` : "";
    const pp = c.pp ? ppGrid(c.pp) : "";
    const detail = c.detail ? `<div class="fc-sub">${esc(c.detail)}</div>` : "";
    const also = c.also ? `<div class="fc-also">Same spelling: ${esc(c.also)}</div>` : "";
    const note = c.note ? `<div class="fc-also">${esc(c.note)}</div>` : "";
    // Forms that need parsing (verb and noun cards) get a prompt on the Latin side
    const cue = c.pn ? `<div class="fc-sub">${deck.cue || (deck.allReadings ? "Translate: give every possible case" : "Translate and parse")}</div>` : "";
    switch(st.mode){
      case "le": {
        if(deck.allReadings){
          // every card of the same word with the same spelling (e.g. equī = gen. sg. AND nom. pl.)
          const f = deck.allReadings, same = deck.cards.filter(x => x.la === c.la && x[f] === c[f]);
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
      $("front").innerHTML = '<p class="fc-empty">No cards match these filters.</p>'; $("back").innerHTML = ""; return;
    }
    const c = d[st.i], m = deck.meta || { front:["",""], back:["",""] };
    const [f, b] = faces(c);
    $("front").innerHTML = meta(m.front.map(t => fillMeta(t, c))) + f +
      (st.timer ? '<div class="fc-timer"><i id="timer-bar"></i></div>' : '<span class="fc-hint">tap to flip</span>');
    $("back").innerHTML  = meta(m.back.map(t => fillMeta(t, c))) + b;
    sizeCard(card);
    if(st.timer && !st.flipped) startTimer();
  }

  function renderDone(){
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

  /* ---------- actions ---------- */
  function startRound(cards){ st.order = cards; st.i = 0; st.flipped = false; st.known = {}; st.finished = false; render(); }
  function reset(){ save(); renderControls(); renderParadigms(); startRound(currentDeck()); }
  function flip(){ if(st.finished || !st.order.length) return; st.flipped = !st.flipped; render(); }
  function go(n){
    if(st.finished || !st.order.length) return;
    const j = st.i + n;
    if(j < 0) return;
    if(j >= st.order.length){ st.finished = true; render(); return; }
    st.i = j; st.flipped = false; render();
  }
  function mark(v){ if(st.finished || !st.order.length) return; st.known[st.order[st.i]._i] = v; go(1); }
  function doShuffle(){ startRound(shuffle(currentDeck())); }

  function wireEvents(){
    $("card").onclick = flip;
    $("flip").onclick = flip;
    $("next").onclick = () => go(1);
    $("prev").onclick = () => go(-1);
    $("again").onclick = () => mark(false);
    $("knew").onclick = () => mark(true);
    $("shuffle").onclick = doShuffle;
    $("restart").onclick = () => startRound(currentDeck());
    document.addEventListener("keydown", e => {
      const tag = e.target.tagName;
      if(tag === "SUMMARY" || tag === "INPUT") return;
      if(tag === "BUTTON" && (e.key === " " || e.key === "Enter")) return;
      if(e.key === " " || e.key === "Enter"){ e.preventDefault(); flip(); }
      else if(e.key === "ArrowRight") go(1);
      else if(e.key === "ArrowLeft") go(-1);
      else if(e.key === "1") mark(false);
      else if(e.key === "2") mark(true);
      else if(e.key.toLowerCase() === "s") doShuffle();
    });
    // don't let the timer run out while the tab is hidden
    document.addEventListener("visibilitychange", () => { if(document.hidden) stopTimer(); else if(st.timer && !st.flipped && !st.finished) render(); });
  }
})();
