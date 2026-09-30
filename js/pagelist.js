/* A list of pages grouped under headings, read from a JSON file.
   Used by games/index.html (data/games.json) and grammar/index.html (data/grammar.json).
   Each entry: { page, title, group, about }; groups appear in the order they first occur. */
(async function(){
  const { $, esc, loadJSON } = window.Site;
  const box = $("page-list"), src = box.dataset.src, what = box.dataset.what || "pages";
  try{
    const items = await loadJSON(src), groups = {};
    items.forEach(g => (groups[g.group] = groups[g.group] || []).push(g));
    box.innerHTML = Object.entries(groups).map(([group, gs]) =>
      `<h2 class="label deck-group">${esc(group)}</h2><ul class="deck-list game-list">` +
      gs.map(g => `<li><a class="panel" href="${encodeURIComponent(g.page)}.html"><span class="t">${esc(g.title)}</span><span class="n">${esc(g.about)}</span></a></li>`).join("") +
      `</ul>`).join("");
  }catch(e){ box.innerHTML = `<p class="callout">Couldn't load the list of ${esc(what)}. (${esc(e.message)})</p>`; }
})();
