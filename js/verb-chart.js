/* Interactive verb charts for the grammar pages (future, incomplete passives, perfect system).
   A page supplies its data and calls VerbChart({...}); the page's HTML provides the toolbar,
   #charts-grid, the optional #er / #er-grid panel (irregular sum) and the #card panel.

   verbs:    [{ id, dict, conj, meta, group?, extra?, f:[[stem, vowel, sign, ending] × 6], eng?:[6 English forms] }]
             persons in the order 1sg 2sg 3sg 1pl 2pl 3pl. extra: true puts the chart in the #er panel.
   groups:   optional [{ id, name }]: charts with a matching verb.group get a heading, and a
             "Tense" row of chips shows one group or all of them.
   english:  c => ({ main, alt }) for a cell c = { verb, p (person), i (0–5), ... }
   labels:   c => ({ st, vw, ts, en }) names of the parts in the breakdown (empty parts are skipped)
   patterns: [{ id, lab, txt, part ('st'|'vw'|'ts'|'en'|'vwen'|'all'), test: c => bool, note }]
   notes:    { "verbId.1sg": "html", ... }
   idle:     html for the detail card before anything is chosen */
(function(){
  const PERSONS = [
    {k:'1sg',p:'1st',n:'sg',sub:'I'},{k:'2sg',p:'2nd',n:'sg',sub:'you'},{k:'3sg',p:'3rd',n:'sg',sub:'he/she/it'},
    {k:'1pl',p:'1st',n:'pl',sub:'we'},{k:'2pl',p:'2nd',n:'pl',sub:'you (all)'},{k:'3pl',p:'3rd',n:'pl',sub:'they'}
  ];
  const ROWS = ['1st','2nd','3rd'];
  const $ = id => document.getElementById(id);
  const strip = s => s.normalize('NFD').replace(/̄/g,'').normalize('NFC');

  window.VerbChart = function(cfg){
    const { verbs, english, labels, patterns = [], notes = {}, idle = '', groups = null } = cfg;
    const state = { mac:true, end:false, en:false, pats:new Set(), active:null, group:'all' };
    const shown = s => state.mac ? s : strip(s);
    const cid = v => v.id + (v.group ? '-' + v.group : '');

    const CELLS = [];
    verbs.forEach(v => PERSONS.forEach((p, i) => {
      const [st, vw, ts, en] = v.f[i];
      CELLS.push({ key:`${cid(v)}.${p.k}`, note:`${v.id}${v.group ? '.' + v.group : ''}.${p.k}`, verb:v, p, i, st, vw, ts, en, form:st+vw+ts+en });
    }));
    const byKey = Object.fromEntries(CELLS.map(c => [c.key, c]));
    const parseName = c => `${c.p.p} person ${c.p.n === 'sg' ? 'singular' : 'plural'}`;

    // pattern chips
    const pRow = $('patterns');
    if(patterns.length){
      patterns.forEach(p => {
        const b = document.createElement('button');
        b.className = 'chip'; b.id = 'p-' + p.id; b.setAttribute('aria-pressed', 'false');
        b.style.setProperty('--c', `var(--p-${p.id})`); b.style.setProperty('--cbg', `var(--p-${p.id}-bg)`);
        b.innerHTML = `<span class="sw"></span><span class="l">${p.lab}</span> ${p.txt}`;
        b.onclick = () => { state.pats.has(p.id) ? state.pats.delete(p.id) : state.pats.add(p.id); render(); };
        pRow.appendChild(b);
      });
      const clr = document.createElement('button');
      clr.className = 'chip plain clear'; clr.textContent = 'Clear';
      clr.onclick = () => { state.pats.clear(); render(); };
      pRow.appendChild(clr);
    } else pRow.hidden = true;

    // tense chips (pages with several tenses)
    if(groups){
      const row = document.createElement('div'); row.className = 'tb-row';
      row.innerHTML = '<span class="tb-label">Tense</span><div class="seg" id="groups"></div>';
      pRow.after(row);
      [{id:'all', name:'All'}, ...groups].forEach(g => {
        const b = document.createElement('button');
        b.className = 'chip plain'; b.dataset.g = g.id; b.textContent = g.name;
        b.onclick = () => { state.group = g.id; render(); };
        $('groups').appendChild(b);
      });
    }

    // charts
    const col = $('charts-col'), main = $('charts-grid'), er = $('er-grid');
    const chart = v => {
      const box = document.createElement('div'); box.className = 'noun'; if(v.group) box.dataset.group = v.group;
      let h = `<div class="noun-h"><div class="de">${v.dict}</div><div class="meta">${v.meta || v.conj}</div></div><div class="grid"><div class="hd"></div><div class="hd">Sing.</div><div class="hd">Plur.</div>`;
      ROWS.forEach(r => {
        h += `<div class="rl">${r}</div>`;
        ['sg','pl'].forEach(n => { h += `<button class="cell" data-k="${cid(v)}.${r[0]}${n}" aria-label="${v.dict.split(',')[0]} ${r} person ${n === 'sg' ? 'singular' : 'plural'}"></button>`; });
      });
      box.innerHTML = h + '</div>';
      return box;
    };
    if(groups){
      groups.forEach(g => {
        const sec = document.createElement('section'); sec.className = 'vgroup'; sec.dataset.group = g.id;
        sec.innerHTML = `<h3 class="vgroup-h">${g.name}</h3><div class="charts three-up"></div>`;
        verbs.filter(v => v.group === g.id && !v.extra).forEach(v => sec.lastChild.appendChild(chart(v)));
        main.appendChild(sec);
      });
      main.classList.remove('charts', 'three-up'); main.classList.add('vgroups');
    } else verbs.filter(v => !v.extra).forEach(v => main.appendChild(chart(v)));
    verbs.filter(v => v.extra).forEach(v => er && er.appendChild(chart(v)));
    if(er && !er.children.length) $('er').hidden = true;

    const cellEls = [...document.querySelectorAll('.cell')];
    cellEls.forEach(el => {
      const go = () => { state.active = el.dataset.k; renderActive(); };
      const stop = () => { if(state.active === el.dataset.k){ state.active = null; renderActive(); } };
      el.addEventListener('mouseenter', go); el.addEventListener('focus', go); el.addEventListener('click', go);
      el.addEventListener('mouseleave', stop); el.addEventListener('blur', stop);
    });
    document.addEventListener('click', e => { if(!e.target.closest('.cell') && state.active){ state.active = null; renderActive(); } });
    const toggle = (id, key) => { $(id).onclick = () => { state[key] = !state[key]; render(); }; };
    toggle('t-mac', 'mac'); toggle('t-end', 'end'); toggle('t-en', 'en');

    function render(){
      ['mac','end','en'].forEach(k => $('t-' + k).setAttribute('aria-pressed', state[k]));
      col.classList.toggle('endonly', state.end); col.classList.toggle('showen', state.en);
      patterns.forEach(p => $('p-' + p.id).setAttribute('aria-pressed', state.pats.has(p.id)));
      if(groups){
        document.querySelectorAll('#groups .chip').forEach(b => b.setAttribute('aria-pressed', b.dataset.g === state.group));
        document.querySelectorAll('.vgroup').forEach(s => s.hidden = state.group !== 'all' && s.dataset.group !== state.group);
      }
      cellEls.forEach(el => {
        const c = byKey[el.dataset.k];
        const hit = patterns.filter(p => state.pats.has(p.id) && p.test(c)).pop();
        el.innerHTML = `<span class="fm"><span class="st">${shown(c.st)}</span><span class="vw">${shown(c.vw)}</span><span class="ts">${shown(c.ts)}</span><span class="en">${shown(c.en)}</span></span><span class="eng">${english(c).main}</span>`;
        el.className = 'cell';
        if(hit){ el.classList.add('pat', 'pp-' + hit.part); el.style.setProperty('--pbg', `var(--p-${hit.id}-bg)`); el.style.setProperty('--pfg', `var(--p-${hit.id})`); }
      });
      $('pnotes').innerHTML = patterns.filter(p => state.pats.has(p.id)).map(p => `<div class="pnote" style="--c:var(--p-${p.id})">${p.note}</div>`).join('');
      renderActive();
    }

    function renderActive(){
      const card = $('card');
      if(!state.active){
        cellEls.forEach(el => el.classList.remove('active'));
        card.innerHTML = `<div class="parse">Inspect a form</div><div class="tr">Hover over or tap any form in the charts.</div><div class="job">${idle}</div>`;
        return;
      }
      const c = byKey[state.active];
      cellEls.forEach(el => el.classList.toggle('active', el.dataset.k === c.key));
      const E = english(c), L = labels(c), parts = [];
      if(c.st) parts.push(`<span class="bk-st">${shown(c.st)}-</span> ${L.st}`);
      if(c.vw) parts.push(`<span class="bk-vw">${shown(c.vw)}</span> ${L.vw}`);
      if(c.ts) parts.push(`<span class="bk-ts">-${shown(c.ts)}-</span> ${L.ts}`);
      if(c.en) parts.push(`<span class="bk-en">-${shown(c.en)}</span> ${L.en}`);
      const g = groups && c.verb.group ? groups.find(x => x.id === c.verb.group).name.toLowerCase() + ' · ' : '';
      let out = `<div class="parse">${parseName(c)} · ${g}${c.verb.dict}</div>
        <div class="form"><span>${shown(c.st)}</span><span class="vwb">${shown(c.vw)}</span><span class="tsb">${shown(c.ts)}</span><span class="en">${shown(c.en)}</span></div>
        <div class="tr">${E.main}</div>
        ${E.alt ? `<div class="job">also: ${E.alt}</div>` : ''}
        <div class="breakdown">${parts.join(' <span class="plus">+</span> ')}</div>`;
      const note = notes[c.note], pats = patterns.filter(p => p.test(c));
      if(note || pats.length) out += `<div class="tip">${note ? `<p>${note}</p>` : ''}${pats.length ? `<p>Patterns: ${pats.map(p => `<b style="color:var(--p-${p.id})">${p.lab}</b> (${p.txt})`).join(' · ')}</p>` : ''}</div>`;
      card.innerHTML = out;
    }
    render();
  };
})();
