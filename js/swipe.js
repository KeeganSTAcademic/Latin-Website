/* Swipe to answer: drag the card left, right, up or down.
   It presses the same buttons the page already has, so scoring and spaced repetition are unchanged.
   Practice (after flipping): right = Got it, left = Still learning.
   Spaced repetition (after flipping): left = Again, down = Hard, up = Good, right = Easy. */
(function(){
  "use strict";
  const { store } = window.Site;
  const $ = id => document.getElementById(id), card = $("card");
  if(!card) return;
  const stage = card.parentElement;
  const NEED = 80, TAP = 10;
  let sx, sy, dx = 0, dy = 0, drag = false, down = false, moved = false, pid = null;

  const state = () => {
    if($("stage").hidden || ($("done") && !$("done").hidden)) return null;
    const practice = !$("nav-practice").hidden, flipped = card.classList.contains("flipped");
    return { practice, flipped };
  };
  // direction -> { id of the button to press, label, colour class }
  function action(dir, s){
    if(!s.flipped) return null;
    if(s.practice) return dir === "r" ? { b:"knew", t:"Got it", c:"good" } : dir === "l" ? { b:"again", t:"Still learning", c:"bad" } : null;
    return { l:{ b:"grade1", t:"Again", c:"bad", n:"g1" }, d:{ b:"grade2", t:"Hard", c:"hard", n:"g2" },
             r:{ b:"grade4", t:"Easy", c:"easy", n:"g4" }, u:{ b:"grade3", t:"Good", c:"good", n:"g3" } }[dir];
  }
  const dirOf = (x, y) => Math.abs(x) >= Math.abs(y) ? (x > 0 ? "r" : "l") : (y > 0 ? "d" : "u");

  const tag = document.createElement("div"); tag.className = "sw-tag"; tag.hidden = true; tag.setAttribute("aria-hidden", "true");
  stage.append(tag);
  stage.classList.add("sw-on");

  function show(a, amt){
    if(!a){ tag.hidden = true; return; }
    const n = a.n && $(a.n) ? $(a.n).textContent : "";
    tag.hidden = false; tag.className = "sw-tag " + a.c; tag.style.opacity = Math.min(1, amt);
    tag.innerHTML = `<b>${a.t}</b>${n ? `<small>${n}</small>` : ""}`;
  }
  function put(x, y, anim){
    stage.style.transition = anim || "none";
    stage.style.transform = x || y ? `translate(${x}px,${y}px) rotate(${x / 18}deg)` : "";
  }

  stage.addEventListener("pointerdown", e => {
    if(e.button > 0 || !state()) return;
    down = true; moved = false; drag = false; sx = e.clientX; sy = e.clientY; dx = dy = 0; pid = e.pointerId;
  });
  stage.addEventListener("pointermove", e => {
    if(!down || e.pointerId !== pid) return;
    dx = e.clientX - sx; dy = e.clientY - sy;
    if(!drag){
      if(Math.hypot(dx, dy) < TAP) return;
      drag = moved = true; try{ stage.setPointerCapture(pid); }catch(_){}
    }
    const s = state(), d = dirOf(dx, dy), a = s && action(d, s);
    // only move along the directions that do something right now
    const mx = (action("l", s) || action("r", s)) ? dx : 0, my = (!s.practice && s.flipped) ? dy : 0;
    put(mx, my);
    show(a, Math.max(Math.abs(dx), Math.abs(dy)) / NEED);
  });
  function end(e){
    if(!down || (e && e.pointerId !== pid)) return;
    down = false;
    if(!drag) return;
    drag = false; try{ stage.releasePointerCapture(pid); }catch(_){}
    const s = state(), d = dirOf(dx, dy), a = s && action(d, s), far = Math.max(Math.abs(dx), Math.abs(dy)) >= NEED;
    if(a && far){
      const fx = d === "r" ? 1 : d === "l" ? -1 : 0, fy = d === "d" ? 1 : d === "u" ? -1 : 0;
      put(fx * innerWidth, fy * innerHeight * .8, "transform .22s ease-in");
      store.set("fc:swiped", true); hint();
      setTimeout(() => {
        $(a.b).click(); tag.hidden = true;
        put(0, 0); stage.classList.remove("sw-in"); void stage.offsetWidth; stage.classList.add("sw-in");
      }, 200);
    } else if(!a && far && s && !s.flipped){
      put(0, 0, "transform .2s"); tag.hidden = true; $("flip").click();   // not flipped yet: show the answer instead
    } else { put(0, 0, "transform .2s"); tag.hidden = true; }
  }
  stage.addEventListener("pointerup", end);
  stage.addEventListener("pointercancel", end);
  // a drag must not also count as a tap that flips the card
  card.addEventListener("click", e => { if(moved){ e.stopImmediatePropagation(); e.preventDefault(); moved = false; } }, true);

  // a one-time reminder under the card
  const p = document.createElement("p"); p.className = "sw-hint"; p.hidden = true;
  $("nav-practice").after(p);
  function hint(){
    const s = state(); let t = "";
    if(!store.get("fc:swiped", false)){
      t = !s ? "" : s.practice ? "Flip the card, then swipe it: right if you got it, left if you are still learning." :
        "Flip the card, then swipe it: ← again, ↓ hard, ↑ good, → easy.";
    }
    p.textContent = t; p.hidden = !t;
  }
  new MutationObserver(hint).observe(card, { attributes:true, attributeFilter:["class"] });
  new MutationObserver(hint).observe($("nav-practice"), { attributes:true, attributeFilter:["hidden"] });
  hint();
})();
