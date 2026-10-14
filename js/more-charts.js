/* Collapses the charts of conjugations that build a tense the same way as amō.
   #charts-col carries the settings: data-show="amo" (verb ids always shown), optional data-groups="impf"
   (only collapse inside these tense groups) and data-more-note (one sentence beside the button).
   A pattern button that lights up only hidden charts opens them. */
(function(){
  const col = document.getElementById('charts-col');
  if(!col || !col.dataset.show) return;
  const show = col.dataset.show.split(' ');
  const only = col.dataset.groups ? col.dataset.groups.split(' ') : null;
  const note = col.dataset.moreNote || '';
  const vid = box => { const c = box.querySelector('.cell[data-k]'); return c ? c.dataset.k.split('.')[0].split('-')[0] : ''; };
  const name = box => (box.querySelector('.de') || {}).textContent.split(',')[0];

  const grid = document.getElementById('charts-grid');
  let boxes = grid.querySelectorAll('.vgroup').length
    ? [...grid.querySelectorAll('.vgroup')].filter(g => !only || only.includes(g.dataset.group)).map(g => g.querySelector('.charts'))
    : [grid];
  const sets = [];
  boxes.forEach(cont => {
    const all = [...cont.children].filter(b => b.classList.contains('noun'));
    const more = all.filter(b => !show.includes(vid(b)));
    if(!more.length) return;
    const bar = document.createElement('div'); bar.className = 'more-bar';
    const btn = document.createElement('button'); btn.type = 'button'; btn.className = 'more-btn';
    bar.appendChild(btn);
    if(note){ const p = document.createElement('p'); p.className = 'more-note'; p.innerHTML = note; bar.appendChild(p); }
    cont.after(bar);
    const set = { all, more, btn, open:false };
    const draw = () => {
      more.forEach(b => b.classList.toggle('more-off', !set.open));
      cont.classList.toggle('more-closed', !set.open);
      btn.setAttribute('aria-expanded', set.open);
      btn.textContent = set.open ? 'Hide the other conjugations' : 'Show the other conjugations (' + more.map(name).join(', ') + ')';
    };
    set.draw = draw;
    btn.onclick = () => { set.open = !set.open; draw(); };
    draw(); sets.push(set);
  });

  // a pattern button that marks only hidden charts opens them
  document.addEventListener('click', e => {
    const chip = e.target.closest('[id^="p-"]');
    if(!chip) return;
    const tag = `var(--${chip.id})`;
    const has = b => [...b.querySelectorAll('.cell.pat')].some(c => c.style.getPropertyValue('--pfg').trim() === tag);
    setTimeout(() => {
      if(chip.getAttribute('aria-pressed') !== 'true') return;
      sets.forEach(s => {
        if(!s.open && s.more.some(has) && !s.all.filter(b => !s.more.includes(b)).some(has)){ s.open = true; s.draw(); }
      });
    }, 0);
  });
})();
