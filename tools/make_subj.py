"""Subjunctive pages: four tense pages (present, imperfect, perfect, pluperfect; active and passive on each),
an overview of the mood, and a page of its uses. Same layout as the indicative tense pages.
Usage: python3 make_subj.py SITE_DIR"""
import os, re, sys
from verb_build import formula, piece, PERS

SITE = sys.argv[1]
V_CSS, V_CHART, V_MORE = '202610150900', '202610150900', '202610142000'

md = lambda s: re.sub(r'\*\*(.+?)\*\*', r'<b class="hl">\1</b>', s)
TV = lambda la: re.sub(r'\[(.)\]', r'<b class="tv">\1</b>', la)

def exs(rows, big=False):
    return (f'<div class="exs{" big" if big else ""}">' + ''.join(
        f'<div class="ex"><div class="la" lang="la">{md(la)}</div><div class="en">{en}{f" <span class=src>{src}</span>" if src else ""}</div></div>'
        for la, en, src in rows) + '</div>')

def block(title, inner, cls=''):
    return f'  <div class="block{" " + cls if cls else ""}">\n    <h3>{title}</h3>\n    {inner}\n  </div>\n'

def use_card(u):
    return (f'<article class="use"><header><h4>{u["name"]}</h4><span class="sec">A&amp;G §{u["sec"]}</span></header>'
            f'<p class="what">{u["what"]}</p><p class="clue"><b>Clue:</b> {u["clue"]}</p>{exs(u["ex"])}</article>')

def head(title, style=''):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,400;0,600;0,700;1,400;1,600;1,700&display=swap">
<link rel="stylesheet" href="../css/grammar.css?v=202610071800">
<link rel="stylesheet" href="../css/grammar-verbs.css?v={V_CSS}">
<style>
{style}
</style>
<link rel="stylesheet" href="../css/sidebar.css?v=202610180900">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,600;8..60,700&display=swap">
<link rel="stylesheet" href="../css/theme.css?v=202610180950">
</head>
<body>
<div class="wrap">
<header>
  <h1>{title}</h1>
</header>
'''

def foot(secs, chart_js='', more=False):
    s = secs if isinstance(secs, str) else ', '.join(map(str, secs))
    many = '§§' if (',' in s or '–' in s) else '§'
    out = f'''
<footer class="cite">
  <h4>Sources</h4>
  <p>Paradigms follow J. H. Allen and J. B. Greenough, <i>Allen and Greenough's New Latin Grammar for Schools and Colleges</i> (Boston: Ginn &amp; Co., 1903), in the <a href="https://dcc.dickinson.edu/grammar/latin" target="_blank" rel="noopener">Dickinson College Commentaries online edition</a>. Uses follow A&amp;G {many}{s}.</p>
</footer>
</div>

'''
    if chart_js:
        out += f'<script src="../js/verb-chart.js?v={V_CHART}"></script>\n<script>\n{chart_js}\n</script>\n'
    out += '<script src="../js/common.js?v=202610011900"></script>\n'
    if more: out += f'<script src="../js/more-charts.js?v={V_MORE}"></script>\n'
    out += ('<script src="../js/account.js?v=202610122000"></script>\n<script src="../js/levels.js?v=202610172240"></script>\n'
            '<script src="../js/sidebar.js?v=202610180945"></script>\n<script src="../js/glossary.js?v=202610131500"></script>\n')
    if chart_js: out += '<script src="../js/pattern-notes.js?v=202610180900"></script>\n<script src="../js/hovercard.js?v=202610180900"></script>\n'
    return out + '</body>\n</html>'

# ---------------------------------------------------------------- the sequence grid
TENSES = [  # id, page, name, latin (3rd sg active), how it is built, row, column
    ('pres', 'subjunctive-present', 'Present subjunctive', 'am[e]t', 'the stem with a changed vowel', 0, 0),
    ('impf', 'subjunctive-imperfect', 'Imperfect subjunctive', 'amāret', 'the infinitive + an ending', 0, 1),
    ('perf', 'subjunctive-perfect', 'Perfect subjunctive', 'amāverit', 'the complete stem + <i>-eri-</i>', 1, 0),
    ('plup', 'subjunctive-pluperfect', 'Pluperfect subjunctive', 'amāvisset', 'the perfect infinitive + an ending', 1, 1)]

def seq_grid(cur=None, caption='Which subjunctive tense?'):
    out = [f'<figure class="ta seq"><figcaption>{caption}</figcaption><div class="ta-grid"><span class="ta-corner"></span>',
           '<span class="ta-col">Primary sequence<span class="ta-sub">after a present or future main verb</span></span>',
           '<span class="ta-col">Secondary sequence<span class="ta-sub">after a past main verb</span></span>']
    rows = [('Incomplete', 'the action happens at the same time as the main verb, or later'),
            ('Complete', 'the action happened before the main verb')]
    for r, (lab, desc) in enumerate(rows):
        out.append(f'<span class="ta-row"><b>{lab}</b><br>{desc}</span>')
        for tid, page, name, la, how, rr, cc in TENSES:
            if rr != r: continue
            inner = f'<span class="nm">{name}</span><span class="la" lang="la">{TV(la)}</span><span class="eg">{how}</span>'
            if tid == cur:
                out.append(f'<span class="ta-c on" aria-current="page"><span class="here">This page</span>{inner}</span>')
            else:
                out.append(f'<a class="ta-c" href="{page}.html">{inner}</a>')
    out.append('</div></figure>')
    return ''.join(out)

# ---------------------------------------------------------------- tense pages
TOOLBAR = '''
<section id="charts">
  <div class="toolbar">
    <div class="tb-row" id="patterns"><span class="tb-label">Highlight a pattern</span></div>
    <div class="tb-row">
      <span class="tb-label">View</span>
      <div class="seg">
      <button class="chip plain" id="t-mac" aria-pressed="true">Show macrons (ā ē ī ō ū)</button>
      <button class="chip plain" id="t-end" aria-pressed="false">Emphasize endings</button>
      <button class="chip plain" id="t-en" aria-pressed="false">Show English</button>
      </div>
    </div>
    <div class="pnotes" id="pnotes"></div>
  </div>
'''

def work(more_note, er_title, er_text):
    attrs = f' data-show="amo" data-more-note="{more_note}"' if more_note else ''
    return f'''  <div class="block">
    <h3>The forms</h3>
  <div class="work">
    <div class="charts-col" id="charts-col"{attrs}>
      <div class="charts three-up" id="charts-grid"></div>
      <div class="er er-open" id="er">
        <h4 class="er-h">{er_title}</h4>
        <div class="prose"><p>{er_text}</p></div>
        <div class="charts one-up" id="er-grid"></div>
      </div>
    </div>
    <aside class="panel" aria-live="polite"><div class="card" id="card"></div></aside>
  </div>
  </div>
'''

def bd_table(rows_act, rows_pass, two_word=False):
    def cell(seg):
        s, m, e = seg
        if two_word:
            return f'<td lang="la"><span class="bd-s">{s}</span> <span class="bd-e">{e}</span></td>'
        return f'<td lang="la">{piece(s, m, e)}</td>'
    rows = ''.join(f'<tr><td class="bd-p">{PERS[i]}</td>{cell(rows_act[i])}{cell(rows_pass[i])}</tr>' for i in range(6))
    return ('<div class="bd-table"><table><thead><tr><th>Person</th><th>Active</th><th>Passive</th></tr></thead><tbody>'
            + rows + '</tbody></table></div>')

def subj_key(marker):
    return (f'<p class="bd-key"><span class="bd-s">stem</span>: aspect · <span class="bd-m">{marker}</span>: the subjunctive · '
            '<span class="bd-e">personal ending</span>: person and number, and voice.</p>')

ACT = ['m', 's', 't', 'mus', 'tis', 'nt']
PAS = ['r', 'ris', 'tur', 'mur', 'minī', 'ntur']
SUMP = ['sim', 'sīs', 'sit', 'sīmus', 'sītis', 'sint']
SUMI = ['essem', 'essēs', 'esset', 'essēmus', 'essētis', 'essent']

PAGES = {}

# ---- present
PAGES['subjunctive-present'] = dict(
  cur='pres', title='Present Subjunctive', q='amet: may love, let him love', secs='439–446, 483',
  summary='The present subjunctive is the incomplete subjunctive of primary sequence. In a main clause it gives an encouragement, a command, a doubtful question or a possibility: '
          '<i>amēmus</i>, "let us love." In a dependent clause after a present or future main verb, it describes an action at the same time as the main verb or later: '
          '<i>rogō quid amet</i>, "I ask what he loves." It has no single English translation; the use decides.',
  more=None,
  er=('Irregular: <i>sum, esse</i> (to be)', '<i>sum</i> uses <i>i</i> instead of <i>e</i> or <i>a</i>: <i>sim, sīs, sit, sīmus, sītis, sint</i>. <i>possum</i> follows it: <i>possim, possit</i>.'),
  build=('<p>Change the vowel after the stem, then add the personal endings. In the 1st conjugation the <i>ā</i> of the stem becomes <i>e</i> (<i>amā-</i> → <i>ame-</i>). '
         'The other conjugations put <i>a</i> after the stem (<i>monea-, rega-, capia-, audia-</i>). The 1st singular ends in <i>-m</i> in the active and <i>-r</i> in the passive, '
         'as in the imperfect indicative. Many students remember the vowels with the phrase "we fear a liar": <i>e</i> for the 1st conjugation, <i>ea</i> for the 2nd, <i>a</i> for the 3rd, <i>ia</i> for the 3rd <i>-iō</i> and 4th.</p>',
         formula('stem', 'am', 'e', 't', 'amet', 'he may love', 'subjunctive vowel') + subj_key('subjunctive vowel')
         + bd_table([('am', v, e) for v, e in zip(['e', 'ē', 'e', 'ē', 'ē', 'e'], ACT)], [('am', v, e) for v, e in zip(['e', 'ē', 'ē', 'ē', 'ē', 'e'], PAS)])
         + '<p class="bd-note">The vowel is long except before <i>-m</i>, <i>-t</i>, <i>-nt</i>, final <i>-r</i> and <i>-ntur</i>.</p>'),
  basic=dict(name='after a present or future main verb', sec='483',
     rule='In a dependent clause after a present or future main verb, the present subjunctive shows an action at the same time as the main verb or later. '
          'Translate it with an ordinary English present or future, not with "may": <i>rogō quid faciat</i>, "I ask what he is doing."',
     how='Look for the changed vowel before the ending: <i>e</i> in the 1st conjugation (<i>amet</i>), <i>a</i> in the others (<i>moneat, regat, capiat, audiat</i>).',
     ex=[('Rogō quid **faciās**.', 'I ask what you are doing.', ''), ('Scrībit ut nōs **moneat**.', 'He writes to warn us.', ''),
         ('Nescit cūr puella **lacrimet**.', "He doesn't know why the girl is crying.", '')]),
  uses=[dict(name='Encouragements and commands', sec='439',
             what='This is the subjunctive\'s oldest meaning: the speaker\'s will. The 1st person plural encourages ("let us ..."), and the 3rd person gives a command ("let him ...," "he is to ..."). The negative is <i>nē</i>.',
             clue='A present subjunctive is the main verb, often at the start of the sentence.',
             ex=[('**Vīvāmus**, mea Lesbia, atque **amēmus**.', 'Let us live, my Lesbia, and let us love.', 'Catullus 5.1'), ('Nē **timeant**.', 'Let them not be afraid.', '')]),
        dict(name='Doubtful questions', sec='444',
             what='A question in the subjunctive asks what should be done. It began as a request to learn someone\'s will ("what do you want me to do?") and came to express doubt, frustration or impossibility. English uses "am I to" or "should I." The negative is <i>nōn</i>.',
             clue='A question whose main verb is subjunctive, usually in the 1st person.',
             ex=[('Quid **agam**, iūdicēs?', 'What am I to do, judges?', '')]),
        dict(name='Possibility', sec='446',
             what='The subjunctive can present an action as something that could happen, not as a fact or a wish. English uses "may," "might," "would" or "could," whichever fits. The negative is <i>nōn</i>.',
             clue='A subjunctive main verb, often with an indefinite subject such as <i>aliquis</i>, or with "you" meaning anyone.',
             ex=[('**Dīcat** aliquis.', 'Someone may say.', ''), ('Fortūnam citius **reperiās** quam **retineās**.', 'You could find good fortune sooner than you could keep it.', '')]),
        dict(name='Wishes that may come true', sec='441',
             what='The present subjunctive wishes for something that can still happen. It may have <i>utinam</i>; the negative is <i>nē</i>. English uses "may" or "I hope that."',
             clue='<i>Utinam</i>, or a wish such as "may the gods ..." with a present subjunctive.',
             ex=[('Dī tē **servent**!', 'May the gods keep you safe!', '')])],
  forms=None,
)

# ---- imperfect
PAGES['subjunctive-imperfect'] = dict(
  cur='impf', title='Imperfect Subjunctive', q='amāret: might love, would love', secs='441, 446, 483, 517, 546',
  summary='The imperfect subjunctive is the incomplete subjunctive of secondary sequence. In a dependent clause after a past main verb, it describes an action at the same time as '
          'the main verb or later: <i>rogāvī quid amāret</i>, "I asked what he loved." On its own it expresses a wish or a condition that is not true now: <i>utinam adesset</i>, '
          '"if only he were here." It is the most common subjunctive in stories.',
  more='Every conjugation builds this tense the same way: the present infinitive plus the personal endings.',
  er=('Irregular: <i>sum, esse</i> (to be)', 'The rule works for irregular verbs too: <i>esse</i> gives <i>essem</i>, <i>posse</i> gives <i>possem</i>, <i>ferre</i> gives <i>ferrem</i>.'),
  build=('<p>Take the present infinitive, the 2nd principal part (<i>amāre, monēre, regere, capere, audīre</i>), and add the personal endings. '
         'The <i>e</i> of <i>-re-</i> is long before most endings (<i>amārēs, amārētur</i>) and short before <i>-m</i>, <i>-t</i>, <i>-nt</i>, final <i>-r</i> and <i>-ntur</i>.</p>',
         formula('stem', 'amā', 're', 't', 'amāret', 'he might love', 'from the infinitive') + subj_key('-re- from the infinitive')
         + bd_table([('amā', m, e) for m, e in zip(['re', 'rē', 're', 'rē', 'rē', 're'], ACT)], [('amā', m, e) for m, e in zip(['re', 'rē', 'rē', 'rē', 'rē', 're'], PAS)])),
  basic=dict(name='after a past main verb', sec='483',
     rule='In a dependent clause after a past main verb, the imperfect subjunctive shows an action at the same time as the main verb or later. '
          'Translate it with an English past tense, not with "might": <i>rogāvī quid faceret</i>, "I asked what he was doing."',
     how='Look for the present infinitive with a personal ending on it: <i>amāre-t, regere-t, audīre-t</i>; for <i>sum</i>, <i>esse-t</i>.',
     ex=[('Rogāvī quid **facerēs**.', 'I asked what you were doing.', ''), ('Scrīpsit ut nōs **monēret**.', 'He wrote to warn us.', ''),
         ('Tam fessus erat ut **dormīret**.', 'He was so tired that he fell asleep.', '')]),
  uses=[dict(name='"When" with cum', sec='546',
             what='<i>Cum</i> with the indicative dates an action: it says when it happened. With the imperfect subjunctive it describes the situation at the time instead. '
                  'English makes the same distinction without a change of form: "he had a fever when he was in Spain" dates the fever, but "Columbus found America when he was looking for India" describes his situation.',
             clue='<i>Cum</i> followed by an imperfect subjunctive, with a past main verb.',
             ex=[('Cum **essem** ōtiōsus in Tusculānō, accēpī tuās litterās.', 'While I was at leisure at my house in Tusculum, I received your letter.', 'Cicero, Ad Fam. 9.18')]),
        dict(name='Wishes that are not true now', sec='441',
             what='The imperfect subjunctive wishes that the present were different, and implies that it is not. <i>Utinam</i> regularly comes first. English uses "if only" or "I wish" with a past form.',
             clue='<i>Utinam</i> with an imperfect subjunctive.',
             ex=[('Utinam **adesset**!', 'If only he were here!', '')]),
        dict(name='Possibility in the past', sec='446',
             what='The imperfect subjunctive can say what could have been the case in the past, often with "you" meaning anyone. English uses "would have" or "could have."',
             clue='An imperfect subjunctive main verb, often 2nd person singular, with no signal word.',
             ex=[('**Crēderēs** victōs.', 'You would have thought them defeated.', '')]),
        dict(name='Conditions that are not true now', sec='517',
             what='In "if" sentences about the present, the imperfect subjunctive in both halves says that the condition is not true. English uses "if ... were" and "would."',
             clue='<i>Sī</i> with an imperfect subjunctive in both halves of the sentence.',
             ex=[('Sī **adessēs**, **gaudērem**.', 'If you were here, I would be glad.', '')])],
  forms=('', [('<i>forem, forēs, foret, forent</i> are used for <i>essem, essēs, esset, essent</i>, especially in poetry.', 'foret', 'esset')]),
)

# ---- perfect
PAGES['subjunctive-perfect'] = dict(
  cur='perf', title='Perfect Subjunctive', q='amāverit: may have loved', secs='450, 483',
  summary='The perfect subjunctive is the complete subjunctive of primary sequence. In a dependent clause after a present or future main verb, it describes an action earlier than '
          'the main verb: <i>rogō quid amāverit</i>, "I ask what he loved." In a main clause it gives a prohibition with <i>nē</i>: <i>nē timueris</i>, "don\'t be afraid."',
  more='Every conjugation builds this tense the same way.',
  er=('Irregular: <i>sum, esse</i> (to be)', '<i>sum</i> is regular here: the stem <i>fu-</i> plus <i>-erim</i>, <i>fuerim, fuerīs, fuerit</i>.'),
  build=('<p>Take the complete stem, the 3rd principal part minus <i>-ī</i>, and add <i>-eri-</i> with the personal endings: <i>amāv-eri-t</i>. '
         'These forms look like the future perfect, except in the 1st singular (<i>amāverim</i>, not <i>amāverō</i>). '
         'The passive is the perfect participle with the present subjunctive of <i>sum</i>: <i>amātus sim, amātus sit</i>.</p>',
         formula('complete stem', 'amāv', 'eri', 't', 'amāverit', 'he may have loved', 'subjunctive marker') + subj_key('-eri-')
         + bd_table([('amāv', m, e) for m, e in zip(['eri', 'erī', 'eri', 'erī', 'erī', 'eri'], ACT)],
                    [('amāt' + ('us' if i < 3 else 'ī'), '', SUMP[i]) for i in range(6)], two_word=False)
         .replace('<span class="bd-s">amātus</span><span class="bd-e">', '<span class="bd-s">amātus</span> <span class="bd-e">')
         .replace('<span class="bd-s">amātī</span><span class="bd-e">', '<span class="bd-s">amātī</span> <span class="bd-e">')),
  basic=dict(name='after a present or future main verb', sec='483',
     rule='In a dependent clause after a present or future main verb, the perfect subjunctive shows an action earlier than the main verb. '
          'Translate it with an English past or "has ___ed": <i>rogō quid fēcerit</i>, "I ask what he did" or "what he has done."',
     how='Look for the complete stem with <i>-eri-</i> before the ending (<i>amāverit, monuerit, rēxerit</i>), or a participle with <i>sim, sīs, sit</i>.',
     ex=[('Rogō quid **fēcerit**.', 'I ask what he did.', ''), ('Nesciō cūr **vēnerint**.', "I don't know why they came.", '')]),
  uses=[dict(name='Prohibitions', sec='450',
             what='Latin forbids an action in three ways: <i>nōlī</i> with an infinitive (the usual way), <i>cavē</i> with the present subjunctive, or <i>nē</i> with the perfect subjunctive, which is blunter. In a prohibition the perfect does not refer to the past.',
             clue='<i>Nē</i> with a 2nd person perfect subjunctive as the main verb.',
             ex=[('Nē **timueris**.', "Don't be afraid.", '')])],
  forms=('Roman writers often shortened the perfect subjunctive, as they did the perfect indicative (A&amp;G §181).',
         [('<i>-ve-</i> is dropped after a long vowel.', 'amārit · amārint', 'amāverit · amāverint')]),
)

# ---- pluperfect
PAGES['subjunctive-pluperfect'] = dict(
  cur='plup', title='Pluperfect Subjunctive', q='amāvisset: had loved, would have loved', secs='441, 483, 517, 546',
  summary='The pluperfect subjunctive is the complete subjunctive of secondary sequence. In a dependent clause after a past main verb, it describes an action earlier than '
          'the main verb: <i>rogāvī quid amāvisset</i>, "I asked what he had loved." It also expresses things that did not happen: a wish about the past and the past '
          'contrary-to-fact condition.',
  more='Every conjugation builds this tense the same way.',
  er=('Irregular: <i>sum, esse</i> (to be)', '<i>sum</i> is regular here: the perfect infinitive <i>fuisse</i> plus the endings, <i>fuissem, fuissēs, fuisset</i>.'),
  build=('<p>Take the perfect active infinitive (<i>amāvisse</i>: the complete stem plus <i>-isse</i>) and add the personal endings: <i>amāvisse-t</i>. '
         'The passive is the perfect participle with the imperfect subjunctive of <i>sum</i>: <i>amātus essem, amātus esset</i>.</p>',
         formula('complete stem', 'amāv', 'isse', 't', 'amāvisset', 'he had loved', 'from the infinitive') + subj_key('-isse-')
         + bd_table([('amāv', m, e) for m, e in zip(['isse', 'issē', 'isse', 'issē', 'issē', 'isse'], ACT)],
                    [('amāt' + ('us' if i < 3 else 'ī'), '', SUMI[i]) for i in range(6)])
         .replace('<span class="bd-s">amātus</span><span class="bd-e">', '<span class="bd-s">amātus</span> <span class="bd-e">')
         .replace('<span class="bd-s">amātī</span><span class="bd-e">', '<span class="bd-s">amātī</span> <span class="bd-e">')),
  basic=dict(name='after a past main verb', sec='483',
     rule='In a dependent clause after a past main verb, the pluperfect subjunctive shows an action earlier than the main verb. '
          'Translate it with "had ___ed": <i>rogāvī quid fēcisset</i>, "I asked what he had done."',
     how='Look for <i>-isse-</i> between the complete stem and the ending (<i>amāvisset, rēxisset</i>), or a participle with <i>essem, esset</i>.',
     ex=[('Rogāvī quid **fēcissēs**.', 'I asked what you had done.', ''), ('Cum id nūntiātum **esset**, mātūrat.', 'When this had been reported, he hurries.', 'Caesar, B.G. 1.7')]),
  uses=[dict(name='Wishes about the past', sec='441',
             what='The pluperfect subjunctive wishes that the past had been different, and implies that it was not. <i>Utinam</i> regularly comes first. English uses "if only ... had."',
             clue='<i>Utinam</i> with a pluperfect subjunctive.',
             ex=[('Utinam **adfuissēs**!', 'If only you had been there!', '')]),
        dict(name='Conditions that were not true', sec='517',
             what='In "if" sentences about the past, the pluperfect subjunctive in both halves says that the condition was not true. English uses "if ... had" and "would have."',
             clue='<i>Sī</i> with a pluperfect subjunctive in both halves of the sentence.',
             ex=[('Sī **vēnissēs**, tē **vīdissem**.', 'If you had come, I would have seen you.', '')])],
  forms=('Roman writers often shortened these forms too (A&amp;G §181).',
         [('<i>-vi-</i> is dropped after a long vowel.', 'amāssem · audīssem', 'amāvissem · audīvissem')]),
)

# ---------------------------------------------------------------- the charts
CHART_HEAD = '''const SUB = ['I','you','he/she/it','we','you (all)','they'];
const rep = (st, vw, signs, ends) => ends.map((e, i) => [st, vw, signs[i], e]);
const ACT = ['m','s','t','mus','tis','nt'], PAS = ['r','ris','tur','mur','minī','ntur'];
const D = {amo:['amō, amāre, amāvī, amātus','1st conjugation · love'], moneo:['moneō, monēre, monuī, monitus','2nd conjugation · warn'],
           rego:['regō, regere, rēxī, rēctus','3rd conjugation · rule'], capio:['capiō, capere, cēpī, captus','3rd conjugation -iō · take'],
           audio:['audiō, audīre, audīvī, audītus','4th conjugation · hear']};
const EN = {amo:['love','loved'], moneo:['warn','warned'], rego:['rule','ruled'], capio:['take','taken'], audio:['hear','heard']};
const IDS = ['amo','moneo','rego','capio','audio'];
const mk = (id, g, f) => ({id, group:g, dict:D[id][0], meta:D[id][1], f});
const GROUPS = [{id:'act', name:'Active'}, {id:'pass', name:'Passive'}];'''

CHARTS = {
'subjunctive-present': r'''
const STEM = {amo:['am',''], moneo:['mon','e'], rego:['reg',''], capio:['cap','i'], audio:['aud','i']};
const VA = id => id === 'amo' ? ['e','ē','e','ē','ē','e'] : ['a','ā','a','ā','ā','a'];
const VP = id => id === 'amo' ? ['e','ē','ē','ē','ē','e'] : ['a','ā','ā','ā','ā','a'];
VerbChart({
  groups: GROUPS, groupLabel: 'Voice',
  verbs: [...IDS.map(id => mk(id, 'act', rep(...STEM[id], VA(id), ACT))), ...IDS.map(id => mk(id, 'pass', rep(...STEM[id], VP(id), PAS))),
          {id:'sum', extra:true, dict:'sum, esse', meta:'irregular · be', f:rep('s','',['i','ī','i','ī','ī','i'], ACT)}],
  english: c => {
    const s = SUB[c.i];
    if(c.verb.extra) return {main:`${s} may be`, alt:''};
    const [v, pp] = EN[c.verb.id];
    return c.verb.group === 'act' ? {main:`${s} may ${v}`, alt:c.i === 3 ? `let us ${v}` : ''} : {main:`${s} may be ${pp}`, alt:''};
  },
  labels: c => ({st:'root', vw:'stem vowel', ts:'subjunctive vowel', en: c.verb.group === 'pass' ? 'passive ending' : 'personal ending'}),
  patterns: [
    {id:'e', lab:'amet', txt:'1st conjugation: ā becomes e', part:'ts', test:c=>c.verb.id === 'amo',
     note:'<b>In the 1st conjugation the subjunctive vowel is e:</b> <i>amet</i>, not the indicative <i>amat</i>. Because <i>e</i> is the 2nd conjugation\'s stem vowel, <i>amet</i> can look like a 2nd conjugation indicative. Check the dictionary form: <i>amō, amāre</i>.'},
    {id:'a', lab:'moneat, regat', txt:'other conjugations: a', part:'ts', test:c=>!['amo','sum'].includes(c.verb.id),
     note:'<b>The 2nd, 3rd and 4th conjugations put a before the ending:</b> <i>moneat, regat, capiat, audiat</i>. The 2nd conjugation keeps its <i>e</i> and the 3rd <i>-iō</i> and 4th keep their <i>i</i> in front of it.'},
    {id:'fut', lab:'regam, audiam', txt:'the same as the future for "I"', part:'all', test:c=>['rego','capio','audio'].includes(c.verb.id) && c.p.k === '1sg',
     note:'<b>Look-alike:</b> in the 3rd, 3rd <i>-iō</i> and 4th conjugations, the 1st singular present subjunctive is spelled the same as the future: <i>regam, capiam, audiam</i> (and <i>regar</i> in the passive). The other persons differ: future <i>regēs</i>, subjunctive <i>regās</i>. The sentence tells you which it is.'},
    {id:'i', lab:'sim, sit', txt:'sum: i', part:'ts', test:c=>c.verb.extra,
     note:'<b>sum uses i:</b> <i>sim, sīs, sit, sīmus, sītis, sint</i>. These forms also make the perfect passive subjunctive: <i>amātus sit</i>.'}
  ],
  notes: {
    'amo-act.1sg':'<i>am-e-m</i>: the 1st singular ends in <i>-m</i>, as in the imperfect <i>amābam</i>.',
    'amo-act.3sg':'<i>am-e-t</i>: compare the indicative <i>amat</i>. Only the vowel differs.',
    'amo-act.1pl':'<i>amēmus</i>: often "let us love."',
    'moneo-act.3sg':'<i>mone-a-t</i>: the 2nd conjugation keeps its <i>e</i>, then adds <i>a</i>.',
    'rego-act.2sg':'<i>reg-ā-s</i>: compare the future <i>regēs</i> and the present indicative <i>regis</i>.',
    'amo-pass.1sg':'<i>am-e-r</i>: the passive 1st singular ends in <i>-r</i>.'
  },
  idle: "You'll see a basic translation, and how the form is built from root, stem vowel, the subjunctive vowel and personal ending. The real translation depends on the use."
});''',
'subjunctive-imperfect': r'''
const INF = {amo:['am','ā'], moneo:['mon','ē'], rego:['reg','e'], capio:['cap','e'], audio:['aud','ī']};
VerbChart({
  groups: GROUPS, groupLabel: 'Voice',
  verbs: [...IDS.map(id => mk(id, 'act', rep(...INF[id], ['re','rē','re','rē','rē','re'], ACT))),
          ...IDS.map(id => mk(id, 'pass', rep(...INF[id], ['re','rē','rē','rē','rē','re'], PAS))),
          {id:'sum', extra:true, dict:'sum, esse', meta:'irregular · be', f:rep('es','',['se','sē','se','sē','sē','se'], ACT)}],
  english: c => {
    const s = SUB[c.i];
    if(c.verb.extra) return {main:`${s} might be`, alt:''};
    const [v, pp] = EN[c.verb.id];
    return c.verb.group === 'act' ? {main:`${s} might ${v}`, alt:`${s} would ${v}`} : {main:`${s} might be ${pp}`, alt:`${s} would be ${pp}`};
  },
  labels: c => ({st:'root', vw:'stem vowel', ts:'-re- of the infinitive', en: c.verb.group === 'pass' ? 'passive ending' : 'personal ending'}),
  patterns: [
    {id:'inf', lab:'amāre-t', txt:'the infinitive + an ending', part:'ts', test:c=>!c.verb.extra,
     note:'<b>The imperfect subjunctive is the present infinitive with the personal endings:</b> <i>amāre-t, monēre-t, regere-t, capere-t, audīre-t</i>. If you can find the infinitive inside the word, you have found the imperfect subjunctive.'},
    {id:'esse', lab:'esse-t', txt:'irregular verbs follow the rule', part:'ts', test:c=>c.verb.extra,
     note:'<b>Even irregular verbs follow the rule:</b> <i>esse-m</i>, <i>posse-m</i>, <i>ferre-m</i>, <i>īre-m</i>, <i>velle-m</i>.'},
    {id:'cap', lab:'caperet', txt:'3rd -iō: no i', part:'vw', test:c=>c.verb.id === 'capio',
     note:'<b>The 3rd -iō conjugation has no i here,</b> because its infinitive has none: <i>capere</i> gives <i>caperet</i>, just like <i>regeret</i>.'}
  ],
  notes: {
    'amo-act.3sg':'<i>amāre-t</i>: the infinitive <i>amāre</i> with the ending <i>-t</i>.',
    'amo-act.2sg':'<i>amārē-s</i>: the <i>e</i> is long before <i>-s</i>.',
    'amo-pass.3sg':'<i>amārē-tur</i>: the passive endings attach the same way.',
    'rego-act.3sg':'<i>regere-t</i>: from <i>regere</i>. Do not confuse it with the infinitive itself.'
  },
  idle: "You'll see a basic translation, and how the form is built from the infinitive and a personal ending. The real translation depends on the use."
});''',
'subjunctive-perfect': r'''
const PERF = {amo:'amāv', moneo:'monu', rego:'rēx', capio:'cēp', audio:'audīv'};
const PART = {amo:'amāt', moneo:'monit', rego:'rēct', capio:'capt', audio:'audīt'};
const SIM = ['sim','sīs','sit','sīmus','sītis','sint'];
VerbChart({
  groups: GROUPS, groupLabel: 'Voice',
  verbs: [...IDS.map(id => mk(id, 'act', rep(PERF[id], '', ['eri','erī','eri','erī','erī','eri'], ACT))),
          ...IDS.map(id => mk(id, 'pass', SIM.map((x, i) => [PART[id], i < 3 ? 'us' : 'ī', '', ' ' + x]))),
          {id:'sum', extra:true, dict:'sum, esse, fuī', meta:'irregular · be', f:rep('fu','',['eri','erī','eri','erī','erī','eri'], ACT)}],
  english: c => {
    const s = SUB[c.i];
    if(c.verb.extra) return {main:`${s} may have been`, alt:''};
    const pp = EN[c.verb.id][1];
    return c.verb.group === 'act' ? {main:`${s} may have ${pp}`, alt:''} : {main:`${s} may have been ${pp}`, alt:''};
  },
  labels: c => c.verb.group === 'pass' ? {st:'participle stem', vw:'participle ending, agreeing with the subject', ts:'', en:'present subjunctive of sum'}
                                        : {st:'complete stem', vw:'', ts:'subjunctive marker', en:'personal ending'},
  patterns: [
    {id:'eri', lab:'-eri-', txt:'complete stem + eri', part:'ts', test:c=>c.verb.group !== 'pass',
     note:'<b>The perfect subjunctive adds -eri- to the complete stem:</b> <i>amāv-eri-t, monu-eri-t, rēx-eri-t</i>. Find the 3rd principal part first.'},
    {id:'fp', lab:'amāverim / amāverō', txt:'look-alike: the future perfect', part:'en', test:c=>c.verb.group !== 'pass',
     note:'<b>Look-alike:</b> the perfect subjunctive and the future perfect indicative differ only in the 1st singular (<i>amāverim</i>, <i>amāverō</i>) and in vowel length (<i>amāverīs</i>, <i>amāveris</i>). Most texts do not mark the length, so let the sentence decide: a subjunctive needs a reason, such as <i>ut</i>, <i>cum</i> or an indirect question.'},
    {id:'sim', lab:'amātus sit', txt:'passive: participle + sim', part:'en', test:c=>c.verb.group === 'pass',
     note:'<b>The passive is the perfect participle with the present subjunctive of sum:</b> <i>amātus sim, sīs, sit</i>. As in the indicative, the present of <i>sum</i> gives a complete meaning: "may have been loved."'}
  ],
  notes: {
    'amo-act.1sg':'<i>amāv-eri-m</i>: compare the future perfect <i>amāverō</i>.',
    'amo-act.3sg':'<i>amāv-eri-t</i>: spelled like the future perfect <i>amāverit</i>.',
    'amo-pass.3sg':'<i>amātus sit</i>: a feminine subject takes <i>amāta sit</i>.'
  },
  idle: "You'll see a basic translation, and how the form is built from the complete stem, -eri- and a personal ending. The real translation depends on the use."
});''',
'subjunctive-pluperfect': r'''
const PERF = {amo:'amāv', moneo:'monu', rego:'rēx', capio:'cēp', audio:'audīv'};
const PART = {amo:'amāt', moneo:'monit', rego:'rēct', capio:'capt', audio:'audīt'};
const ESSEM = ['essem','essēs','esset','essēmus','essētis','essent'];
VerbChart({
  groups: GROUPS, groupLabel: 'Voice',
  verbs: [...IDS.map(id => mk(id, 'act', rep(PERF[id], '', ['isse','issē','isse','issē','issē','isse'], ACT))),
          ...IDS.map(id => mk(id, 'pass', ESSEM.map((x, i) => [PART[id], i < 3 ? 'us' : 'ī', '', ' ' + x]))),
          {id:'sum', extra:true, dict:'sum, esse, fuī', meta:'irregular · be', f:rep('fu','',['isse','issē','isse','issē','issē','isse'], ACT)}],
  english: c => {
    const s = SUB[c.i];
    if(c.verb.extra) return {main:`${s} had been`, alt:`${s} would have been`};
    const pp = EN[c.verb.id][1];
    return c.verb.group === 'act' ? {main:`${s} had ${pp}`, alt:`${s} would have ${pp}`} : {main:`${s} had been ${pp}`, alt:`${s} would have been ${pp}`};
  },
  labels: c => c.verb.group === 'pass' ? {st:'participle stem', vw:'participle ending, agreeing with the subject', ts:'', en:'imperfect subjunctive of sum'}
                                        : {st:'complete stem', vw:'', ts:'-isse- of the perfect infinitive', en:'personal ending'},
  patterns: [
    {id:'isse', lab:'amāvisse-t', txt:'the perfect infinitive + an ending', part:'ts', test:c=>c.verb.group !== 'pass',
     note:'<b>The pluperfect subjunctive is the perfect active infinitive with the personal endings:</b> <i>amāvisse-t, monuisse-t, rēxisse-t</i>. The same idea as the imperfect subjunctive, one step back in time.'},
    {id:'essem', lab:'amātus esset', txt:'passive: participle + essem', part:'en', test:c=>c.verb.group === 'pass',
     note:'<b>The passive is the perfect participle with the imperfect subjunctive of sum:</b> <i>amātus essem, essēs, esset</i>. The imperfect of <i>sum</i> gives the meaning "had been loved."'}
  ],
  notes: {
    'amo-act.3sg':'<i>amāvisse-t</i>: the perfect infinitive <i>amāvisse</i> with <i>-t</i>.',
    'amo-pass.3sg':'<i>amātus esset</i>: "he had been loved." A feminine subject takes <i>amāta esset</i>.'
  },
  idle: "You'll see a basic translation, and how the form is built from the perfect infinitive and a personal ending. The real translation depends on the use."
});''',
}

COLORS = {'subjunctive-present': {'e':('#23487B','#DAE4F1'), 'a':('#7F2756','#F4DDE9'), 'fut':('#7C3112','#FADFCF'), 'i':('#2F5331','#DDEBDC')},
          'subjunctive-imperfect': {'inf':('#23487B','#DAE4F1'), 'esse':('#2F5331','#DDEBDC'), 'cap':('#7F2756','#F4DDE9')},
          'subjunctive-perfect': {'eri':('#23487B','#DAE4F1'), 'fp':('#7C3112','#FADFCF'), 'sim':('#2F5331','#DDEBDC')},
          'subjunctive-pluperfect': {'isse':('#23487B','#DAE4F1'), 'essem':('#2F5331','#DDEBDC')}}
WIDE = ('/* two-word passive forms need wider charts */\n'
        '.vgroups .charts.three-up,.has-sb .vgroups .charts.three-up{grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}\n'
        '.vgroups .cell .fm{white-space:nowrap}\n'
        '@media (max-width:640px){.vgroups .charts.three-up,.has-sb .vgroups .charts.three-up{grid-template-columns:1fr}.vgroups .three-up .cell{font-size:1.0625rem;padding:10px 4px}}')

def tense_page(page, T):
    style = ':root{' + ' '.join(f'--p-{k}:{c}; --p-{k}-bg:{bg};' for k, (c, bg) in COLORS[page].items()) + '}' + ('\n' + WIDE if T['cur'] in ('perf', 'plup') else '')
    s = head(T['title'], style) + TOOLBAR
    s += (f'  <div class="intro" id="intro"><div class="intro-h"><span class="q">{T["q"]}</span><span class="sec">A&amp;G §§{T["secs"]}</span></div>'
          f'<p>{T["summary"]}</p>{seq_grid(T["cur"])}<p class="ta-note">For what the subjunctive is and how sequence of tenses works, see '
          '<a href="subjunctive.html">The Subjunctive: Overview</a>. Every use is listed on <a href="subjunctive-uses.html">Uses of the Subjunctive</a>.</p></div>\n\n')
    s += work(T['more'], *T['er'])
    prose, fig = T['build']
    s += block('How to build it', f'<div class="prose">{prose}</div><figure class="bd">{fig}</figure>')
    b = T['basic']
    s += (f'  <div class="block basic"><h3>The basic use: {b["name"]} <span class="sec">A&amp;G §{b["sec"]}</span></h3>'
          f'<p class="rule">{b["rule"]}</p><p class="how"><b>How to spot it:</b> {b["how"]}</p>{exs(b["ex"], True)}</div>\n')
    s += block('Other uses', '<div class="uses">' + ''.join(use_card(u) for u in T['uses']) + '</div>')
    if T['forms']:
        note, rows = T['forms']
        body = ''.join(f'<tr><td>{w}</td><td><i lang="la">{a}</i></td><td><i lang="la">{b_}</i></td></tr>' for w, a, b_ in rows)
        s += block("Other forms you'll see", (f'<p class="how">{note}</p>' if note else '') +
                   '<div class="conj-box"><table class="rule-table conj-table forms-table"><thead><tr><th>What happens</th><th>You may see</th><th>Same as</th></tr></thead>'
                   f'<tbody>{body}</tbody></table></div>')
    s += '</section>\n'
    secs = sorted({int(u['sec']) for u in T['uses']} | {int(b['sec'])})
    return s + foot(secs, CHART_HEAD + CHARTS[page], more=bool(T['more']))

for page, T in PAGES.items():
    open(os.path.join(SITE, 'grammar', page + '.html'), 'w').write(tense_page(page, T))
    print(page)

# ---------------------------------------------------------------- overview and uses pages
import subj_pages
subj_pages.SITE = SITE
for page, html in subj_pages.build(head, foot, block, exs, use_card, seq_grid).items():
    open(os.path.join(SITE, 'grammar', page + '.html'), 'w').write(html)
    print(page)
