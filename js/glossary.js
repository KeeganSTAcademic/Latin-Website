/* Grammar terms on hover (like the dictionary's abbreviations).
   Marks the first use of each term in each block of a grammar page with a dotted underline;
   hovering, focusing or tapping it shows a short plain-language definition.
   Words that are also everyday English (person, number, time) are only marked in their grammar sense. */
(function(){
  // [label, pattern source (case-insensitive, whole word), definition]
  const TERMS = [
    // parts of speech
    ['noun', 'nouns?', 'A word for a person, place, thing or idea.'],
    ['pronoun', 'pronouns?', 'A word that stands in place of a noun.'],
    ['adjective', 'adjectives?', 'A word that describes a noun. In Latin it matches its noun in case, number and gender.'],
    ['verb', 'verbs?', 'A word for an action or a state of being.'],
    ['adverb', 'adverbs?', 'A word that tells how, when or where something happens. Adverbs don\'t change their endings.'],
    ['preposition', 'prepositions?', 'A small word placed before a noun to show place, direction or time. In Latin each one takes the accusative or the ablative.'],
    ['conjunction', 'conjunctions?', 'A word that joins words or clauses: "and", "but", "because".'],
    ['participle', 'participles?', 'A form of a verb that works like an adjective: "the running water", "the broken vase".'],
    ['infinitive', 'infinitives?', 'The "to" form of a verb, like to love or to be.'],
    // kinds of pronoun
    ['personal', 'personal(?= pronouns?)', 'Personal pronouns stand for the people in a conversation: I, me, you, we, us.'],
    ['reflexive', 'reflexives?', 'Points back to the subject of its sentence: "he hurt himself", "they saw themselves".'],
    ['demonstrative', 'demonstratives?', 'A pointing word, like this or that.'],
    ['intensive', 'intensive', 'Adds emphasis to a noun or pronoun: "the king himself", "the very thing".'],
    ['relative', 'relatives?(?! to)', 'Relative pronouns (who, which, that) begin a clause that describes a noun: "the girl who sings".'],
    ['interrogative', 'interrogatives?', 'Asks a question: who, what, which.'],
    ['indefinite', 'indefinites?', 'Refers to someone or something without saying exactly who or what: "someone", "anyone", "a certain man".'],
    ['pronominal', 'pronominal', 'Pronoun-like. The pronominal adjectives are adjectives that take pronoun endings in the genitive and dative singular.'],
    ['possessive', 'possessives?', 'Shows who owns something: "my", "your", "his own".'],
    ['antecedent', 'antecedents?', 'The noun that a relative pronoun refers back to. In "the girl who sings", the antecedent is "girl".'],
    // the categories
    ['case', 'cases?', 'The form of a word that shows its job in the sentence. English still does this with pronouns: "he" (subject) and "him" (object). Latin does it with endings on nouns, pronouns and adjectives.'],
    ['number', '(?<![Aa] )number(?! of)', 'Whether a word is singular (one) or plural (more than one).'],
    ['gender', 'genders?', 'Every Latin noun is masculine, feminine or neuter. For things, gender is a grammar category, not about being male or female: a table is feminine, a war is neuter.'],
    ['person', '(?:1st|2nd|3rd|first|second|third)[- ]person|person(?=,? (?:and )?number)', 'Who is doing the action. 1st person is the speaker (I, we), 2nd person is the one spoken to (you), 3rd person is anyone else (he, she, it, they).'],
    ['declension', 'declensions?|declined|declines', 'A family of nouns that share the same set of endings. Latin has five. To decline a word is to list its forms.'],
    ['conjugation', 'conjugations?|conjugated', 'A family of verbs that share the same pattern of endings. Latin has four.'],
    ['tense', 'tenses?', 'The verb form that shows when an action happens and whether it is ongoing or complete: "walks", "was walking", "walked", "will walk".'],
    ['time', 'time markers?|(?<=aspect (?:and|or) )time|time(?= (?:and|or) aspect)|(?<=(?:past|present|future) )time', 'When an action happens: past, present or future.'],
    ['aspect', 'aspects?', 'Whether an action is seen as ongoing ("was walking") or as complete ("walked").'],
    ['mood', 'moods?', 'How a verb presents an action: as a fact ("you are quiet"), a command ("be quiet!") or something possible or wished ("if only you were quiet").'],
    ['voice', 'voices?', 'Whether the subject does the action (active: "the dog bites") or receives it (passive: "the dog is bitten").'],
    ['stem', 'stems?', 'The part of a word that carries its meaning, before the ending: the "walk" in "walking".'],
    ['ending', 'endings?', 'The letters at the end of a word that change to show its case and number, or its person, number and tense.'],
    ['agree', 'agree(?:s|ing|ment)?', 'Match. An adjective agrees with its noun when it has the same case, number and gender.'],
    ['clause', 'clauses?', 'A group of words with its own verb. "I saw the girl who was singing" has two: "I saw the girl" and "who was singing".'],
    ['subject', 'subjects?', 'Who or what does the action of the verb, or what the sentence is about: "the girl" in "the girl sings". In Latin it is nominative.'],
    ['direct object', 'direct objects?', 'Who or what receives the action of the verb: "the girl" in "I see the girl". In Latin it is accusative. Often just called the object.'],
    ['indirect object', 'indirect objects?', 'The person to whom or for whom something is given, shown or told: "the girl" in "I give the book to the girl". In Latin it is dative.'],
    ['object', 'objects?', 'Usually means the direct object: who or what receives the action of the verb, like "the girl" in "I see the girl". In Latin it is accusative.'],
    ['predicate nominative', 'predicate nominatives?|predicate nouns?', 'A noun or adjective after a linking verb that renames or describes the subject: "a farmer" in "Marcus is a farmer". It is nominative, like the subject.'],
    ['predicate', 'predicates?', 'What the sentence says about the subject: the verb and the words that go with it. In "Marcus is a farmer", the predicate is "is a farmer".'],
    ['linking verb', 'linking verbs?', 'A verb like "be", "become" or "seem" that connects the subject to a word describing or renaming it.'],
    ['appositive', 'appositives?|apposition', 'A noun placed right next to another noun to rename or explain it, like "a farmer" in "Marcus, a farmer, works hard". It takes the same case.'],
    ['indirect question', 'indirect questions?', 'A question reported inside another sentence, as in "he asked who was coming". In Latin its verb is subjunctive.'],
    ['partitive', 'partitive', 'Naming the whole that a part is taken from, as in "one of us".'],
    ['comparative', 'comparatives?', 'The "more" or "-er" form of an adjective or adverb.'],
    ['enclitic', 'enclitics?', 'A small word attached to the end of another word, the way "-n\'t" attaches in "can\'t".'],
    ['macron', 'macrons?', 'The line over a vowel that marks it as long.'],
    ['i-stem', 'i-stems?', 'Third-declension nouns with an extra i in some forms, most often the genitive plural.'],
    // case names
    ['nominative', 'nominatives?|nom\\.', 'The case of the subject, and of a word that renames the subject after "is".'],
    ['genitive', 'genitives?|gen\\.', 'The "of" case: it shows possession or a relationship.'],
    ['dative', 'datives?|dat\\.', 'The "to / for" case: the indirect object, and the person something is given to or done for.'],
    ['accusative', 'accusatives?|acc\\.', 'The case of the direct object, and of some prepositions, especially ones showing motion toward.'],
    ['ablative', 'ablatives?|abl\\.', 'The "by / with / from / in" case: means, manner, place, time or separation, and some prepositions.'],
    ['vocative', 'vocatives?|voc\\.', 'The case for calling or speaking to someone.'],
    ['locative', 'locatives?', 'The "at" case, used with names of cities and a few words like home.'],
    ['singular', 'singular|sg\\.', 'One.'],
    ['plural', 'plurals?|pl\\.', 'More than one.'],
    ['masculine', 'masculine|m\\.', 'One of the three genders. Most words for men are masculine, along with many words for things.'],
    ['feminine', 'feminine|f\\.', 'One of the three genders. Most words for women are feminine, along with many words for things.'],
    ['neuter', 'neuters?|n\\.', 'One of the three genders: neither masculine nor feminine. The neuter nominative and accusative are always the same.'],
    // verb names
    ['indicative', 'indicative', 'The mood for statements and questions of fact.'],
    ['subjunctive', 'subjunctives?', 'The mood for actions that are possible, wished, intended or reported.'],
    ['imperative', 'imperatives?', 'The mood for commands.'],
    ['active', 'active', 'The subject does the action.'],
    ['passive', 'passives?', 'The subject receives the action.'],
    ['deponent', 'deponents?', 'A verb with passive endings but an active meaning.'],
    ['principal parts', 'principal parts', 'The forms you learn for a verb; every other form is built from them.'],
    ['pluperfect', 'pluperfect', 'The tense for an action completed before another past action: had done.'],
    ['future perfect', 'future perfect', 'The tense for an action that will be completed before a point in the future: will have done.'],
    ['imperfect', 'imperfect', 'The tense for ongoing or repeated action in the past: was doing, used to do.'],
    ['perfect', 'perfect', 'The tense for a completed action: did, has done.'],
    ['present', 'present(?= (?:tense|active|passive|system|stem|indicative|imperative|infinitive|participle|time))', 'The tense for what is happening now: does, is doing.'],
    ['future', 'future(?! perfect)(?= (?:tense|active|passive|indicative|time|marker))', 'The tense for what will happen: will do.'],
  ];
  const DEF = {}; TERMS.forEach(([k,, t]) => DEF[k] = t);
  // longest patterns first so "direct object" wins over "object", "future perfect" over "perfect"
  const ORDER = TERMS.slice().sort((a, b) => b[0].length - a[0].length);
  const RE = new RegExp(ORDER.map(([, re]) => `(?<![\\w\\u00C0-\\u024F-])(${re})(?![\\w\\u00C0-\\u024F])`).join('|'), 'gi');
  const KEY = m => { for(let j = 1; j < m.length; j++) if(m[j] !== undefined) return ORDER[j - 1][0]; };

  const SKIP = 'script,style,button,a,select,input,textarea,label,h1,h2,th,.tb-label,i,em,code,nav,footer,.q,#sb,.sb,.sb-open,.gl,.cell,.chip,.tb-sub,.legend,.src,.sec,.label,figcaption,[lang="la"],.la,.form,#gltip';
  const BLOCK = 'article,section,aside,figure,table,.use,.pnote,.tip,.amb-box,.like-noun,.intro,.basic,.card,.noun,.pattern';
  const UNIT = '#card,.card,.use,.noun,.intro,.basic,.pnote,.pattern,figure,table,article';
  // everyday basics are marked once per page (and again in the inspector); the rest once per unit
  const BASIC = new Set(['noun','verb','adjective','subject','object','singular','plural','case','ending','stem','number','gender','masculine','feminine','neuter','agree','preposition','declension','conjugation']);
  const root = document.body;
  let busy = false;

  function scan(){
    if(busy) return; busy = true;
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: n => (!n.parentElement || n.parentElement.closest(SKIP) || !n.textContent.trim()) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
    const nodes = []; let n; while((n = walker.nextNode())) nodes.push(n);
    const pageSeen = new Set([...root.querySelectorAll('.gl')].filter(g => BASIC.has(g.dataset.k) && !g.closest('#card')).map(g => g.dataset.k));
    const seen = new Map();  // block -> Set of terms already marked in it
    const seenIn = b => { if(!seen.has(b)){ seen.set(b, new Set([...b.querySelectorAll('.gl')].map(s => s.dataset.k))); } return seen.get(b); };
    for(const node of nodes){
      const txt = node.textContent; RE.lastIndex = 0;
      if(!RE.test(txt)) continue;
      const block = node.parentElement.closest(BLOCK) || root;
      // a term marked in a containing block counts as seen here too
      // ...but only up to a self-contained unit (the inspector, a use card, a chart, the intro), so each of those gets its own marks
      const outer = []; if(!block.matches(UNIT)) for(let b = block.parentElement && block.parentElement.closest(BLOCK); b; b = b.parentElement && b.parentElement.closest(BLOCK)){ outer.push(seenIn(b)); if(b.matches(UNIT)) break; }
      const local = [seenIn(block), ...outer], inCard = !!node.parentElement.closest('#card');
      const setsFor = k => (BASIC.has(k) && !inCard) ? [pageSeen] : local;
      const has = k => setsFor(k).some(x => x.has(k));
      RE.lastIndex = 0; let m, last = 0; const frag = document.createDocumentFragment();
      while((m = RE.exec(txt))){
        const k = KEY(m); if(!k || has(k)) continue;
        setsFor(k).forEach(x => x.add(k));
        frag.append(txt.slice(last, m.index));
        const s = document.createElement('g-t'); s.className = 'gl'; s.tabIndex = 0; s.dataset.k = k; s.textContent = m[0];
        frag.append(s); last = m.index + m[0].length;
      }
      if(!last) continue;
      frag.append(txt.slice(last)); node.replaceWith(frag);
    }
    busy = false;
  }

  const css = document.createElement('style');
  css.textContent = `.gl{display:inline;font:inherit;color:inherit;text-decoration:underline dotted;text-decoration-color:var(--rule2,var(--muted));text-decoration-thickness:1.5px;text-underline-offset:3px;cursor:help}
.gl:hover,.gl:focus-visible{text-decoration-color:var(--accent);color:var(--accent);outline:none}
#gltip{position:fixed;z-index:60;max-width:320px;background:var(--ink);color:var(--bg);font:1rem/1.5 var(--font,inherit);padding:9px 13px;border-radius:10px;box-shadow:0 6px 24px rgba(0,0,0,.18);pointer-events:none;text-align:left}
#gltip b{color:var(--bg);text-transform:capitalize;margin-right:4px}`;
  document.head.append(css);
  const tip = document.createElement('div'); tip.id = 'gltip'; tip.hidden = true; tip.setAttribute('role', 'tooltip'); document.body.append(tip);
  let tipFor = null;
  const esc = s => s.replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  function show(el){
    tipFor = el; tip.innerHTML = `<b>${esc(el.dataset.k)}:</b> ${esc(DEF[el.dataset.k])}`; tip.hidden = false;
    tip.style.maxWidth = Math.min(320, innerWidth - 24) + 'px';
    const r = el.getBoundingClientRect(), tw = tip.offsetWidth, th = tip.offsetHeight;
    tip.style.left = Math.max(12, Math.min(r.left + r.width / 2 - tw / 2, innerWidth - tw - 12)) + 'px';
    let y = r.top - th - 8; if(y < 8) y = r.bottom + 8; tip.style.top = y + 'px';
  }
  function hide(){ tip.hidden = true; tipFor = null; }
  document.addEventListener('mouseover', e => { const g = e.target.closest && e.target.closest('.gl'); if(g) show(g); });
  document.addEventListener('mouseout', e => { if(e.target.closest && e.target.closest('.gl')) hide(); });
  document.addEventListener('focusin', e => { const g = e.target.closest('.gl'); g ? show(g) : (tipFor && hide()); });
  document.addEventListener('click', e => { const g = e.target.closest('.gl'); if(g){ tipFor === g && !tip.hidden ? hide() : show(g); } else if(tipFor) hide(); });
  document.addEventListener('keydown', e => { if(e.key === 'Escape') hide(); });
  addEventListener('scroll', hide, true);

  // pages build their content with JS, and the inspector redraws on hover: mark new text as it appears
  let queued = false;
  new MutationObserver(() => { if(busy || queued) return; queued = true; requestAnimationFrame(() => { queued = false; scan(); }); })
    .observe(root, {childList: true, subtree: true});
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', scan); else scan();
})();
