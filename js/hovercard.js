/* Form inspector, two ways (Oct 2026).
   Mouse (desktop): the inspector (#card) floats beside the pointer while it is over a form, so the charts get the
   full width and nothing is covered. Keyboard focus shows it beside the focused form; Esc hides it.
   Touch (phones, tablets) and windows under 700px: the inspector is a bottom sheet that appears only after a form is
   tapped, with the full details (translation, breakdown, look-alikes, patterns). Tap the same form again, tap outside
   the charts, or press the close button to dismiss it. The page gets bottom space while the
   sheet is up, so the last chart can scroll above it, and the tapped form is scrolled clear of it. Dragging on the
   sheet scrolls the page unless the sheet has more of its own to scroll.
   The pattern notes (#pcard) sit in the sidebar (wide screens) or above the charts (everything else).
   Load after the page's own script and pattern-notes.js. Its styles are here so the pages need one script tag. */
(function(){
  const card = document.getElementById("card"), panel = card && card.closest(".panel");
  if(!panel) return;
  const mq = matchMedia("(hover:hover) and (pointer:fine) and (min-width:700px)"), root = document.documentElement;
  const css = document.createElement("style");
  css.textContent = `
/* mouse: floating card */
html.hovercard .work{grid-template-columns:minmax(0,1fr);grid-template-areas:"panel" "charts";gap:0}
html.hovercard .panel{position:static}
html.hovercard .panel:has(.pcard:not([hidden])){margin-bottom:20px}
html.hovercard #card{position:fixed;z-index:60;width:min(400px,calc(100vw - 24px));height:auto;max-height:calc(100vh - 16px);overflow:hidden;
  pointer-events:none;box-shadow:0 14px 44px rgba(40,30,20,.3);display:none;top:0;left:0}
html.hovercard #card.hc-on:not([hidden]){display:grid}
.sh-bar,.sh-hint{display:none}
/* touch: bottom sheet that appears on tap */
html.sheet .work{grid-template-columns:minmax(0,1fr);grid-template-areas:"charts";gap:0}
html.sheet .panel{position:fixed;top:auto;left:0;right:0;bottom:calc(env(safe-area-inset-bottom,0px) + 8px);margin:0 auto;z-index:60;display:none;
  width:min(640px,calc(100% - 16px));background:var(--surface);border:1px solid var(--rule2);border-radius:16px;box-shadow:0 -8px 30px rgba(40,30,20,.28);overflow:hidden}
html.sheet .panel.sh-on{display:block}
html.sheet .sh-bar{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:2px 6px 0}
html.sheet .sh-bar button{min-width:44px;height:44px;border:0;background:none;font:inherit;font-size:1.25rem;color:var(--ink);cursor:pointer;border-radius:10px}
html.sheet .sh-bar .sh-sp{width:44px}
html.sheet .sh-grab{width:40px;height:5px;border-radius:3px;background:var(--rule2);opacity:.7}
html.sheet #card{height:auto;border:0;border-radius:0;box-shadow:none;background:none;padding:0 16px 14px;gap:8px;overscroll-behavior:auto;touch-action:pan-y}
html.sheet #card{max-height:min(55vh,520px);overflow:auto}
html.sheet #card .form{font-size:2rem;line-height:1.3}
html.sheet #card[hidden]{display:none}
html.sheet #pcard{height:auto;max-height:none;overflow:visible;text-align:left;box-shadow:none;margin:0 0 16px}
html.sheet .sh-hint{display:block;margin:0 0 12px;color:var(--muted);font-size:1rem}
html.sheet.sh-live body{padding-bottom:calc(var(--sh-h,0px) + 24px)}`;
  document.head.appendChild(css);

  const cellOf = n => n && n.closest ? n.closest(".cell") : null;
  const idle = () => { const p = card.querySelector(".parse"); return !p || /^Inspect an? /.test(p.textContent.trim()); };

  /* ---------- mouse ---------- */
  let x = 0, y = 0, on = false, raf = 0;
  function place(){
    raf = 0; if(!on) return;
    const w = card.offsetWidth, h = card.offsetHeight, gap = 18, m = 8, vw = innerWidth, vh = innerHeight;
    let left = x + gap, top = y + gap;
    if(left + w > vw - m) left = x - gap - w;          // no room on the right: go to the left of the pointer
    if(top + h > vh - m) top = y - gap - h;            // no room below: go above
    left = Math.min(Math.max(m, left), Math.max(m, vw - m - w));
    top = Math.min(Math.max(m, top), Math.max(m, vh - m - h));
    card.style.left = left + "px"; card.style.top = top + "px";
  }
  const schedule = () => { if(!raf) raf = requestAnimationFrame(place); };
  const show = () => { on = true; card.classList.add("hc-on"); schedule(); };
  const hide = () => { on = false; card.classList.remove("hc-on"); };
  const hovering = () => mq.matches;
  document.addEventListener("mouseover", e => { if(hovering() && cellOf(e.target)){ x = e.clientX; y = e.clientY; show(); } });
  document.addEventListener("mousemove", e => { if(on){ x = e.clientX; y = e.clientY; schedule(); } });
  document.addEventListener("mouseout", e => { if(cellOf(e.target) && !cellOf(e.relatedTarget)) hide(); });
  document.addEventListener("focusin", e => { const c = cellOf(e.target); if(hovering() && c){ const r = c.getBoundingClientRect(); x = r.left + r.width / 2; y = r.bottom - 6; show(); } });
  document.addEventListener("focusout", e => { if(cellOf(e.target)) hide(); });
  window.addEventListener("scroll", () => { if(on) place(); }, { passive: true });

  /* ---------- touch: bottom sheet ---------- */
  const bar = document.createElement("div"); bar.className = "sh-bar";
  bar.innerHTML = `<span class="sh-sp" aria-hidden="true"></span><span class="sh-grab" aria-hidden="true"></span><button type="button" class="sh-x" aria-label="Close inspector">✕</button>`;
  panel.prepend(bar);
  const hint = document.createElement("p"); hint.className = "sh-hint"; hint.textContent = "Tap a form in the charts to see what it is and how it is built.";
  let key = null, lastCell = null;
  const sheetMode = () => !mq.matches;
  function closeSheet(){ key = null; document.body.dispatchEvent(new MouseEvent("click", { bubbles: true })); }   // the page's own outside-click clears the selection
  bar.querySelector(".sh-x").onclick = closeSheet;
  panel.addEventListener("click", e => e.stopPropagation());   // a tap inside the sheet is not an "outside" tap (the page would clear the selection)
  document.addEventListener("keydown", e => { if(e.key === "Escape"){ hide(); if(sheetMode() && panel.classList.contains("sh-on")) closeSheet(); } });
  const ro = "ResizeObserver" in window ? new ResizeObserver(() => root.style.setProperty("--sh-h", (panel.classList.contains("sh-on") ? panel.offsetHeight : 0) + "px")) : null;
  if(ro) ro.observe(panel);
  function sync(){
    const live = sheetMode() && !idle() && !card.hidden;
    panel.classList.toggle("sh-on", live); root.classList.toggle("sh-live", live);
    if(!live) key = null;
    root.style.setProperty("--sh-h", (live ? panel.offsetHeight : 0) + "px");
  }
  new MutationObserver(sync).observe(card, { childList: true, subtree: true, attributes: true, attributeFilter: ["hidden"] });
  // In the sheet layout a form is chosen by click or tap only (Enter or Space from the keyboard). The page's own code also
  // selects on hover and focus and clears on mouse-leave and blur. On a touch screen the sheet would then open under the
  // finger before it lifts, and the tap would land on the sheet; with a mouse it would close before the pointer reached its buttons.
  ["mouseenter", "mouseleave", "focus", "blur"].forEach(t => window.addEventListener(t, e => {
    if(sheetMode() && e.target && e.target.classList && e.target.classList.contains("cell")) e.stopImmediatePropagation();
  }, true));
  // a tap on a form: the same form again closes; otherwise keep it visible above the sheet
  document.addEventListener("click", e => {
    if(!sheetMode()) return;
    const c = cellOf(e.target); if(!c) return;
    if(panel.classList.contains("sh-on") && key === c.dataset.k){ setTimeout(closeSheet); return; }
    key = c.dataset.k; lastCell = c;
    requestAnimationFrame(() => requestAnimationFrame(() => {
      if(!panel.classList.contains("sh-on")) return;
      const r = c.getBoundingClientRect(), top = panel.getBoundingClientRect().top;
      if(r.bottom > top - 12) window.scrollBy({ top: r.bottom - top + 28, behavior: "smooth" });
    }));
  }, true);

  /* ---------- phones: start with the English translations showing (verb pages' "Show English") ---------- */
  // A choice the student makes is remembered in this browser and wins over the default.
  const en = document.getElementById("t-en");
  if(en){
    let saved = null; try{ saved = localStorage.getItem("gram:en"); }catch(e){}
    if((saved === null ? sheetMode() : saved === "1") && en.getAttribute("aria-pressed") !== "true") en.click();
    en.addEventListener("click", e => { if(e.isTrusted) try{ localStorage.setItem("gram:en", en.getAttribute("aria-pressed") === "true" ? "1" : "0"); }catch(_){} });
  }

  /* ---------- mode: where the pattern notes and the hint live ---------- */
  function mode(){
    const hv = mq.matches, pc = document.getElementById("pcard"), work = document.querySelector(".work");
    root.classList.toggle("hovercard", hv); root.classList.toggle("sheet", !hv);
    if(hv){ hide(); hint.remove(); if(pc && !pc.closest("#sb-tools") && pc.parentElement !== panel) panel.prepend(pc); }
    else if(work){
      if(pc && !pc.closest("#sb-tools") && pc.parentElement !== work.parentElement) work.before(pc);
      work.before(hint);
    }
    sync();
  }
  mq.addEventListener("change", mode); mode();
})();
