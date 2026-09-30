/* A list of pages grouped under headings, read from a JSON file, with the level switcher above it.
   Used by games/index.html (data/games.json) and grammar/index.html (data/grammar.json).
   Each entry: { page, title, group, about }; groups appear in the order they first occur.
   Levels come from data/levels.json (see js/levels.js). */
(async function(){
  const { $, esc, loadJSON, levels } = window.Site;
  const box = $("page-list"), src = box.dataset.src, what = box.dataset.what || "pages", section = box.dataset.section;
  let items;
  try{ [items] = await Promise.all([loadJSON(src), levels.load("../")]); }
  catch(e){ box.innerHTML = `<p class="callout">Couldn't load the list of ${esc(what)}. (${esc(e.message)})</p>`; return; }
  function draw(){
    const groups = {};
    items.filter(g => levels.shows(section, [g.page])).forEach(g => (groups[g.group] = groups[g.group] || []).push(g));
    box.innerHTML = Object.keys(groups).length ? Object.entries(groups).map(([group, gs]) =>
      `<h2 class="label deck-group">${esc(group)}</h2><ul class="deck-list game-list">` +
      gs.map(g => `<li><a class="panel" href="${encodeURIComponent(g.page)}.html"><span class="t">${esc(g.title)}</span><span class="n">${esc(g.about)}</span></a></li>`).join("") +
      `</ul>`).join("") : `<p class="level-empty">No ${esc(what)} for this level yet.</p>`;
  }
  levels.render($("level-switch"), draw);
  draw();
})();
