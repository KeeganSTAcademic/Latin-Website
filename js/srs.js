/* =========================================================
   Spaced repetition (Anki-style SM-2), stored in this browser.
   Exposed as window.Site.srs. Used by the flashcard player
   (review sessions) and the deck list (due counts, export).

   One entry per card, keyed "deck:hash" (the same history whichever direction it's studied in):
     s  state: "l" learning (seen, not yet graduated) | "r" review
     d  due day (see today())      i  interval in days
     e  ease (starts at 2.5)       r  reviews   l  lapses
     t  last day it was answered
   ========================================================= */
(function(){
  const { store } = window.Site;
  const KEY = "srs";
  const NEW_PER_DAY = 15;          // new cards introduced per deck per day
  const MAX_IVL = 365;

  // Day number in local time; the day rolls over at 4 a.m. (like Anki), so late-night study counts for "today".
  const today = () => { const n = new Date(); n.setHours(n.getHours() - 4); return Math.floor((n.getTime() - n.getTimezoneOffset()*60000) / 864e5); };

  // Stable card id: Latin form + parse, so fixing an English gloss keeps the student's progress.
  function hash(str){ let h = 0x811c9dc5; for(let i=0;i<str.length;i++){ h ^= str.charCodeAt(i); h = Math.imul(h, 0x01000193); } return (h>>>0).toString(36); }
  const cardId = c => c.id || hash([c.la, c.pn, c.tl, c.parse].map(x => x || "").join("|"));
  const key = (deckId, c) => `${deckId}:${cardId(c)}`;

  const newer = (a, b) => !b || (a.t ?? -1) > (b.t ?? -1) || ((a.t ?? -1) === (b.t ?? -1) && a.r > b.r);
  // Early test versions kept one entry per direction ("deck:mode:hash"); fold those into one entry per card.
  function migrate(db){
    for(const k of Object.keys(db.cards)){
      const parts = k.split(":"); if(parts.length !== 3) continue;
      const nk = parts[0] + ":" + parts[2], e = db.cards[k]; delete db.cards[k];
      if(newer(e, db.cards[nk])) db.cards[nk] = e;
    }
    for(const k of Object.keys(db.newLog || {})) if(k.includes(":")) delete db.newLog[k];
    return db;
  }
  const load = () => { const db = store.get(KEY, null); return db && db.cards ? migrate(db) : { v:1, cards:{}, newLog:{} }; };
  const save = db => store.set(KEY, db);

  const isDue = (e, day) => !!e && (e.s === "l" || e.d <= day);

  /* Grade 1 Again · 2 Hard · 3 Good · 4 Easy.
     Returns the new entry and whether the card comes back later in this session. */
  function answer(e, grade, day){
    e = e ? { ...e } : { s:"l", i:0, e:2.5, r:0, l:0, fresh:true };
    const wasNew = !!e.fresh; delete e.fresh;
    e.r++; e.t = day;
    if(e.s === "l"){                                  // new, or relearning after a lapse
      if(grade <= 2) return { entry:{ ...e, d:day }, again:true, wasNew };
      e.s = "r";
      e.i = grade === 4 ? (e.lapsed ? 2 : 4) : 1;
      delete e.lapsed;
    } else {                                          // a graduated card
      if(grade === 1){
        e.l++; e.e = Math.max(1.3, e.e - 0.2); e.s = "l"; e.lapsed = true; e.i = 1;
        return { entry:{ ...e, d:day }, again:true, wasNew };
      }
      // as in Anki, each button always gives a longer interval than the one before it
      const hard = Math.max(e.i + 1, Math.round(e.i * 1.2));
      const good = Math.max(hard + 1, Math.round(e.i * e.e));
      const easy = Math.max(good + 1, Math.round(e.i * e.e * 1.3));
      if(grade === 2){ e.e = Math.max(1.3, e.e - 0.15); e.i = hard; }
      if(grade === 3){ e.i = good; }
      if(grade === 4){ e.e += 0.15; e.i = easy; }
    }
    e.i = Math.min(e.i, MAX_IVL); e.e = Math.round(e.e * 100) / 100; e.d = day + e.i;
    return { entry:e, again:false, wasNew };
  }

  // What each button would do, for the labels under Again / Hard / Good / Easy
  function preview(e, day){
    return [1,2,3,4].map(g => { const r = answer(e, g, day); return r.again ? "soon" : describe(r.entry.i); });
  }
  const describe = n => n < 1 ? "soon" : n === 1 ? "1 day" : n < 60 ? `${n} days` : n < 365 ? `${+(n/30).toFixed(1)} mo` : `${+(n/365).toFixed(1)} yr`;

  // New cards introduced today for this deck + direction
  function newLeft(db, slot, day){
    const log = db.newLog[slot];
    return NEW_PER_DAY - (log && log.day === day ? log.n : 0);
  }
  function countNew(db, slot, day){
    const log = db.newLog[slot];
    db.newLog[slot] = { day, n: (log && log.day === day ? log.n : 0) + 1 };
  }

  /* Export / import. The file is plain JSON so a teacher could inspect it. */
  function exportText(){ return JSON.stringify({ app:"latin-flashcards", v:1, exported:new Date().toISOString(), srs:load() }); }
  function importText(text){
    const data = JSON.parse(text), incoming = data && data.srs && data.srs.cards;
    if(!incoming) throw new Error("That file doesn't contain flashcard progress.");
    const db = load(); let added = 0, updated = 0;
    for(const [k, e] of Object.entries(incoming)){
      const cur = db.cards[k];
      // keep whichever copy was studied more recently (then whichever has more reviews)
      if(!cur){ db.cards[k] = e; added++; }
      else if(newer(e, cur)){ db.cards[k] = e; updated++; }
    }
    save(migrate(db)); return { added, updated };
  }
  function reset(){ save({ v:1, cards:{}, newLog:{} }); }

  window.Site.srs = { NEW_PER_DAY, today, key, cardId, load, save, isDue, answer, preview, newLeft, countNew, exportText, importText, reset };
})();
