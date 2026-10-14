# Indefinites: an overview page plus aliquis and quīdam pages (A&G §§149-151, 309-313), adapted for Latin III-IV students.
# Spliced into TABS in place of the single "indefinite" entry (see the end of pronoun_content.py).

def SCALE(cur=None):
    """How definite: quis -> aliquis -> quīdam along a line, quisquam / ūllus underneath. Uses the .dist styles."""
    on = lambda k: ' on' if cur == k else ''
    here = lambda k: '<span class="here">This page</span>' if cur == k else ''
    st = lambda k, who, la, eg: (f'<div class="st{on(k)}">{here(k)}<span class="who">{who}</span>'
                                 f'<span class="la" lang="la">{la}</span><span class="eg">{eg}</span></div>')
    return ('<figure class="dist"><figcaption>How definite is it?</figcaption>'
            '<div class="dist-row">'
            + st("quis", "Anyone at all", "quis, quid", "if <b>anyone</b> comes: whoever it may be")
            + st("aliquis", "Someone", "aliquis, aliquid", "<b>someone</b> is knocking: a real person, but I don't know who")
            + st("quidam", "A certain one", "quīdam, quaedam, quiddam", "<b>a certain</b> man came: I know who, but I'm not saying")
            + '</div><div class="dist-axis" aria-hidden="true"><span>vaguer</span><span>more definite</span></div>'
            + st("quisquam", "In negative sentences", "quisquam, ūllus", "not <b>anyone</b> at all, without <b>any</b> fear")
            + '</figure>')

TABLE = ('<div class="dem-table"><table><thead><tr><th>Pronoun</th><th>Means</th><th>Where you find it</th><th>A&amp;G</th></tr></thead><tbody>'
  '<tr><td lang="la"><a href="pronouns-quis-indef.html"><i>quis, quid</i></a></td><td>anyone, anything</td><td>after <i>sī, nisi, num, nē</i></td><td>§310.a</td></tr>'
  '<tr><td lang="la"><a href="pronouns-aliquis.html"><i>aliquis, aliquid</i></a></td><td>someone, something</td><td>anywhere; adjective <i>aliquī</i>: some</td><td>§310</td></tr>'
  '<tr><td lang="la"><a href="pronouns-quidam.html"><i>quīdam, quaedam, quiddam</i></a></td><td>a certain one</td><td>anywhere; plural often some, a few</td><td>§310</td></tr>'
  '<tr><td lang="la"><a href="pronouns-quisquam.html"><i>quisquam</i> · <i>ūllus</i></a></td><td>anyone at all · any</td><td>in negative sentences and questions</td><td>§311</td></tr>'
  '<tr><td lang="la"><a href="pronouns-quisque.html"><i>quisque</i></a></td><td>each, every</td><td>often after a superlative or <i>suus</i></td><td>§313</td></tr>'
  '<tr><td lang="la"><a href="pronouns-quisquis.html"><i>quisquis, quidquid</i></a></td><td>whoever, whatever</td><td>starts a clause, like a relative</td><td>§151.a</td></tr>'
  '<tr><td lang="la"><a href="pronouns-quicumque.html"><i>quīcumque</i></a></td><td>whoever, whatever; any … that</td><td>starts a clause, like a relative</td><td>§151</td></tr>'
  '</tbody></table></div>')

# The indefinite relatives: who? / who / whoever. Uses the .dist styles.
def WHO(cur=None):
    on = lambda k: ' on' if cur == k else ''
    here = lambda k: '<span class="here">This page</span>' if cur == k else ''
    st = lambda k, who, la, eg: (f'<div class="st{on(k)}">{here(k)}<span class="who">{who}</span>'
                                 f'<span class="la" lang="la">{la}</span><span class="eg">{eg}</span></div>')
    return ('<figure class="dist"><figcaption>Which person does it mean?</figcaption><div class="dist-row">'
            + st("quis", "Asking", "quis? quī?", "<b>who</b> is at the door?")
            + st("qui", "A known person", "quī, quae, quod", "the man <b>who</b> is at the door: that one")
            + st("ever", "Anyone at all", "quisquis · quīcumque", "<b>whoever</b> is at the door: I don't know or care who")
            + '</div></figure>')

INDEF = [
 {"id": "indefinite", "name": "Indefinites", "q": "someone, anyone, a certain", "prons": ["quisindef", "aliquis", "quidam", "quisquam", "quisque"], "secs": "149–151, 309–313",
  "summary": "An <b>indefinite</b> pronoun refers to someone or something without saying exactly who or what. English has several, and they differ in how much the speaker has in mind. "
             "<i>Anyone</i> could be anybody at all. <i>Someone</i> is a real person, but we don't know or care who. <i>A certain man</i> is a particular man the speaker could name but doesn't. "
             "Latin marks the same three steps with <i>quis</i>, <i>aliquis</i> and <i>quīdam</i>. Next to them are <i>quisquam</i>, anyone at all in a negative sentence, <i>quisque</i>, each, "
             "and the indefinite relatives <i>quisquis</i> and <i>quīcumque</i>, whoever. They are all built on <i>quis</i> or <i>quī</i>, so the endings will look familiar. "
             "Each one has its own page; this page sets them side by side.",
  "extra": SCALE() + TABLE,
  "pattern": "<b>Pattern:</b> every indefinite here is <i>quis</i> or <i>quī</i> with something added: <i>ali-</i> on the front (<i>aliquis</i>), <i>-dam</i>, <i>-quam</i>, <i>-que</i> or <i>-cumque</i> on the end (<i>quīdam, quisquam, quisque, quīcumque</i>), or the whole word said twice (<i>quisquis</i>). If you know <i>quis</i> and <i>quī</i>, you know most of these forms. The extras: <i>aliquis</i> has <i>aliqua</i>, not <i>aliquae</i>, for the feminine singular and neuter plural, and <i>quīdam</i> turns m into n before <i>-dam</i> (<i>quendam, quōrundam</i>).",
  "basic": {"name": "How definite?", "sec": "310",
   "rule": "Latin picks the word by how much the speaker has in mind. <b><i>Quis</i></b> is the vaguest: anyone at all, whoever it may be. "
           "<b><i>Aliquis</i></b> is someone real, but unknown or unimportant. <b><i>Quīdam</i></b> is the most definite: a particular person the speaker could name but doesn't.",
   "how": "Translate <i>quis</i> as anyone, <i>aliquis</i> as someone or some, <i>quīdam</i> as a certain (one). With a noun, they work as adjectives: <i>aliquī philosophī</i>, some philosophers; <i>quīdam homō</i>, a certain man.",
   "ex": [["Sī **quis** vēnerit, mē vocā.", "If anyone comes, call me. (anyone at all)", ""],
          ["**aliquī** philosophī ita putant", "some philosophers think so", "A&G §310"],
          ["habitant hīc **quaedam** mulierēs pauperculae", "some (particular) poor women live here", "Ter. Ad. 647"]]},
  "uses": [
   {"name": "After sī, nisi, num, nē: quis", "sec": "310.a", "lvl": "core",
    "what": "After <i>sī, nisi, num</i> and <i>nē</i>, plain <i>quis</i> means anyone: <i>sī quis</i>, if anyone. See <a href=\"pronouns-quis-indef.html\">Quis after sī, nisi, num, nē</a>.",
    "clue": "<i>Sī, nisi, num</i> or <i>nē</i> right before a form of <i>quis</i>.", "ex": [["sī **quis**", "if anyone", ""]]},
   {"name": "In negative sentences: quisquam, ūllus", "sec": "311", "lvl": "core",
    "what": "When a sentence says no one or nothing at all, Latin uses <i>quisquam</i> on its own and <i>ūllus</i> with a noun. See <a href=\"pronouns-quisquam.html\">Quisquam, quidquam</a>.",
    "clue": "<i>Nōn, numquam, sine</i> before <i>quisquam</i> or <i>ūllus</i>.", "ex": [["sine **ūllō** metū", "without any fear", "A&G §311"]]},
   {"name": "Each: quisque", "sec": "313", "lvl": "core",
    "what": "<i>Quisque</i> means each, every, and usually follows the word it goes with. See <a href=\"pronouns-quisque.html\">Quisque, quidque</a>.",
    "clue": "<i>-que</i> on a form of <i>quis</i> that does not mean and.", "ex": [["**suum cuique**", "to each his own", ""]]},
   {"name": "Whoever: quisquis, quīcumque", "sec": "151", "lvl": "core",
    "what": "<i>Quisquis</i> and <i>quīcumque</i> start a clause, like the relative <i>quī</i>, but they don't point back to anyone in particular: whoever, whatever. See <a href=\"pronouns-quisquis.html\">Quisquis</a> and <a href=\"pronouns-quicumque.html\">Quīcumque</a>.",
    "clue": "A doubled form (<i>quisquis, quidquid</i>) or <i>-cumque</i> on a form of <i>quī</i>.", "ex": [["**quisquis** es", "whoever you are", ""]]},
  ]},

 {"id": "indef-aliquis", "name": "Aliquis, aliquid", "q": "someone, something", "prons": ["aliquis"], "secs": "149, 310",
  "summary": "<i>Aliquis, aliquid</i> means someone, something: a real person or thing, but the speaker doesn't know or doesn't care which. "
             "It is <i>quis</i> with <i>ali-</i> (from <i>alius</i>, other) on the front, so its forms follow <i>quis</i> and <i>quī</i>: <i>alicuius, alicui, aliquem</i>. "
             "With a noun it becomes the adjective <i>aliquī, aliqua, aliquod</i>: some.",
  "extra": SCALE("aliquis"),
  "pattern": "<b>Pattern:</b> <i>ali-</i> + <i>quis</i>. The pronoun is <i>aliquis, aliquid</i> (someone, something); the adjective is <i>aliquī, aliqua, aliquod</i> (some). The feminine singular and the neuter plural are <i>aliqua</i>, not <i>aliquae</i>. Everything else is spelled like <i>quis</i> and <i>quī</i> with <i>ali-</i> in front.",
  "basic": {"name": "Someone, something", "sec": "310",
   "rule": "<b>On its own</b>, as a pronoun: <i>aliquis</i>, someone; <i>aliquid</i>, something. <b>With a noun</b>, as an adjective (<i>aliquī, aliqua, aliquod</i>), it agrees with the noun and means some: <i>aliquī philosophī</i>, some philosophers.",
   "how": "Cover the <i>ali-</i>, read what's left as a form of <i>quis</i> or <i>quī</i>, and translate it with some-: someone, something, to someone, some.",
   "ex": [["**Aliquis** pulsat.", "Someone is knocking.", ""],
          ["**Aliquid** dīc.", "Say something.", ""],
          ["**aliquī** philosophī ita putant", "some philosophers think so", "A&G §310"]]},
  "uses": [
   {"name": "Aliquis or quīdam?", "sec": "310", "lvl": "core",
    "what": "Both can come out as someone in English. <i>Aliquis</i> is someone unknown or unimportant; <i>quīdam</i> is a particular person the speaker has in mind but doesn't name.",
    "clue": "Ask whether the speaker knows who: no (<i>aliquis</i>), yes but isn't saying (<i>quīdam</i>).",
    "ex": [["**Aliquis** pulsat.", "Someone is knocking. (I don't know who)", ""], ["**Quīdam** pulsat.", "A certain man is knocking. (I know who)", ""]]},
   {"name": "Sī quis, not sī aliquis", "sec": "310.a", "lvl": "core",
    "what": "After <i>sī, nisi, num</i> and <i>nē</i>, the <i>ali-</i> drops and plain <i>quis</i> means anyone: <i>sī quis</i>, if anyone; <i>nē quid</i>, so that nothing.",
    "clue": "A form of <i>quis</i> right after <i>sī, nisi, num</i> or <i>nē</i>.",
    "ex": [["sī **quis**", "if anyone", ""], ["nē **quid**", "so that nothing", ""]]},
  ]},

 {"id": "indef-quidam", "name": "Quīdam, quaedam, quiddam", "q": "a certain one", "prons": ["quidam"], "secs": "149, 310",
  "summary": "<i>Quīdam, quaedam, quiddam</i> means a certain one: a particular person or thing that the speaker has in mind but doesn't name. English uses a certain the same way: a certain man came to see you. "
             "It is the relative <i>quī</i> with <i>-dam</i> on the end. In the plural it often just means some, a few.",
  "extra": SCALE("quidam"),
  "pattern": "<b>Pattern:</b> <i>quī</i> + <i>-dam</i>, declined like the relative <i>quī, quae, quod</i>: <i>cuiusdam, cuidam, quōdam</i>. Two changes: m becomes n before the d (<i>quendam, quandam, quōrundam, quārundam</i>), and the neuter singular is <i>quiddam</i> as a pronoun (something) but <i>quoddam</i> as an adjective (<i>quoddam bellum</i>, a certain war).",
  "basic": {"name": "A certain", "sec": "310",
   "rule": "<i>Quīdam</i> points to a particular person or thing without naming it. <b>With a noun</b>, as an adjective, it agrees with the noun: <i>quīdam homō</i>, a certain man. "
           "<b>On its own</b>, as a pronoun: <i>quīdam</i>, a certain man, someone; <i>quaedam</i>, a certain woman; <i>quiddam</i>, a certain thing.",
   "how": "Spot the <i>-dam</i> on the end, read the rest as a form of <i>quī</i>, and translate a certain.",
   "ex": [["**quīdam** homō", "a certain man", ""],
          ["**Quendam** vīdī.", "I saw a certain man.", ""],
          ["habitant hīc **quaedam** mulierēs pauperculae", "some poor women live here", "Ter. Ad. 647"]]},
  "uses": [
   {"name": "Plural: some, a few", "sec": "310", "lvl": "core",
    "what": "In the plural, <i>quīdam</i> often just means some, certain ones: particular people, but the speaker isn't listing them.",
    "clue": "A plural <i>quīdam, quaedam</i>, often with <i>ex</i> or <i>dē</i> + the group.",
    "ex": [["**quīdam** ex mīlitibus", "some of the soldiers", ""]]},
   {"name": "A sort of", "sec": "310", "lvl": "adv",
    "what": "With an adjective, <i>quīdam</i> can soften it, the way English says a sort of, a kind of, so to speak.",
    "clue": "<i>Quīdam</i> next to an adjective describing something unusual.",
    "ex": [["incrēdibilis **quaedam** magnitūdō", "a sort of incredible size", ""]]},
  ]},
]

# ---------- quis after sī, quisquam, quisque, quisquis, quīcumque (A&G §§149, 151, 310–313) ----------
INDEF += [
 {"id": "indef-quis", "name": "Quis after sī, nisi, num, nē", "q": "anyone, anything", "prons": ["quisindef"], "secs": "149, 310.a",
  "summary": "On its own, <i>quis</i> asks a question: who? But after <i>sī</i> (if), <i>nisi</i> (unless), <i>num</i> (whether) and <i>nē</i> (so that not), the same word means anyone, and <i>quid</i> means anything. "
             "This is the vaguest of the indefinites: anyone at all, whoever it may be. Students often remember it with a rhyme: after <i>sī, nisi, num</i> and <i>nē</i>, all the <i>ali-</i>s go away. "
             "That is, Latin says <i>sī quis</i>, not <i>sī aliquis</i>, for if anyone.",
  "extra": SCALE("quis"),
  "pattern": "<b>Pattern:</b> the forms are those of the interrogative <i>quis</i>, with one change: the feminine singular and the neuter plural are usually <i>qua</i>, not <i>quae</i> (<i>sī qua</i>, if any woman; <i>nē qua</i>, so that no things). The feminine nominative plural stays <i>quae</i>. As an adjective, the masculine is often <i>quī</i> and the neuter <i>quod</i>: <i>sī quod bellum</i>, if any war.",
  "basic": {"name": "Anyone, anything", "sec": "310.a",
   "rule": "When a form of <i>quis</i> comes right after <i>sī, nisi, num</i> or <i>nē</i>, translate it anyone or anything, not who or what. With <i>nē</i>, the English usually comes out as no one or nothing: <i>nē quis</i>, so that no one.",
   "how": "Look at the word in front. If it is <i>sī, nisi, num</i> or <i>nē</i>, the <i>quis</i> after it is indefinite.",
   "ex": [["Sī **quis** vēnerit, mē vocā.", "If anyone comes, call me.", ""],
          ["Nē **quid** dīxerīs.", "Don't say anything.", ""],
          ["Rogō num **quis** adsit.", "I ask whether anyone is here.", ""]]},
  "uses": [
   {"name": "Who? or anyone?", "sec": "149.b", "lvl": "core",
    "what": "The same spellings serve as the question word and as anyone. The words in front decide. At the start of a question, <i>quis</i> asks who; after <i>sī, nisi, num, nē</i>, it means anyone.",
    "clue": "Is there a question mark, or is there <i>sī, nisi, num</i> or <i>nē</i> just before?",
    "ex": [["**Quis** vēnit?", "Who came?", ""], ["Sī **quis** vēnit,", "If anyone came,", ""]]},
   {"name": "Aliquis after sī", "sec": "310.a", "lvl": "adv",
    "what": "Sometimes a writer keeps <i>aliquis</i> after <i>sī</i> or <i>nisi</i> to stress that it is someone real: <i>nisi alicui suōrum negōtium daret</i>, unless he gave the job to one of his friends.",
    "clue": "<i>Sī aliquis</i> or <i>nisi aliquis</i>: someone, said with more weight.",
    "ex": [["nisi **alicui** suōrum negōtium daret", "unless he were to give the task to one of his friends", "A&G §310.a"]]},
  ]},

 {"id": "indef-quisquam", "name": "Quisquam, quidquam", "q": "anyone at all, anything at all", "prons": ["quisquam", "ullus"], "secs": "151.d, 311–312",
  "summary": "<i>Quisquam, quidquam</i> means anyone at all, anything at all, and it belongs in sentences that say no one or nothing: <i>nec quisquam vēnit</i>, and no one came. "
             "It is <i>quis</i> with <i>-quam</i> on the end, and it has no feminine and no plural. When Latin needs any with a noun, or a plural, it uses <i>ūllus, ūlla, ūllum</i>, which is shown next to it here. "
             "English works the same way: we say I didn't see anyone, not I didn't see someone.",
  "extra": SCALE("quisquam"),
  "pattern": "<b>Pattern:</b> <i>quis</i> + <i>-quam</i>, singular only: <i>quisquam, cuiusquam, cuiquam, quemquam, quōquam</i>, neuter <i>quidquam</i> (also spelled <i>quicquam</i>). Its partner <i>ūllus</i> is an ordinary <i>-us, -a, -um</i> adjective except for the genitive <i>ūllīus</i> and dative <i>ūllī</i>, like the other <a href=\"pronouns-unus-nauta.html\">ūnus nauta</a> words.",
  "basic": {"name": "Anyone at all, in a negative sentence", "sec": "311",
   "rule": "Use <i>quisquam</i> (on its own) and <i>ūllus</i> (with a noun) when the sentence says no one, nothing, never or without. Translate them anyone and any. Latin keeps <i>aliquis</i> for sentences where someone does exist: <i>nōn sine aliquō metū</i>, not without some fear, but <i>sine ūllō metū</i>, without any fear at all.",
   "how": "Look for a negative nearby: <i>nōn, numquam, nec, vix, sine</i>, or a question that expects the answer no.",
   "ex": [["Iūstitia numquam nocet **cuiquam**.", "Justice never harms anyone.", "Cic. Fin. 1.50"],
          ["sine **ūllō** metū", "without any fear", "A&G §311"],
          ["Nec **quidquam** dīxit.", "And he said nothing.", ""]]},
  "uses": [
   {"name": "Questions that expect no", "sec": "311", "lvl": "core",
    "what": "A question that really means no one can use <i>quisquam</i>: is there anyone who would believe this? (No, there isn't.)",
    "clue": "A question with <i>num</i> or a scornful tone, plus <i>quisquam</i> or <i>ūllus</i>.",
    "ex": [["Num **quisquam** hoc crēdit?", "Surely no one believes this?", ""]]},
   {"name": "If anyone at all", "sec": "311", "lvl": "core",
    "what": "After <i>sī</i>, <i>quisquam</i> is stronger than <i>quis</i>: if anyone at all, if anyone ever.",
    "clue": "<i>Sī quisquam</i>.",
    "ex": [["Sī **quisquam**, ille sapiēns fuit.", "If anyone was ever wise, he was.", "A&G §311"]]},
   {"name": "No one: nēmō, nūllus", "sec": "311", "lvl": "core",
    "what": "To say no one or none outright, Latin has its own words: <i>nēmō</i> (no one) and <i>nūllus</i> (no, none). <i>Nec quisquam</i> (and no one) is used instead of <i>et nēmō</i>.",
    "clue": "<i>Nec</i> + <i>quisquam</i> = and no one.",
    "ex": [["**Nēmō** vēnit.", "No one came.", ""], ["nec **quisquam** respondit", "and no one answered", ""]]},
  ]},

 {"id": "indef-quisque", "name": "Quisque, quidque", "q": "each, every", "prons": ["quisque"], "secs": "151.g, 313",
  "summary": "<i>Quisque</i> means each one, every one, and the adjective <i>quīque, quaeque, quodque</i> means each, every. "
             "It is <i>quis</i> with <i>-que</i> on the end, so watch that you don't read that <i>-que</i> as and. "
             "It usually comes right after the word it goes with, often a reflexive (<i>suus, sē</i>) or a superlative: <i>suum cuique</i>, to each his own.",
  "extra": "",
  "pattern": "<b>Pattern:</b> <i>quis</i> + <i>-que</i>, with every case of <i>quis</i> and <i>quī</i> underneath: <i>cuiusque, cuique, quemque, quōque</i>. The neuter is <i>quidque</i> (also spelled <i>quicque</i>) on its own and <i>quodque</i> with a noun. The plural is rare.",
  "basic": {"name": "Each, every", "sec": "313",
   "rule": "Translate <i>quisque</i> each or every, and expect it to sit just after the word it goes with. It is common with a reflexive pronoun or possessive: <i>sua quemque fortūna</i>, each man's own fortune.",
   "how": "Cover the <i>-que</i>. If what is left is a form of <i>quis</i> or <i>quī</i>, the word is <i>quisque</i>, not and.",
   "ex": [["**suum cuique**", "to each his own", ""],
          ["**Quisque** suam domum petit.", "Each man heads for his own home.", ""],
          ["**ūnusquisque** vestrum", "every single one of you", ""]]},
  "uses": [
   {"name": "With a superlative: all the best", "sec": "313", "lvl": "core",
    "what": "<i>Quisque</i> with a superlative means all the ___est people, taken one by one: <i>nōbilissimus quisque</i>, all the noblest men. English uses a plural.",
    "clue": "A superlative (<i>-issimus, optimus</i>) with <i>quisque</i>.",
    "ex": [["**optimus quisque**", "all the best men", ""], ["**nōbilissimus quisque**", "all the noblest, one after another", "A&G §313"]]},
   {"name": "With an ordinal: every tenth", "sec": "313", "lvl": "core",
    "what": "With an ordinal number, <i>quisque</i> picks one out of every so many: <i>decimus quisque</i>, every tenth man, one in ten. <i>Prīmō quōque tempore</i> means at the first chance.",
    "clue": "<i>Prīmus, decimus</i> and other ordinals with <i>quisque</i>.",
    "ex": [["**decimus quisque**", "one in ten", "A&G §313"], ["**prīmō quōque** tempore", "at the earliest opportunity", "A&G §313"]]},
   {"name": "The more …, the more …", "sec": "313", "lvl": "adv",
    "what": "Two superlatives with <i>quisque</i> set up a proportion: the wiser a man is, the calmer he is. <i>Quō quisque … hōc …</i> works the same way with comparatives.",
    "clue": "Two superlatives, or <i>quō … hōc</i>, in one sentence with <i>quisque</i>.",
    "ex": [["Sapientissimus **quisque** aequissimō animō moritur.", "The wiser a man is, the more calmly he dies.", "A&G §313"]]},
  ]},

 {"id": "indef-quisquis", "name": "Quisquis, quidquid", "q": "whoever, whatever", "prons": ["quisquis"], "secs": "151.a",
  "summary": "<i>Quisquis, quidquid</i> means whoever, whatever. Like the relative <i>quī</i>, it starts a clause, but it doesn't point back to a person already named: it means anyone at all who fits. "
             "It is <i>quis</i> said twice, and both halves change: <i>quemquem, quōquō</i>. In practice you will meet only a few forms: <i>quisquis</i>, <i>quidquid</i> and <i>quōquō</i>. "
             "For the other cases, Latin uses <a href=\"pronouns-quicumque.html\"><i>quīcumque</i></a>.",
  "extra": WHO("ever"),
  "pattern": "<b>Pattern:</b> <i>quis</i> doubled, both halves declined. Only <i>quisquis</i>, <i>quidquid</i> (also spelled <i>quicquid</i>) and <i>quōquō</i> are common. The rest are rare or missing, shown here with a dash, and the feminine hardly exists. <i>Quisquis</i> is usually a pronoun (whoever); <i>quōquō</i> is usually an adjective (<i>quōquō modō</i>, in whatever way).",
  "basic": {"name": "Whoever, whatever", "sec": "151.a",
   "rule": "<i>Quisquis</i> begins a clause that describes anyone or anything that fits, without saying who or what: whoever, whatever. The clause usually comes first, and the main sentence follows.",
   "how": "A doubled form at the start of a clause: <i>quisquis, quidquid, quōquō</i>.",
   "ex": [["**Quisquis** es, salvē.", "Whoever you are, hello.", ""],
          ["**quidquid** id est, timeō Danaōs et dōna ferentēs", "whatever it is, I fear the Greeks even when they bring gifts", "Verg. A. 2.49"],
          ["**quōquō** modō", "in whatever way", ""]]},
  "uses": [
   {"name": "Quisquis or quīcumque?", "sec": "151", "lvl": "core",
    "what": "Both mean whoever, whatever. <i>Quisquis</i> is mostly a pronoun and has only a few forms; <i>quīcumque</i> has every form and is the usual choice with a noun: <i>quācumque ratiōne</i>, by whatever means.",
    "clue": "On its own: often <i>quisquis</i>. With a noun, or in the dative or genitive: <i>quīcumque</i>.",
    "ex": [["**quidquid** agis", "whatever you do", ""], ["**quācumque** ratiōne", "by whatever means", ""]]},
  ]},

 {"id": "indef-quicumque", "name": "Quīcumque, quaecumque, quodcumque", "q": "whoever, whatever; any … that", "prons": ["quicumque"], "secs": "151",
  "summary": "<i>Quīcumque, quaecumque, quodcumque</i> means whoever, whatever, or any … that. It is the relative <i>quī, quae, quod</i> with <i>-cumque</i> on the end (A&amp;G §151), so it starts a clause like a relative, "
             "but it doesn't point back to one person already named: it means anyone or anything at all that fits. "
             "The same ending makes other whatever-words: <i>ubicumque</i>, wherever; <i>quāliscumque</i>, of whatever kind.",
  "extra": WHO("ever"),
  "pattern": "<b>Pattern:</b> <i>quī, quae, quod</i> + <i>-cumque</i>. Every form is a form of the relative with <i>-cumque</i> added: <i>cuiuscumque, quemcumque, quibuscumque</i>. Cover the <i>-cumque</i> and read the rest as <i>quī</i>.",
  "basic": {"name": "Whoever, whatever", "sec": "151",
   "rule": "<i>Quīcumque</i> begins a clause about anyone or anything that fits. On its own it means whoever or whatever; with a noun it means whatever ___ or any ___ that: <i>quaecumque rēs</i>, whatever thing, anything that.",
   "how": "Look for <i>-cumque</i> on a form of <i>quī</i>.",
   "ex": [["**Quīcumque** vēnerit, eum accipiam.", "Whoever comes, I will welcome him.", ""],
          ["**quācumque** ratiōne", "by whatever means", ""],
          ["**quaecumque** vīs", "whatever things you want", ""]]},
  "uses": [
   {"name": "Other -cumque words", "sec": "151", "lvl": "core",
    "what": "<i>-Cumque</i> turns other relative words into whatever-words: <i>ubi</i> (where) becomes <i>ubicumque</i> (wherever), <i>quālis</i> (of which kind) becomes <i>quāliscumque</i> (of whatever kind), <i>quandō</i> (when) becomes <i>quandōcumque</i> (whenever).",
    "clue": "Any word ending in <i>-cumque</i> means -ever.",
    "ex": [["**ubicumque** es", "wherever you are", ""]]},
  ]},
]
