/* A list of pages grouped under headings, read from a JSON file, with the level switcher above it.
   Used by games/index.html (data/games.json) and grammar/index.html (data/grammar.json).
   Each entry: { page, title, group, about, topic }; groups appear in the order they first occur.
   topic (games): the grammar the game practises, shown above its name.
   Levels come from data/levels.json (see js/levels.js). */
(async function(){
  const { $, esc, loadJSON, levels } = window.Site;
  const lsw = $("level-switch"), box = $("page-list"), src = box.dataset.src, what = box.dataset.what || "pages", section = box.dataset.section;
  let items;
  try{ [items] = await Promise.all([loadJSON(src), levels.load("../")]); }
  catch(e){ box.innerHTML = `<p class="callout">Couldn't load the list of ${esc(what)}. (${esc(e.message)})</p>`; return; }
  function entry(g){ return levels.data && levels.data[section] && levels.data[section][g.page]; }
  function levelOf(g){ const e = entry(g); return typeof e === "number" ? e : e && e.level; }
  function alsoAt(g, lv){ const e = entry(g); return !!(e && e.also && e.also.indexOf(lv) >= 0); }   // a game listed under another level too: "also": [2]
  function draw(){   // games: only the chosen level's own games (not the earlier years too), plus any listed there with "also"
    const groups = new Map();
    const names = (levels.data && levels.data.levels) || [];
    const games = section === "games" && levels.current;
    items.filter(g => games && levelOf(g) ? levelOf(g) === levels.current || alsoAt(g, levels.current) : levels.shows(section, [g.page])).forEach(g => { const name = games && alsoAt(g, levels.current) ? names[levels.current - 1] || g.group : g.group; if(!groups.has(name)) groups.set(name, []); groups.get(name).push(g); });
    const jump = box.parentElement.querySelector(".level-switch");
    if(jump){ const old = jump.querySelector(".pl-jump"); if(old) old.remove();
      if(groups.size > 1){ const n = document.createElement("nav"); n.className = "pl-jump"; n.setAttribute("aria-label", "Sections");
        n.innerHTML = [...groups].map(([name, gs], i) => `<a href="#pl-${i}">${esc(name)} <span>${gs.length}</span></a>`).join(""); jump.append(n); } }
    if(!groups.size){ box.innerHTML = `<p class="level-empty">No ${esc(what)} for this level yet.</p>`; return; }
    box.innerHTML = [...groups].map(([group, gs], i) => {
      let out = `<section class="pl-sec" id="pl-${i}"><h2 class="pl-h">${esc(group)} <span>${gs.length} ${gs.length === 1 ? "page" : "pages"}</span></h2>`, cur = null, open = false;
      gs.forEach(g => {
        const sub = (g.path || []).slice(1).join(" \u203a ");
        if(!open || sub !== cur){ if(open) out += "</ul>"; if(sub) out += `<h3 class="pl-sub">${esc(sub)}</h3>`; out += `<ul class="pl-rows${!sub && cur !== null ? " pl-after" : ""}">`; open = true; cur = sub; }
        const lv = lsw && !levels.current && levelOf(g);
        out += `<li><a class="pl-row" href="${encodeURIComponent(g.page)}.html">${g.topic ? `<span class="tp">${esc(g.topic)}</span>` : ""}<span class="t">${esc(g.title)}</span>${g.about ? `<span class="n">${esc(g.about)}</span>` : ""}${lv ? `<span class="lv">${esc(names[lv - 1] || "")}</span>` : ""}</a></li>`;
      });
      return out + (open ? "</ul>" : "") + `</section>`;
    }).join("");
  }
  if(lsw) levels.render(lsw, draw); else window.addEventListener("site:level", draw);   // no switcher on the games page: it still follows the chosen level (?level=2, or the level kept from another list)
  draw();
})();
