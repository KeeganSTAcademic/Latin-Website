/* =========================================================
   Student accounts.
   Load right after common.js (before srs.js and flashcards.js), so a signed-in student's
   flashcard storage is moved under their login before anything reads it.

   Privacy by design:
     - Students never create accounts. The teacher makes a class, which gets a class code and
       a set of logins: a random Latin, Greek or Phoenician name, with a password of a Latin noun
       and an adjective that agrees with it (lupusferox, aquilaalba).
     - No real names, emails or birthdays are stored. The teacher may label logins with real names,
       but those labels stay in the teacher's own browser.

   Two back ends, chosen by data/account-config.json:
     - { "api": "https://script.google.com/macros/s/…/exec" }: the Google Apps Script in server/Code.gs,
       saving to a Sheet and Drive folder in the teacher's Google account.
     - no file, or no "api": the demo, where the "server" is this browser's localStorage.
   Exposed as window.Site.account.
   ========================================================= */
(function(){
  const Site = window.Site, store = Site.store;
  const RAW = {
    get(k, f){ try{ const v = localStorage.getItem(k); return v === null ? f : JSON.parse(v); }catch(e){ return f; } },
    set(k, v){ try{ localStorage.setItem(k, JSON.stringify(v)); }catch(e){} },
    keys(){ try{ return Object.keys(localStorage); }catch(e){ return []; } },
    del(k){ try{ localStorage.removeItem(k); }catch(e){} },
  };
  const DEMO = "latin-demo-server", SESSION = "latin:acct:session", LABELS = "latin:teacher-labels", TEACHER = "latin:acct:teacher";
  const MAX_EVENTS = 4000, SYNC_MS = 20000;
  const here = document.currentScript && document.currentScript.src;
  const ROOT = here ? here.replace(/js\/account\.js.*$/, "") : "../";
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;" }[c]));

  // same day count as srs.js (the day rolls over at 4 a.m.)
  const today = () => { const n = new Date(); n.setHours(n.getHours() - 4); return Math.floor((n.getTime() - n.getTimezoneOffset()*60000) / 864e5); };
  const dayOf = t => { const n = new Date(t); n.setHours(n.getHours() - 4); return Math.floor((n.getTime() - n.getTimezoneOffset()*60000) / 864e5); };
  const normCode = c => String(c || "").toUpperCase().replace(/[^A-Z0-9]/g, "");
  const normLogin = l => String(l || "").trim().toLowerCase();
  const newId = () => Math.random().toString(36).slice(2, 10) + Date.now().toString(36);

  /* ---------- which back end ---------- */
  let API = "";
  let known = false;   // false until the config has loaded; changes made before then wait in the queue
  const ready = fetch(ROOT + "data/account-config.json", { cache:"no-store" })
    .then(r => r.ok ? r.json() : {}).catch(() => ({}))
    .then(c => { API = (c && c.api) || ""; known = true; });
  const mode = () => API ? "live" : "demo";

  async function call(action, body){
    let r;
    try{
      r = await fetch(API, { method:"POST", headers:{ "Content-Type":"text/plain;charset=utf-8" }, body: JSON.stringify({ action, ...body }) });
    }catch(e){ return { ok:false, error:"offline" }; }
    try{ return await r.json(); }catch(e){ return { ok:false, error:"server" }; }
  }

  // deck titles, for the progress pages
  let titles = {};
  const titlesReady = fetch(ROOT + "data/decks/index.json").then(r => r.json())
    .then(list => { for(const d of list) titles[d.id] = d.title; }).catch(() => {});
  const deckTitle = id => titles[id] || id;

  /* ---------- names and passwords (the demo makes them here; the live server makes its own) ---------- */
  const NAMES = [
    "Gaius","Lucius","Marcus","Quintus","Titus","Aulus","Decimus","Gnaeus","Publius","Servius","Sextus","Tiberius","Appius","Numerius",
    "Livia","Julia","Cornelia","Claudia","Tullia","Aemilia","Valeria","Octavia","Fabia","Sulpicia","Lucretia","Antonia","Flavia","Junia",
    "Agathon","Aspasia","Chloe","Daphne","Demetrius","Eudora","Hector","Iris","Kleon","Leander","Lysander","Melissa","Nikias","Phaedra",
    "Sappho","Theron","Xanthe","Zeno","Penelope","Ariadne","Philon","Thais","Kallias","Ione","Myron","Thalia",
    "Hamilcar","Hannibal","Hanno","Hasdrubal","Himilco","Mago","Elissa","Sophonisba","Bomilcar","Adherbal","Gisco","Maharbal","Imilce","Dido","Batbaal","Arishat"
  ];
  const NOUNS = [["lupus","m"],["ursus","m"],["corvus","m"],["leo","m"],["equus","m"],["taurus","m"],["cervus","m"],["delphinus","m"],["cygnus","m"],["gladius","m"],["hortus","m"],["mons","m"],
    ["aquila","f"],["columba","f"],["vulpes","f"],["noctua","f"],["rosa","f"],["silva","f"],["stella","f"],["luna","f"],["navis","f"],["turris","f"],["insula","f"],["villa","f"],
    ["bellum","n"],["caelum","n"],["donum","n"],["saxum","n"],["scutum","n"],["templum","n"],["flumen","n"],["mare","n"],["aurum","n"],["signum","n"]];
  const ADJS = [["ferox","ferox","ferox"],["velox","velox","velox"],["audax","audax","audax"],["felix","felix","felix"],["ingens","ingens","ingens"],
    ["fortis","fortis","forte"],["brevis","brevis","breve"],["acer","acris","acre"],["magnus","magna","magnum"],["parvus","parva","parvum"],
    ["laetus","laeta","laetum"],["clarus","clara","clarum"],["aureus","aurea","aureum"],["niger","nigra","nigrum"],["albus","alba","album"],
    ["ruber","rubra","rubrum"],["altus","alta","altum"],["novus","nova","novum"],["longus","longa","longum"],["bonus","bona","bonum"]];
  const CODE_WORDS = ["FORUM","VESTA","TIBER","AQUILA","LUPA","ROMA","OSTIA","CAPUA","JANUS","MINERVA","LYRA","PHAROS","DELOS","TYRUS","SIDON","UTICA"];
  const pick = a => a[Math.floor(Math.random() * a.length)];
  function freshPassword(used){
    for(let i = 0; i < 500; i++){ const n = pick(NOUNS), a = pick(ADJS), p = n[0] + a[{ m:0, f:1, n:2 }[n[1]]]; if(!used.has(p)){ used.add(p); return p; } }
    return pick(NOUNS)[0] + Math.floor(100 + Math.random() * 900);
  }
  async function hashPw(code, login, pw){
    const data = new TextEncoder().encode(`${normCode(code)}:${normLogin(login)}:${pw}`);
    const buf = await crypto.subtle.digest("SHA-256", data);
    return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join("");
  }

  /* ---------- the demo back end (this browser's localStorage) ---------- */
  const Demo = {
    load(){ return RAW.get(DEMO, null) || { v:1, classes:{}, progress:{} }; },
    save(db){ RAW.set(DEMO, db); },
    pkey(code, login){ return normCode(code) + "/" + normLogin(login); },
    student(db, code, login){ const k = Demo.pkey(code, login); return db.progress[k] || (db.progress[k] = { store:{}, events:[], last:0 }); },
  };
  // The sample class (Latin II · Period 3), built from the real decks; times are relative so it always looks current.
  let sampleLoading = null;
  function ensureSample(){
    if(mode() === "live") return Promise.resolve();
    if(Demo.load().classes.FORUM27) return Promise.resolve();
    if(sampleLoading) return sampleLoading;
    sampleLoading = fetch(ROOT + "data/demo-class.json").then(r => r.json()).then(async data => {
      const db = Demo.load(), now = Date.now(), day = today(), c = data.class, code = normCode(c.code), students = {};
      for(const s of data.students) students[normLogin(s.login)] = { login:s.login, pw: await hashPw(code, s.login, s.password), created: now - 30*864e5 };
      db.classes[code] = { code:c.code, name:c.name, level:c.level, created: now - 30*864e5, students, sample:true };
      for(const s of data.students){
        const p = data.progress[s.login], cards = {};
        for(const [k, e] of Object.entries(p.srs.cards)) cards[k] = { ...e, t: day + e.t, d: day + e.d };
        const events = p.events.map(e => { const { ago, ...rest } = e; return { ...rest, t: now - ago * 60000 }; });
        db.progress[Demo.pkey(code, s.login)] = { store:{ srs:{ v:1, cards, newLog:{} } }, events, last: events.length ? events[events.length - 1].t : 0 };
      }
      Demo.save(db);
    }).catch(() => {});
    return sampleLoading;
  }
  function demoLogins(n, taken){
    const pool = NAMES.filter(x => !taken.has(normLogin(x))).sort(() => Math.random() - 0.5), out = [];
    for(let i = 0; out.length < n; i++){
      const base = pool[i % pool.length], name = i < pool.length ? base : base + (Math.floor(i / pool.length) + 1);
      if(!taken.has(normLogin(name))){ out.push(name); taken.add(normLogin(name)); }
    }
    return out;
  }

  /* ---------- session and storage ---------- */
  let session = RAW.get(SESSION, null);
  const SYNCED = k => k === "srs" || k.startsWith("fc:");
  const userPrefix = s => `u:${normCode(s.code)}:${normLogin(s.login)}:`;
  const pendingKey = () => "latin:acct:pending:" + normCode(session.code) + ":" + normLogin(session.login);
  const pending = {
    get(){ return RAW.get(pendingKey(), null) || { keys:{}, events:[] }; },
    put(p){ RAW.set(pendingKey(), p); },
  };

  // While signed in, flashcard storage lives under the student's login, and each change is queued for their account.
  const baseGet = store.get.bind(store), baseSet = store.set.bind(store);
  store.get = (k, f) => (session && SYNCED(k)) ? baseGet(userPrefix(session) + k, f) : baseGet(k, f);
  store.set = (k, v) => {
    if(!(session && SYNCED(k))) return baseSet(k, v);
    baseSet(userPrefix(session) + k, v);
    if(known && mode() === "demo"){ const db = Demo.load(); Demo.student(db, session.code, session.login).store[k] = v; Demo.save(db); flash("Saved to your account"); return; }
    const p = pending.get(); p.keys[k] = 1; pending.put(p); soon();
  };

  function record(kind, data){
    if(!session) return;
    const ev = { id:newId(), t:Date.now(), k:kind, ...(data || {}) };
    if(known && mode() === "demo"){
      const db = Demo.load(), p = Demo.student(db, session.code, session.login);
      p.events.push(ev); if(p.events.length > MAX_EVENTS) p.events.splice(0, p.events.length - MAX_EVENTS);
      p.last = ev.t; Demo.save(db); return;
    }
    const p = pending.get(); p.events.push(ev); pending.put(p); soon();
  }

  /* ---------- live syncing: batched, retried, never lost on page change ---------- */
  let timer = null, flushing = null, signedOutNotice = false;
  const soon = () => { if(!timer) timer = setTimeout(() => { timer = null; flush(); }, SYNC_MS); };
  function payload(){
    const p = pending.get(), set = {};
    for(const k of Object.keys(p.keys)){ const v = baseGet(userPrefix(session) + k, undefined); if(v !== undefined) set[k] = v; }
    return { p, set, events: p.events.slice(0, 500) };
  }
  async function flush(){
    await ready;
    if(!session || mode() !== "live" || !session.token) return;
    if(flushing) return flushing;
    flushing = (async () => {
      const { p, set, events } = payload();
      if(!Object.keys(set).length && !events.length) return;
      const r = await call("sync", { token:session.token, set, events });
      if(r.ok){
        // remove only what was sent; anything queued meanwhile stays for next time
        const now = pending.get(), sentIds = new Set(events.map(e => e.id));
        for(const k of Object.keys(set)) delete now.keys[k];
        now.events = now.events.filter(e => !sentIds.has(e.id));
        pending.put(now);
        flash("Saved to your account");
        if(now.events.length || Object.keys(now.keys).length) soon();
      } else if(r.error === "signed-out"){
        session.token = null; RAW.set(SESSION, session); signedOutNotice = true; drawBar();
      } else soon();   // offline or busy: try again shortly
    })();
    try{ await flushing; } finally { flushing = null; }
  }
  // when the page is hidden or closed, send what's queued; the server ignores anything it has already seen
  function beacon(){
    if(!session || mode() !== "live" || !session.token || !navigator.sendBeacon) return;
    const { set, events } = payload();
    if(!Object.keys(set).length && !events.length) return;
    navigator.sendBeacon(API, new Blob([JSON.stringify({ action:"sync", token:session.token, set, events })], { type:"text/plain;charset=utf-8" }));
  }
  addEventListener("pagehide", beacon);
  document.addEventListener("visibilitychange", () => { if(document.visibilityState === "hidden") beacon(); });
  // anything queued before the config loaded: send it (live), or file it in the demo store (demo)
  ready.then(() => {
    if(!session) return;
    if(mode() === "live"){ flush(); return; }
    const p = pending.get(); if(!p.events.length && !Object.keys(p.keys).length) return;
    const db = Demo.load(), st = Demo.student(db, session.code, session.login);
    for(const k of Object.keys(p.keys)){ const v = baseGet(userPrefix(session) + k, undefined); if(v !== undefined) st.store[k] = v; }
    st.events.push(...p.events); if(st.events.length > MAX_EVENTS) st.events.splice(0, st.events.length - MAX_EVENTS);
    if(p.events.length) st.last = p.events[p.events.length - 1].t;
    Demo.save(db); RAW.del(pendingKey());
  });

  /* ---------- students: sign in, out, and their own data ---------- */
  async function signIn(code, login, pw){
    await ready;
    if(mode() === "demo"){
      await ensureSample();
      const db = Demo.load(), cls = db.classes[normCode(code)];
      if(!cls) return { ok:false, why:"code" };
      const s = cls.students[normLogin(login)];
      if(!s || s.pw !== await hashPw(code, s.login, pw)) return { ok:false, why:"login" };
      startSession({ code:cls.code, login:s.login, cls:cls.name, level:cls.level }, Demo.student(db, cls.code, s.login).store);
      record("login");
      return { ok:true };
    }
    const r = await call("signin", { code, login, pw });
    if(!r.ok) return { ok:false, why: r.error === "code" ? "code" : r.error === "locked" ? "locked" : r.error === "offline" ? "offline" : "login" };
    startSession({ code:r.code, login:r.login, cls:r.cls, level:r.level, token:r.token }, (r.data && r.data.store) || {});
    record("login");
    return { ok:true };
  }
  function startSession(s, saved){
    session = s; RAW.set(SESSION, session); signedOutNotice = false;
    // bring this student's saved progress onto this device
    for(const [k, v] of Object.entries(saved || {})) baseSet(userPrefix(session) + k, v);
  }
  // Signing out sends anything still queued, then removes the student's progress from this device
  // (it stays in their account), so a shared Chromebook stays clean.
  async function signOut(){
    if(!session) return { ok:true };
    if(mode() === "live" && session.token){
      await flush();
      const left = pending.get();
      if(left.events.length || Object.keys(left.keys).length) return { ok:false, why:"unsaved" };
    }
    const pre = "latin:" + userPrefix(session);
    for(const k of RAW.keys()) if(k.startsWith(pre)) RAW.del(k);
    RAW.del(pendingKey());
    session = null; RAW.del(SESSION);
    return { ok:true };
  }
  // the signed-in student's progress, for their own page
  async function myData(){
    await ready; await titlesReady;
    if(!session) return null;
    if(mode() === "demo") return Demo.student(Demo.load(), session.code, session.login);
    await flush();
    const r = session.token ? await call("me", { token:session.token }) : { ok:false };
    const local = { srs: baseGet(userPrefix(session) + "srs", null) };
    const data = r.ok ? r.data : { store:{}, events:[] };
    if(local.srs) data.store.srs = local.srs;                      // this device's copy is the freshest
    data.events = (data.events || []).concat(pending.get().events);
    return data;
  }

  /* ---------- teacher ---------- */
  let tToken = RAW.get(TEACHER, null);
  if(tToken && tToken.e < Date.now()) tToken = null;
  const teacher = {
    async needsLogin(){ await ready; return mode() === "live" && !tToken; },
    async login(pw){
      await ready;
      const r = await call("teacherLogin", { pw });
      if(!r.ok) return { ok:false, why:r.error };
      tToken = { t:r.token, e: Date.now() + 6.5 * 864e5 }; RAW.set(TEACHER, tToken);
      return { ok:true };
    },
    logout(){ tToken = null; RAW.del(TEACHER); },
    // every call returns { ok, ... }; a "signed-out" error means the teacher must sign in again
    async run(action, body){
      const r = await call(action, { token: tToken && tToken.t, ...body });
      if(!r.ok && r.error === "signed-out") teacher.logout();
      return r;
    },
    async classes(){
      await ready; await titlesReady;
      if(mode() === "demo"){
        await ensureSample();
        return { ok:true, classes: Object.values(Demo.load().classes).map(c => ({ code:c.code, name:c.name, level:c.level, students:Object.keys(c.students).length, sample:!!c.sample })) };
      }
      return teacher.run("classes", {});
    },
    // { cls:{ code, name, level, students:[logins] }, progress:{ login: { store, events } } }
    async classData(code){
      if(mode() === "demo"){
        const db = Demo.load(), c = db.classes[normCode(code)]; if(!c) return { ok:false, error:"code" };
        const students = Object.values(c.students).map(s => s.login), progress = {};
        for(const l of students) progress[l] = db.progress[Demo.pkey(code, l)] || { store:{}, events:[] };
        return { ok:true, cls:{ code:c.code, name:c.name, level:c.level, students, sample:!!c.sample }, progress };
      }
      return teacher.run("classData", { code });
    },
    async createClass(name, level, n){
      if(mode() === "live") return teacher.run("createClass", { name, level, n });
      const db = Demo.load();
      let code; do { code = pick(CODE_WORDS) + "-" + (10 + Math.floor(Math.random() * 90)); } while(db.classes[normCode(code)]);
      db.classes[normCode(code)] = { code, name, level, created:Date.now(), students:{} }; Demo.save(db);
      const r = await teacher.addStudents(code, n);
      return { ok:true, code, roster:r.roster };
    },
    async addStudents(code, n){
      if(mode() === "live") return teacher.run("addStudents", { code, n });
      const db = Demo.load(), cls = db.classes[normCode(code)]; if(!cls) return { ok:false, error:"code" };
      const roster = [], used = new Set();
      for(const login of demoLogins(n, new Set(Object.keys(cls.students)))){
        const password = freshPassword(used);
        roster.push({ login, password });
        cls.students[normLogin(login)] = { login, pw: await hashPw(code, login, password), created: Date.now() };
      }
      Demo.save(db); return { ok:true, roster };
    },
    async resetPassword(code, login){
      if(mode() === "live") return teacher.run("resetPassword", { code, login });
      const db = Demo.load(), cls = db.classes[normCode(code)], s = cls && cls.students[normLogin(login)]; if(!s) return { ok:false };
      const password = freshPassword(new Set());
      s.pw = await hashPw(code, s.login, password); Demo.save(db);
      return { ok:true, password };
    },
    async deleteClass(code){
      const labelsAll = RAW.get(LABELS, {}); delete labelsAll[normCode(code)]; RAW.set(LABELS, labelsAll);
      if(mode() === "live") return teacher.run("deleteClass", { code });
      const db = Demo.load(), k = normCode(code);
      delete db.classes[k];
      for(const p of Object.keys(db.progress)) if(p.startsWith(k + "/")) delete db.progress[p];
      Demo.save(db); return { ok:true };
    },
  };
  // Real names typed by the teacher stay in this browser only; they are never sent anywhere.
  const labels = {
    get(code){ return RAW.get(LABELS, {})[normCode(code)] || {}; },
    set(code, login, text){ const all = RAW.get(LABELS, {}), k = normCode(code); all[k] = all[k] || {}; if(text) all[k][normLogin(login)] = text; else delete all[k][normLogin(login)]; RAW.set(LABELS, all); },
  };

  /* ---------- what gets recorded ---------- */
  document.addEventListener("latin:review", e => { const d = e.detail; record("card", { d:d.deck, c:d.key, la:d.la, g:d.grade }); });
  document.addEventListener("latin:mark", e => { const d = e.detail; record("mark", { d:d.deck, c:d.key, la:d.la, v:!!d.known }); });
  // games call Site.account.record("game", { g:id, title, s:score, of:outOf })
  // grammar pages count as visited once per page load
  if(session && /\/grammar\/[^/]+\.html$/.test(location.pathname) && !/\/index\.html$/.test(location.pathname)){
    record("page", { p: "grammar/" + location.pathname.split("/").pop().replace(/\.html$/, ""), title: document.title });
  }

  /* ---------- summaries (teacher dashboard and the student's own page) ---------- */
  const DAY_MS = 864e5;
  function summarize(p){
    p = p || { store:{}, events:[] };
    const now = Date.now(), d0 = today(), ev = (p.events || []).slice().sort((a, b) => a.t - b.t);
    const srs = (p.store && p.store.srs && p.store.srs.cards) || {};
    const byDeck = {};
    let learned = 0, due = 0;
    for(const [k, e] of Object.entries(srs)){
      const deck = k.split(":")[0], b = byDeck[deck] || (byDeck[deck] = { seen:0, learned:0, due:0 });
      b.seen++;
      if(e.s === "r" && e.i >= 7){ learned++; b.learned++; }
      if(e.s === "l" || e.d <= d0){ due++; b.due++; }
    }
    const act = ev.filter(e => e.k !== "login");
    const days = new Set(act.map(e => dayOf(e.t)));
    const strip = Array.from({ length:28 }, (_, i) => { const d = d0 - 27 + i; return act.filter(e => dayOf(e.t) === d).length; });
    const week = ev.filter(e => now - e.t < 7 * DAY_MS);
    const answered = ev.filter(e => e.k === "card" || e.k === "mark");
    const right = answered.filter(e => e.k === "card" ? e.g >= 2 : e.v).length;   // Hard still counts as remembered
    const misses = {};
    for(const e of answered) if(e.k === "card" ? e.g === 1 : !e.v){ const m = misses[e.c] || (misses[e.c] = { la:e.la, deck:e.d, n:0 }); m.n++; }
    const pages = {};
    for(const e of ev) if(e.k === "page"){ const x = pages[e.p] || (pages[e.p] = { title:e.title, n:0, last:0 }); x.n++; x.last = Math.max(x.last, e.t); }
    const games = {};
    for(const e of ev) if(e.k === "game"){ const g = games[e.g] || (games[e.g] = { title:e.title, best:0, of:e.of, plays:0, last:0 }); g.plays++; g.best = Math.max(g.best, e.s); g.last = Math.max(g.last, e.t); }
    const last = act.length ? act[act.length - 1].t : 0;
    const flags = [];
    if(!ev.length) flags.push("Has not signed in yet");
    else if(!last || now - last > 7 * DAY_MS) flags.push("No practice in 7+ days");
    if(due > 40) flags.push(`${due} cards overdue`);
    if(answered.length >= 30 && right / answered.length < 0.7) flags.push("Missing many cards");
    return {
      last, daysActive14: [...days].filter(d => d > d0 - 14).length, strip,
      learned, due, seen: Object.keys(srs).length, byDeck,
      reviewsWeek: week.filter(e => e.k === "card" || e.k === "mark").length,
      accuracy: answered.length ? right / answered.length : null,
      missed: Object.entries(misses).map(([c, m]) => ({ c, ...m })).sort((a, b) => b.n - a.n),
      pages, games, flags, events: ev,
    };
  }

  /* ---------- the status line on site pages ---------- */
  let flashTimer = null;
  function flash(text){
    const el = document.getElementById("acct-saved"); if(!el) return;
    el.textContent = text; el.hidden = false;
    clearTimeout(flashTimer); flashTimer = setTimeout(() => { el.hidden = true; }, 2500);
  }
  function drawBar(){
    if(document.body.dataset.acct === "page") return;            // the account pages draw their own
    const host = document.querySelector(".wrap"); if(!host) return;
    let bar = host.querySelector(":scope > .acct-bar");
    if(!bar){ bar = document.createElement("div"); bar.className = "acct-bar"; host.prepend(bar); }
    const acct = ROOT + "account/";
    bar.innerHTML = !session
      ? `<a href="${acct}">Sign in</a><span>to save your flashcard progress to your account.</span>`
      : signedOutNotice || (mode() === "live" && !session.token)
        ? `<span>Signed in as <b>${esc(session.login)}</b>, but your sign-in has expired.</span><a href="${acct}">Sign in again</a><span>Your progress is kept on this computer until you do.</span>`
        : `<span>Signed in as <b>${esc(session.login)}</b> · ${esc(session.cls)}</span><span class="acct-saved" id="acct-saved" role="status" hidden></span><a href="${acct}">Your progress</a>`;
    const note = [...document.querySelectorAll("#srs-panel p")].find(p => /saved in this browser only|saved to your account/.test(p.textContent));
    if(note && session) note.innerHTML = note.innerHTML.replace("Your progress is saved in this browser only.", "Your progress is saved to your account, so it follows you to any computer you sign in on.");
  }
  const css = document.createElement("style");
  css.textContent = `.acct-bar{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;justify-content:flex-end;font-size:1rem;color:var(--muted);margin:0 0 8px}
.acct-bar a{color:var(--accent);font-weight:600}
.acct-saved{color:var(--good,#1E6B3A)}`;
  document.head.append(css);
  ready.then(() => { if(document.readyState === "loading") document.addEventListener("DOMContentLoaded", drawBar); else drawBar(); });

  Site.account = {
    ready, get mode(){ return mode(); }, get session(){ return session; },
    signIn, signOut, myData, record, flush, ensureSample, teacher, labels,
    summarize, deckTitle, today, dayOf, normCode, normLogin,
  };
})();
