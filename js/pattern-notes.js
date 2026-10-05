/* Pattern notes in the inspector.
   A highlighted pattern's explanation used to sit above the charts and push them down. This moves the
   notes box (#pnotes) into the inspector panel instead: while no form is being inspected, the panel shows
   the notes for the patterns that are on; hovering or tapping a form shows that form as usual, and moving
   off it brings the notes back. Nothing above the charts changes size.
   Works on any grammar page with #pnotes and an .panel > #card inspector; load it after the page's own script. */
(function(){
  const notes = document.getElementById("pnotes"), card = document.getElementById("card");
  const panel = card && card.closest(".panel");
  if(!notes || !panel) return;

  const box = document.createElement("div");
  box.className = "card pcard"; box.id = "pcard";
  box.innerHTML = `<div class="parse">Pattern${""}</div>`;
  const label = box.firstChild;
  notes.replaceWith(document.createComment("pattern notes: in the inspector"));
  box.appendChild(notes);
  const hint = document.createElement("div");
  hint.className = "job pc-hint"; hint.textContent = "Hover over or tap a form to inspect it.";
  box.appendChild(hint);
  panel.prepend(box);

  const idle = () => { const p = card.querySelector(".parse"); return !p || /^Inspect an? /.test(p.textContent.trim()); };
  function update(){
    const n = notes.children.length;
    label.textContent = n > 1 ? "Patterns" : "Pattern";
    const show = n > 0 && idle();
    box.hidden = !show; card.hidden = show;
  }
  new MutationObserver(update).observe(card, { childList: true, subtree: true });
  new MutationObserver(update).observe(notes, { childList: true });
  update();
})();
