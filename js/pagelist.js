/* A list of pages grouped under headings, read from a JSON file, with the level switcher above it.
   Used by games/index.html (data/games.json) and grammar/index.html (data/grammar.json).
   Each entry: { page, title, group, about }; groups appear in the order they first occur.
   Levels come from data/levels.json (see js/levels.js). */
(async function(){
  const { $, esc, loadJSON, levels } = window.Site;
  const lsw = $("level-switch"), box = $("page-list"), src = box.dataset.src, what = box.dataset.what || "pages", section = box.dataset.section;
  let items;
  try{ [items] = await Promise.all([loadJSON(src), levels.load("../")]); }
  catch(e){ box.innerHTML = `<p class="callout">Couldn't load the list of ${esc(what)}. (${esc(e.message)})</p>`; return; }
  function levelOf(g){ const e = levels.data && levels.data[section] && levels.data[section][g.page]; return typeof e === "number" ? e : e && e.level; }
  function draw(){   // games: only the chosen level's own games (not the earlier years too)
    const groups = new Map();
    items.filter(g => section === "games" && levels.current && levelOf(g) ? levelOf(g) === levels.current : levels.shows(section, [g.page])).forEach(g => { if(!groups.has(g.group)) groups.set(g.group, []); groups.get(g.group).push(g); });
    const names = (levels.data && levels.data.levels) || [];
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
        out += `<li><a class="pl-row" href="${encodeURIComponent(g.page)}.html"><span class="t">${esc(g.title)}</span>${g.about ? `<span class="n">${esc(g.about)}</span>` : ""}${lv ? `<span class="lv">${esc(names[lv - 1] || "")}</span>` : ""}</a></li>`;
      });
      return out + (open ? "</ul>" : "") + `</section>`;
    }).join("");
  }
  if(lsw) levels.render(lsw, draw); else window.addEventListener("site:level", draw);   // no switcher on the games page: it still follows the chosen level (?level=2, or the level kept from another list)
  draw();
})();
