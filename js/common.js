/* Shared helpers for every interactive page on the site.
   Exposed as window.Site so pages can use them without a build step. */
(function(){
  const $ = id => document.getElementById(id);

  const esc = s => String(s).replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

  /* Fisher–Yates shuffle, in place */
  function shuffle(a){
    for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];}
    return a;
  }

  /* localStorage that never throws (private windows, blocked storage).
     Keys are prefixed "latin:" so pages never collide with each other. */
  const store = {
    get(key, fallback){ try{ const v=localStorage.getItem("latin:"+key); return v===null?fallback:JSON.parse(v); }catch(e){ return fallback; } },
    set(key, value){ try{ localStorage.setItem("latin:"+key, JSON.stringify(value)); }catch(e){} }
  };

  const param = name => new URLSearchParams(location.search).get(name);

  /* Fetch JSON relative to the site root (works on GitHub Pages sub-paths). */
  async function loadJSON(path){
    const r = await fetch(path, {cache:"no-cache"});
    if(!r.ok) throw new Error(path+" → "+r.status);
    return r.json();
  }

  /* Toggle button ("chip") */
  function chip(parent, label, pressed, onClick){
    const b=document.createElement("button");
    b.type="button"; b.className="chip"; b.textContent=label;
    b.setAttribute("aria-pressed", pressed ? "true" : "false");
    b.onclick=onClick; parent.appendChild(b); return b;
  }

  window.Site = { $, esc, shuffle, store, param, loadJSON, chip };
})();
