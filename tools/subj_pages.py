"""The Subjunctive: Overview, and Uses of the Subjunctive. Text pages in the Introduction to Verbs style."""
import os, re
SITE = '.'   # set by make_subj.py

def verbs_style():
    s = open(os.path.join(SITE, 'grammar', 'verbs.html')).read()
    return re.search(r'<style>\n(.*?)\n</style>', s, flags=re.S).group(1)

EXTRA = '''.seq-ex{display:grid;gap:8px;margin:0}
.seq-ex .row{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(0,1fr) minmax(0,1.1fr);gap:4px 16px;align-items:baseline;background:var(--surface);border:1px solid var(--rule);border-radius:var(--radius,14px);padding:10px 16px}
.seq-ex .la{font-size:1.1875rem;font-style:italic}
.seq-ex .la .hl{color:var(--accent);font-weight:700}
.seq-ex .en{font-size:1.0625rem}
.seq-ex .why{color:var(--muted);font-size:1rem}
.uses-h{margin:6px 0 0;font-size:1.1875rem}
.intro a{color:var(--accent)}
.wo-row .la .hl{color:var(--accent);font-weight:700}
@media (max-width:640px){.seq-ex .row{grid-template-columns:1fr}}'''

def build(head, foot, block, exs, use_card, seq_grid):
    style = verbs_style() + '\n' + EXTRA
    hl = lambda s: re.sub(r'\*\*(.+?)\*\*', r'<b class="hl">\1</b>', s)
    pages = {}

    # ------------------------------------------------ overview
    wo = [('Venit.', 'He comes.', 'Indicative: a fact.', False),
          ('**Veniat.**', 'Let him come.', 'Subjunctive as the main verb: a command.', True),
          ('Utinam **veniat**!', 'I hope he comes!', 'Subjunctive as the main verb: a wish.', True),
          ('Rogō cūr **veniat**.', 'I ask why he is coming.', 'Subjunctive in a dependent clause: English uses an ordinary verb.', True)]
    fig = ('<figure class="wo"><figcaption>Fact, or something else?</figcaption>' + ''.join(
        f'<div class="wo-row{" flip" if f else ""}"><span class="la" lang="la">{hl(la)}</span><span class="en">{en}</span><span class="note">{n}</span></div>'
        for la, en, n, f in wo) + '</figure>')
    s = head('The Subjunctive: Overview', style)
    s += '\n<section id="charts">\n'
    s += ('  <div class="intro" id="intro">\n    <div class="intro-h"><span class="q">the mood for actions that are wished, possible, intended or reported</span><span class="sec">A&amp;G §§154, 438</span></div>\n'
          '    <p>Every Latin verb has a mood. The <b>indicative</b> presents an action as a fact: <i lang="la">venit</i>, "he comes." The <b>subjunctive</b> presents it in some other way. '
          'Its meanings come from two old ideas: <b>will</b>, what someone wants to happen ("let him come," "may he come"), and <b>imagining</b>, what could happen '
          '("he would come"). Most of its uses grow out of one or the other.</p>\n'
          '    <p>English has almost lost its subjunctive. It survives in a few phrases ("if I were you," "God save the king"); otherwise English uses helping words such as '
          '<i>may</i>, <i>might</i>, <i>would</i> and <i>let</i>, or an ordinary verb. So the Latin subjunctive has no single translation. Students often find this the hardest part: '
          'you translate a subjunctive according to its use, and you need to find the use first.</p>\n'
          f'    {fig}\n  </div>\n\n')
    s += block('Where you find it <span class="sec">A&amp;G §438</span>',
        '<div class="props">'
        '<article class="prop"><h4>In main clauses</h4><p class="ask">The subjunctive is the main verb.</p>'
        '<p>It adds an attitude to the action: an encouragement, a command, a wish, a doubtful question or a possibility. These uses are less common, and English usually needs <i>let</i>, <i>may</i> or <i>should</i>.</p>'
        '<div class="eg"><span><i lang="la">Amēmus.</i> Let us love.</span><span><i lang="la">Quid faciam?</i> What am I to do?</span></div></article>'
        '<article class="prop"><h4>In dependent clauses</h4><p class="ask">Something in the sentence calls for it.</p>'
        '<p>Most subjunctives are here, after words such as <i>ut</i>, <i>nē</i>, <i>cum</i> and <i>quī</i>, or in a reported question. These clauses began as main-clause subjunctives '
        'attached to another sentence: <i lang="la">mīsit lēgātōs quī dīcerent</i> first meant "he sent envoys; they were to say," and came to mean "he sent envoys to say." '
        'As the clause became a fixed construction, the subjunctive\'s own meaning faded, so English usually translates it with an ordinary verb.</p>'
        '<div class="eg"><span><i lang="la">Vēnit ut vidēret.</i> He came to see.</span><span><i lang="la">Rogāvit quid facerem.</i> He asked what I was doing.</span></div></article>'
        '</div><p class="lede sm">Every use is listed, with how to spot it, on <a href="subjunctive-uses.html">Uses of the Subjunctive</a>.</p>')
    rows = [('Present', 'subjunctive-present', 'amet', 'amētur', 'a changed vowel: <i>e</i> in the 1st conjugation, <i>a</i> in the others (<i>moneat, regat, audiat</i>)'),
            ('Imperfect', 'subjunctive-imperfect', 'amāret', 'amārētur', 'the present infinitive with an ending'),
            ('Perfect', 'subjunctive-perfect', 'amāverit', 'amātus sit', 'the complete stem with <i>-eri-</i>, or a participle with <i>sim</i>'),
            ('Pluperfect', 'subjunctive-pluperfect', 'amāvisset', 'amātus esset', 'the perfect infinitive with an ending, or a participle with <i>essem</i>')]
    tbl = ('<div class="tbl"><table><thead><tr><th>Tense</th><th>Active</th><th>Passive</th><th>How to recognize it</th></tr></thead><tbody>' + ''.join(
        f'<tr><td class="nm"><a href="{p}.html">{n}</a></td><td><span class="la-i" lang="la">{a}</span></td><td><span class="la-i" lang="la">{ps}</span></td><td>{how}</td></tr>'
        for n, p, a, ps, how in rows) + '</tbody></table></div>')
    s += block('The four tenses',
        '<p class="lede">The subjunctive has four tenses: two incomplete and two complete, built from the same principal parts as the indicative. '
        'It has no future. For a later action Latin uses the incomplete tenses, or, where it must be clear, the future participle with <i lang="la">sim</i> or <i lang="la">essem</i>: '
        '<i lang="la">prōspiciō quī concursūs futūrī sint</i>, "I foresee what crowds there will be."</p>' + tbl)
    seq_rows = [('Rogō quid **faciās**.', 'I ask what you are doing.', 'primary · same time → present'),
                ('Rogō quid **fēcerīs**.', 'I ask what you did.', 'primary · earlier → perfect'),
                ('Rogāvī quid **facerēs**.', 'I asked what you were doing.', 'secondary · same time → imperfect'),
                ('Rogāvī quid **fēcissēs**.', 'I asked what you had done.', 'secondary · earlier → pluperfect')]
    seq_ex = ('<div class="seq-ex">' + ''.join(f'<div class="row"><span class="la" lang="la">{hl(la)}</span><span class="en">{en}</span><span class="why">{w}</span></div>'
                                              for la, en, w in seq_rows) + '</div>')
    s += block('Sequence of tenses <span class="sec">A&amp;G §§482–485</span>',
        '<p class="lede">In a dependent clause, the main verb decides which subjunctive tense to use. This pattern is called <b>sequence of tenses</b>. '
        'It is a strong tendency rather than a strict law, and writers sometimes break it for emphasis. To choose the tense, ask two questions.</p>'
        '<div class="prose"><p><b>1. When is the main verb?</b> A present or future main verb puts the sentence in <b>primary sequence</b>, which uses the present or perfect subjunctive. '
        'A past main verb puts it in <b>secondary sequence</b>, which uses the imperfect or pluperfect subjunctive: <i lang="la">scrībit ut nōs moneat</i>, "he writes to warn us," '
        'but <i lang="la">scrīpsit ut nōs monēret</i>, "he wrote to warn us." A perfect main verb usually counts as past ("he loved"); when the writer has the present in mind ("has loved"), '
        'it can take primary sequence.</p>'
        '<p><b>2. When is the dependent action, compared with the main verb?</b> If it happens at the same time or later, use an incomplete tense (present or imperfect). '
        'If it happened earlier, use a complete tense (perfect or pluperfect).</p></div>'
        + seq_grid(None, 'The four subjunctive tenses') + seq_ex +
        '<div class="watch"><b class="t">Translate by the sequence, not with "may" and "might"</b>'
        '<p>In <i lang="la">rogāvī quid facerēs</i>, the imperfect subjunctive is simply "you were doing." The helping words <i>may</i> and <i>might</i> belong to a few uses, '
        'such as possibility and some purpose clauses. In most dependent clauses, use the English tense that the sequence points to.</p></div>')
    s += block('The tense pages', '<div class="links">' + ''.join(f'<a href="{p}.html">{n}</a>' for n, p, *_ in rows)
               + '<a href="subjunctive-uses.html">Uses of the Subjunctive</a></div>')
    s += '</section>\n'
    pages['subjunctive'] = s + foot('154, 438, 482–485')

    # ------------------------------------------------ uses
    signals = [('<i>ut</i> or <i>nē</i> with a subjunctive', 'purpose, indirect command, result (<i>ut</i>, <i>ut nōn</i>), fear (<i>nē</i>, <i>ut</i>)'),
               ('<i>ut</i> with an indicative', 'not a subjunctive use: "as" or "when"'),
               ('<i>cum</i> with a subjunctive', '"when," "since" or "although"'),
               ('<i>quī, quae, quod</i> with a subjunctive', 'a relative clause of purpose or of characteristic'),
               ('a question word after a verb of asking, knowing or telling', 'an indirect question'),
               ('<i>sī</i> or <i>nisi</i> with a subjunctive', 'a condition that is imagined or contrary to fact'),
               ('<i>utinam</i>', 'a wish'),
               ('a subjunctive main verb with no signal word', 'an encouragement, a command, a doubtful question or a possibility')]
    sig = ('<div class="tbl"><table><thead><tr><th>Look for</th><th>It may be</th></tr></thead><tbody>'
           + ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in signals) + '</tbody></table></div>')
    main = [dict(name='Encouragements and commands', sec='439',
                 what='The oldest meaning of the subjunctive is the speaker\'s will. The 1st person plural encourages ("let us ..."); the 3rd person gives a command ("let him ..."). The negative is <i>nē</i>.',
                 clue='A present subjunctive as the main verb.',
                 ex=[('**Eāmus**!', "Let's go!", ''), ('Nē **timeant**.', 'Let them not be afraid.', '')]),
            dict(name='Granting a point', sec='440',
                 what='The same use can grant something for the sake of argument, before the speaker makes the real point. English uses "grant that" or "suppose." The negative is <i>nē</i>.',
                 clue='A present or perfect subjunctive as the main verb, followed by a "but" or "still."',
                 ex=[('**Sit** fūr, **sit** sacrilegus.', 'Grant that he is a thief and a temple robber.', '')]),
            dict(name='Prohibitions', sec='450',
                 what='Latin forbids an action in three ways: <i>nōlī</i> with an infinitive (the usual way), <i>cavē</i> with the present subjunctive, or <i>nē</i> with the perfect subjunctive, which is blunter. The perfect here does not refer to the past.',
                 clue='<i>Nē</i> with a 2nd person perfect subjunctive, or <i>cavē</i> with a present subjunctive.',
                 ex=[('Nē **timueris**.', "Don't be afraid.", ''), ('Cavē **festīnēs**.', "Don't hurry.", '')]),
            dict(name='Wishes', sec='441',
                 what='The tense shows whether the wish can still come true. The present wishes for something possible; the imperfect wishes the present were different; the pluperfect wishes the past had been different. <i>Utinam</i> regularly comes before the imperfect and pluperfect. The negative is <i>nē</i>.',
                 clue='<i>Utinam</i>, or a wish such as "may the gods ..."',
                 ex=[('Utinam **veniat**!', 'I hope he comes!', ''), ('Utinam **adesset**!', 'If only he were here!', ''), ('Utinam **adfuisset**!', 'If only he had been here!', '')]),
            dict(name='Doubtful questions', sec='444',
                 what='A question in the subjunctive asks what should be done. It began as a request to learn someone\'s will and came to express doubt, frustration or impossibility. English uses "am I to" or "should I." The negative is <i>nōn</i>.',
                 clue='A question whose main verb is subjunctive, usually 1st person.',
                 ex=[('Quid **agam**, iūdicēs?', 'What am I to do, judges?', ''), ('Quid **facerem**?', 'What was I to do?', '')]),
            dict(name='Possibility', sec='446',
                 what='The subjunctive presents an action as something that could happen, not as a fact or a wish. English uses "may," "might," "would" or "could," whichever fits. The present looks to the future; the imperfect looks to the past. The negative is <i>nōn</i>.',
                 clue='A subjunctive main verb, often with an indefinite subject such as <i>aliquis</i>, or with "you" meaning anyone.',
                 ex=[('**Dīcat** aliquis.', 'Someone may say.', ''), ('**Crēderēs** victōs.', 'You would have thought them defeated.', '')])]
    dep = [dict(name='Purpose', sec='531',
                what='<i>Ut</i> (negative <i>nē</i>) with the subjunctive says why someone does something. English often uses an infinitive ("to," "in order to"), but Latin prose never does: it uses a clause.',
                clue='<i>Ut</i> or <i>nē</i> after a verb of action, with no signpost word such as <i>tam</i> or <i>ita</i>.',
                ex=[('Ab arātrō abdūxērunt Cincinnātum, ut dictātor **esset**.', 'They brought Cincinnatus from the plow to be dictator.', ''), ('Fūgit nē **caperētur**.', 'He fled so that he would not be captured.', '')]),
           dict(name='Relative clause of purpose', sec='531',
                what='A relative pronoun or adverb can introduce a purpose clause, especially when the purpose belongs to one word in the sentence. English uses "to."',
                clue='<i>Quī, quae, quod</i> with a subjunctive, often after a verb of sending.',
                ex=[('Mittitur quī locī nātūram **perspiciat**.', 'He is sent to examine the lay of the land.', '')]),
           dict(name='Indirect command', sec='563',
                what='Verbs whose action points to the future (asking, ordering, urging, warning, persuading, permitting) take a clause with <i>ut</i> or <i>nē</i> and the subjunctive. '
                     'It works like a purpose clause that is the object of the verb. English uses "to" or "not to." <i>Iubeō</i> and <i>vetō</i> take an infinitive instead.',
                clue='<i>Ut</i> or <i>nē</i> after a verb such as <i>rogō, ōrō, imperō, moneō, hortor, persuādeō</i>.',
                ex=[('Monet ut omnēs suspīciōnēs **vītet**.', 'He warns him to avoid all suspicion.', ''), ('Mē ōrat nē **discēdam**.', 'She begs me not to leave.', '')]),
           dict(name='Result', sec='537',
                what='<i>Ut</i> (negative <i>ut nōn</i>) with the subjunctive gives the result of something described in the main clause. English uses "that," or sometimes an infinitive: "too far away to see."',
                clue='A signpost word in the main clause: <i>tam, ita, sīc, adeō</i> ("so"), <i>tantus</i> ("so great"), <i>tālis</i> ("such").',
                ex=[('Tanta vīs probitātis est ut eam in hoste **dīligāmus**.', 'Goodness has such power that we love it even in an enemy.', 'Cicero, Laelius 29'),
                    ('Tam longē aberam ut nōn **vidērem**.', 'I was too far away to see.', '')]),
           dict(name='Relative clause of characteristic', sec='535',
                what='A relative clause in the indicative states a fact about a particular person or thing. In the subjunctive it says what kind of person or thing is meant. English uses "the kind of ... who," "such as" or an ordinary verb.',
                clue='<i>Sunt quī</i>, <i>nēmō est quī</i>, <i>quis est quī</i>, <i>sōlus quī</i>, or <i>dignus quī</i>.',
                ex=[('Nēmō est quī hoc **nesciat**.', 'There is no one who does not know this.', ''), ('Sunt quī **dīcant**.', 'There are people who say so.', '')]),
           dict(name='Indirect question', sec='574',
                what='A question opened by a question word can be part of a larger sentence, as the object of a verb of asking, knowing, telling or doubting. Its verb is subjunctive, and English uses an ordinary verb.',
                clue='A question word (<i>quis, quid, cūr, ubi, quandō, num, -ne, utrum</i>) after a verb such as <i>rogō, sciō, nesciō, dīcō</i>.',
                ex=[('Quid ipse **sentiam** expōnam.', 'I will explain what I think.', ''), ('Rogāvit quis **vēnisset**.', 'He asked who had come.', '')]),
           dict(name='Fearing', sec='564',
                what='After verbs of fearing (<i>timeō, metuō, vereor</i>), <i>nē</i> means "that" and <i>ut</i> means "that ... not." This makes sense once you see where it comes from: '
                     '<i>timeō nē veniat</i> began as two sentences, "I am afraid. May he not come!"',
                clue='A verb of fearing followed by <i>nē</i> or <i>ut</i>.',
                ex=[('Timeō nē Verrēs **fēcerit**.', 'I am afraid that Verres has done it.', ''), ('Vereor ut tibi **possim** concēdere.', 'I am afraid that I cannot grant you this.', '')]),
           dict(name='Cum clauses', sec='546',
                what='<i>Cum</i> with the indicative dates an action. With the subjunctive it describes the circumstances ("when," "while"), or gives a reason ("since") or a concession ("although," A&amp;G §549). '
                     '<i>Tamen</i> in the main clause points to "although."',
                clue='<i>Cum</i> followed by a subjunctive.',
                ex=[('Cum id nūntiātum **esset**, mātūrat.', 'When this had been reported, he hurries.', 'Caesar, B.G. 1.7'),
                    ('Cum prīmī ōrdinēs **concidissent**, tamen ācerrimē reliquī resistēbant.', 'Although the front ranks had fallen, the rest still resisted fiercely.', 'Caesar, B.G. 7.62')]),
           dict(name='Conditions', sec='516–517',
                what='A condition in the subjunctive is imagined, not stated as a fact. The present subjunctive imagines a possible future ("should ... would"). The imperfect and pluperfect imagine something that is not true now or was not true then, so they imply the opposite.',
                clue='<i>Sī</i> or <i>nisi</i> with a subjunctive in both halves of the sentence.',
                ex=[('Sī **rogēs** Aristōnem, **neget**.', 'If you should ask Aristo, he would say no.', ''), ('Sī **adessēs**, **gaudērem**.', 'If you were here, I would be glad.', ''),
                    ('Sī **vēnissēs**, tē **vīdissem**.', 'If you had come, I would have seen you.', '')]),
           dict(name='Clauses inside indirect statement', sec='580',
                what='When a statement is reported with an infinitive, the verbs of its dependent clauses become subjunctive. English uses an ordinary verb.',
                clue='A dependent clause inside an accusative-and-infinitive statement.',
                ex=[('Dīxit puerum, quī **adesset**, fessum esse.', 'He said that the boy who was present was tired.', '')])]
    s = head('Uses of the Subjunctive', style)
    s += '\n<section id="charts">\n'
    s += ('  <div class="intro" id="intro">\n    <div class="intro-h"><span class="q">every common use, and how to spot it</span><span class="sec">A&amp;G §§439–580</span></div>\n'
          '    <p>The subjunctive appears in two places: as the main verb of a sentence, where it adds a wish, a command, a doubt or a possibility, and in dependent clauses, '
          'where a word such as <i lang="la">ut</i>, <i lang="la">nē</i>, <i lang="la">cum</i> or <i lang="la">quī</i>, or a reported question, calls for it.</p>\n'
          '    <p>To translate a subjunctive, first find what calls for it, then use the translation that goes with that use. The tense follows sequence of tenses, '
          'explained on <a href="subjunctive.html">The Subjunctive: Overview</a>.</p>\n  </div>\n\n')
    s += block('Start from the signal word', sig)
    s += block('In main clauses', '<div class="uses">' + ''.join(use_card(u) for u in main) + '</div>')
    s += block('In dependent clauses', '<div class="uses">' + ''.join(use_card(u) for u in dep) + '</div>'
               '<div class="watch"><b class="t">Purpose or result?</b><p>In positive sentences the two look the same. A result clause usually follows a signpost word in the main clause '
               '(<i lang="la">tam, ita, sīc, tantus</i>). The negative tells them apart: purpose uses <i lang="la">nē</i>, result uses <i lang="la">ut nōn</i>. '
               'Compare <i lang="la">custōdītus est nē effugeret</i>, "he was guarded so that he would not escape" (purpose), with <i lang="la">custōdītus est ut nōn effugeret</i>, '
               '"he was guarded, so that he did not escape" (result).</p></div>')
    s += '</section>\n'
    pages['subjunctive-uses'] = s + foot('439–580')
    return pages
