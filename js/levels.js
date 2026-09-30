/* Level switcher for the lists of decks, grammar pages and games.
   Each item's level (where it is first taught) lives in data/levels.json. Levels are cumulative:
   choosing Latin II hides Latin III and IV content.
   The chosen level is remembered in this browser (shared by all three lists);
   a link can set it for one visit with ?level=2 (1 = Latin I … 4 = Latin IV, 0 = all), e.g. to embed
   a Latin II list on the Google Site. */
(function(){
  const { store, param, loadJSON, chip } = window.Site;
  let data = null, level = 0;

  async function load(base){
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
  const shows = (section, keys) => { if(!level) return true; const e = entryOf(section, keys); return !e || e.level <= level; };
  // extra link settings a deck uses at the chosen level (e.g. "mood=ind"), or ""
  const linkExtra = (section, keys) => { const e = level && entryOf(section, keys); return (e && e.links && e.links[level]) || ""; };

  // chips: All levels · Latin I · Latin II …
  function render(box, onChange){
    box.innerHTML = '<span class="label">Level</span>';
    const make = () => {
      box.querySelectorAll(".chip").forEach(c => c.remove());
      ["All levels", ...data.levels].forEach((name, i) => chip(box, name, level === i, () => {
        level = i; store.set("level", i); make(); onChange(level);
      }));
    };
    make();
  }
  window.Site.levels = { load, shows, linkExtra, render, get current(){ return level; } };
})();
