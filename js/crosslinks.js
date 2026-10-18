/* Flashcards -> grammar links. Each deck links to the one grammar page that lists it in data/grammar.json ("decks"). */
(function(){
  "use strict";
  const { esc, loadJSON, param } = window.Site;
  let pages = null;
  const keyOf = (id, view) => id + (view ? "." + view : "");
  const pageFor = key => pages && pages.find(p => (p.decks || []).includes(key));
  const href = p => "../grammar/" + p.page + ".html";

  function rows(){
    document.querySelectorAll(".deck-list li[data-id]:not([data-gl])").forEach(li => {
      li.dataset.gl = "1";
      const p = pageFor(keyOf(li.dataset.id, li.dataset.view));
      if(!p) return;
      li.classList.add("has-gl");
      li.insertAdjacentHTML("beforeend", `<a class="fc-gl" href="${href(p)}" title="${esc(p.title)}">Grammar page ›</a>`);
    });
  }
  function header(){
    const id = param("deck"); if(!id || document.getElementById("fc-gl-line")) return;
    const p = pageFor(keyOf(id, param("view"))); if(!p) return;
    const sub = document.getElementById("subtitle"); if(!sub) return;
    sub.insertAdjacentHTML("afterend", `<p id="fc-gl-line" class="fc-gl-line">Grammar Reference: <a href="${href(p)}">${esc(p.title)}</a></p>`);
  }
  loadJSON("../data/grammar.json").then(g => {
    pages = g; header(); rows();
    const dg = document.getElementById("deck-groups");
    if(dg) new MutationObserver(rows).observe(dg, { childList:true, subtree:true });
  }).catch(() => {});
})();
