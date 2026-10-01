/* Level switcher for the lists of decks, grammar pages and games.
   Each item's level (where it is first taught) lives in data/levels.json. Levels are cumulative:
   choosing Latin II hides Latin III and IV content.
   The chosen level is remembered in this browser (shared by all three lists);
   a link can set it for one visit with ?level=2 (1 = Latin I … 4 = Latin IV, 0 = all), e.g. to embed
   a Latin II list on the Google Site.
   Choosing a level also shows that level's banner painting across the top of the page (data/levels.json
   "banners"), like the Google Site's level pages. No banner for All levels, or when the page is embedded
   in another site (the Google Site already has one), unless the link adds ?banner=1. */
(function(){
  const { store, param, loadJSON, chip, esc } = window.Site;
  let data = null, level = 0, root = "";
  let embedded = false; try{ embedded = window.self !== window.top; }catch(e){ embedded = true; }
  const bannersOn = param("banner") === "1" || (param("banner") !== "0" && !embedded);

  async function load(base){
    root = base;
    try{ data = await loadJSON(base + "data/levels.json"); }catch(e){ data = { levels:[], flashcards:{}, grammar:{}, games:{} }; }
    const q = param("level");
    level = q !== null && /^[0-4]$/.test(q) ? +q : store.get("level", 0);
    if(level > data.levels.length) level = 0;
    return data;
  }
  // an item's entry: the most specific key first (deck/view, then deck); undefined = every level
  function entryOf(section, keys){
    const map = (data && data[section]) || {};
    for(const k of keys) if(k && map[k] !== undefined) return typeof map[k] === "number" ? { level: map[k] } : map[k];
  }
  // levels are cumulative: Latin II shows everything first taught in Latin I or II
  // ("only": true = that level alone, e.g. a year's vocabulary list)
  const shows = (section, keys) => { if(!level) return true; const e = entryOf(section, keys); return !e || (e.only ? e.level === level : e.level <= level); };
  // extra link settings a deck uses at the chosen level (e.g. "mood=ind"), or ""
  const linkExtra = (section, keys) => { const e = level && entryOf(section, keys); return (e && e.links && e.links[level]) || ""; };

  // full-width banner for the chosen level, inserted at the top of <body>
  function banner(){
    if(!bannersOn) return;
    let el = document.getElementById("level-banner");
    const b = level && data.banners && data.banners[level - 1];
    if(!b){ if(el) el.hidden = true; return; }
    if(!el){ el = document.createElement("div"); el.id = "level-banner"; el.className = "level-banner"; document.body.prepend(el); }
    const src = root + "img/banners/" + encodeURIComponent(b.file);
    el.hidden = false;
    el.innerHTML = `<img src="${src}.webp" srcset="${src}-800.webp 800w, ${src}.webp 1600w" sizes="100vw" alt="" title="${esc(b.credit || "")}" style="--focus:${esc(b.focus || "50% 50%")}">` +
      `<p class="level-banner-title">${esc(data.levels[level - 1])}</p>`;
  }

  // chips: All levels · Latin I · Latin II …
  function render(box, onChange){
    box.innerHTML = '<span class="label">Level</span>';
    const make = () => {
      box.querySelectorAll(".chip").forEach(c => c.remove());
      ["All levels", ...data.levels].forEach((name, i) => chip(box, name, level === i, () => {
        level = i; store.set("level", i); make(); banner(); onChange(level);
      }));
    };
    make();
    banner();
  }
  window.Site.levels = { load, shows, linkExtra, render, get current(){ return level; } };
})();
