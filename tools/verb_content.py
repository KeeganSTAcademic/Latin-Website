# Verb grammar pages in the pronoun-page layout: intro + time/aspect grid, the forms, how to build it,
# the basic use, the site's own analogy panel, other uses, other forms.
# Keeps the site's time-vs-aspect framing: incomplete / complete stem + time marker + personal ending.
# Writing rule: plain, complete sentences that say what the grammar does; no slogans; "function", not "job".
# ex rows: (latin with **highlight**, english, source or "")

# the time / aspect grid: (tense id, page, name, latin, english) by row (incomplete, complete) and column (past, present, future)
TA = {
 "active": [[("imperfect", "imperfect-active", "Imperfect", "amāb[a]t", "was loving"),
             ("present", "present-active", "Present", "amat", "is loving"),
             ("future", "future-active", "Future", "amāb[i]t", "will be loving")],
            [("pluperfect", "pluperfect-active", "Pluperfect", "amāver[a]t", "had loved"),
             ("perfect", "perfect-active", "Perfect", "amāvit", "has loved"),
             ("futperf", "future-perfect-active", "Future perfect", "amāver[i]t", "will have loved")]],
 "passive": [[("imperfect", "incomplete-passive", "Imperfect", "amāb[ā]tur", "was being loved"),
              ("present", "incomplete-passive", "Present", "amātur", "is being loved"),
              ("future", "incomplete-passive", "Future", "amāb[i]tur", "will be being loved")],
             [("pluperfect", "complete-passive", "Pluperfect", "amātus er[a]t", "had been loved"),
              ("perfect", "complete-passive", "Perfect", "amātus est", "has been loved"),
              ("futperf", "complete-passive", "Future perfect", "amātus er[i]t", "will have been loved")]],
}

# where this page's tense sits in the grid, in full sentences (the one place each page explains its time and aspect)
WHERE = {'present': 'The present is in the <b>present time</b> column and the <b>incomplete</b> row: the action is happening now and is not finished. Directly below it, the perfect is also in present time, '
            'but its action is finished: "she has loved."',
 'imperfect': 'The imperfect is in the <b>past time</b> column and the <b>incomplete</b> row: the action happened before now and, at that point, was not finished. Directly below it, the pluperfect '
              'is also in past time, but its action was already finished: "she had loved."',
 'future': 'The future is in the <b>future time</b> column and the <b>incomplete</b> row: the action has not happened yet and is pictured as going on. Directly below it, the future perfect is also '
           'in future time, but its action will be finished: "he will have loved."',
 'perfect': 'The perfect is in the <b>present time</b> column and the <b>complete</b> row: as of now, the action is finished. Directly above it, the present is also in present time, but its action '
            'is not finished: "he is loving." The perfect\'s second translation, the simple past "he loved," is shown under Simple translations.',
 'pluperfect': 'The pluperfect is in the <b>past time</b> column and the <b>complete</b> row: by a moment in the past, the action was already finished. Directly above it, the imperfect is also in '
               'past time, but its action was still going on: "he was loving."',
 'futperf': 'The future perfect is in the <b>future time</b> column and the <b>complete</b> row: by a moment in the future, the action will be finished. Directly above it, the future is also in '
            'future time, but its action is pictured as going on: "he will be loving."',
 'passive': 'This page covers the whole <b>incomplete</b> row in the passive. Each passive tense has the same time and aspect as its active partner; only the personal ending changes. The complete '
            'passives in the bottom row are formed differently, with <i>amātus</i> and a form of <i>sum</i>, and will have their own page.'}

# the simple row: a secondary meaning of another tense. (source tense, name, latin, english, where the source sits: "up" or "diag")
SIMPLE = {'active': [('perfect', 'Perfect', 'amāvit', 'loved', 'diag'), ('present', 'Present', 'amat', 'loves', 'up'), ('future', 'Future', 'amāb[i]t', 'will love', 'up')],
 'passive': [('perfect', 'Perfect', 'amātus est', 'was loved', 'diag'), ('present', 'Present', 'amātur', 'is loved', 'up'), ('future', 'Future', 'amāb[i]tur', 'will be loved', 'up')]}

# summary: what the tense is for and its main translations (formation lives in How to build it; time and aspect under the grid)
# basic: how to choose the English translation; how_label defaults to "How to spot it"
PAGES = {'present-active': {'cur': 'present',
                    'q': 'is loving, loves',
                    'secs': '163, 465–469',
                    'summary': 'The present tense describes what is happening now, or what is generally true. Latin has one form where English has three: <i>amat</i> can be translated "she loves," '
                               '"she is loving" or "she does love."',
                    'basic': {'name': 'choosing the English translation',
                              'sec': '465',
                              'rule': 'Choose the English form that fits the sentence. Use "she loves" for a habit or something generally true, "she is loving" for something going on at this moment, '
                                      'and "she does love" for emphasis.',
                              'how': 'In questions and negative sentences, English usually needs "do": <i>nōn amat</i>, "she does not love"; <i>amatne?</i>, "does she love?"',
                              'ex': [('Puella **cantat**.', 'The girl sings. / The girl is singing.', ''),
                                     ('Nautae nōn **nāvigant**.', 'The sailors do not sail. / The sailors are not sailing.', ''),
                                     ('Tē **amō**.', 'I love you.', '')],
                              'how_label': 'Questions and negatives'},
                    'uses': [{'name': 'An action continuing from the past',
                              'sec': '466',
                              'what': 'With <i>iam diū</i> ("for a long time now") or <i>iam prīdem</i>, the present describes an action that began in the past and is still going on. English uses '
                                      '"has been ___ing" for this.',
                              'clue': 'Look for <i>iam diū</i>, <i>iam prīdem</i> or a length of time next to a present verb.',
                              'ex': [('Iam diū tē **exspectō**.', 'I have been waiting for you for a long time.', '')]},
                             {'name': 'An attempted action',
                              'sec': '467',
                              'what': 'Because the present shows an action that is not finished, it can describe an attempt. In that case, translate it as "is trying to ___."',
                              'clue': 'The context shows that the action has not succeeded, or cannot have succeeded yet.',
                              'ex': [('Hostēs urbem **capiunt**.', 'The enemy are trying to take the city.', '')]},
                             {'name': 'The historical present',
                              'sec': '469',
                              'what': 'When telling a story about the past, Latin writers often switch to the present tense to make the events feel vivid. Translate these verbs with the English past '
                                      'tense.',
                              'clue': 'Present-tense verbs appear in the middle of a story that is otherwise told in the past.',
                              'ex': [('Caesar flūmen **trānsit**.', 'Caesar crossed the river. (literally: crosses)', '')]}]},
 'imperfect-active': {'cur': 'imperfect',
                      'q': 'was loving, used to love',
                      'secs': '470–471',
                      'summary': 'The imperfect describes something that was going on, or used to happen, in the past: <i>amābat</i>, "she was loving" or "she used to love." In a story it usually '
                                 'describes the background, while the <a href="perfect-active.html">perfect</a> reports the main events.',
                      'basic': {'name': 'choosing the English translation',
                                'sec': '470',
                                'rule': 'Use "was ___ing" for an action in progress at a moment in the past, "used to ___" for a habit, and "kept ___ing" for an action repeated again and again. If '
                                        'none of these sounds natural, the simple past ("she loved") is often fine, as long as the action is not a single, finished event.',
                                'how': 'Look for <i>-ba-</i> between the stem and the personal ending.',
                                'ex': [('Puella **cantābat**.', 'The girl was singing.', ''),
                                       ('Cotīdiē **ambulābāmus**.', 'We used to walk every day.', ''),
                                       ('Nox **erat**; mīlitēs **dormiēbant**.', 'It was night; the soldiers were sleeping.', '')]},
                      'uses': [{'name': 'An action continuing up to a past moment',
                                'sec': '471',
                                'what': 'With <i>iam diū</i> or <i>iam prīdem</i>, the imperfect describes an action that had already been going on for some time at a moment in the past. English '
                                        'uses "had been ___ing" for this.',
                                'clue': 'Look for <i>iam diū</i>, <i>iam prīdem</i> or a length of time next to an imperfect verb.',
                                'ex': [('Iam diū tē **exspectābam**.', 'I had been waiting for you for a long time.', '')]},
                               {'name': 'An attempted or beginning action',
                                'sec': '471',
                                'what': 'Because the imperfect shows an action that was not finished, it can describe an attempt ("tried to ___") or an action that was just beginning ("began to '
                                        '___").',
                                'clue': 'The context shows that the action did not succeed or had only just started.',
                                'ex': [('Hostēs urbem **capiēbant**.', 'The enemy were trying to take the city.', '')]}]},
 'future-active': {'cur': 'future',
                   'q': 'will love, will be loving',
                   'secs': '472',
                   'summary': 'The future describes something that will happen later: <i>amābit</i>, "he will love" or "he will be loving." The 1st and 2nd conjugations mark the '
                              'future with <i>-bi-</i>; the 3rd and 4th conjugations mark it with a vowel instead (<i>regam, regēs</i>; <i>audiam, audiēs</i>).',
                   'basic': {'name': 'choosing the English translation',
                             'sec': '472',
                             'rule': '"Will ___" is usually the natural translation. Use "will be ___ing" when the sentence stresses that the action will be in progress at some time in the future.',
                             'how': 'In the 1st and 2nd conjugations, look for <i>-bi-</i> between the stem and the personal ending, with <i>-bō</i> for "I" and <i>-bunt</i> for "they." '
                                    'In the 3rd and 4th conjugations, look for <i>-am</i> for "I" and an <i>ē</i> (or <i>e</i>) before the other endings.',
                             'ex': [('Crās **labōrābimus**.', 'We will work tomorrow.', ''), ('Tē semper **amābō**.', 'I will always love you.', '')]},
                   'uses': [{'name': 'A polite command',
                             'sec': '449',
                             'what': 'As in English, a sentence such as "you will take care of this" can give an order or an instruction.',
                             'clue': 'A 2nd-person future verb is used to tell someone what to do.',
                             'ex': [('Tū hoc **cūrābis**.', 'You will take care of this.', '')]},
                            {'name': 'In "if" and "when" clauses',
                             'sec': '472',
                             'what': 'Latin is more exact than English here. When the action of an "if" or "when" clause is still in the future, Latin puts that verb in the future tense, while '
                                     'English uses the present.',
                             'clue': 'Look for a future verb after <i>sī</i>, <i>cum</i> or <i>ubi</i>.',
                             'ex': [('Sī mē **vocābis**, aderō.', 'If you call me, I will be there.', '')]}]},
 'perfect-active': {'cur': 'perfect',
                    'q': 'has loved, loved',
                    'secs': '473–476',
                    'summary': 'The perfect describes either a completed action in the present ("he has loved") or a simple action in the past ("he loved"). The complete present is for an action that is finished by the time of speaking, like "I have arrived!" from someone who just showed up, or one finished earlier that still affects the present: you could say "I have studied two years of Latin" now or ten years from now. The simple past says only that an action happened; it is neither complete nor incomplete (see below for more).',
                    'basic': {'name': 'choosing the English translation',
                              'sec': '473',
                              'rule': 'In a story or a report of events, use the simple past: "Caesar came, saw and conquered." When someone is talking about the situation now, and the result of the '
                                      'action still matters, use "has ___ed": "I have written the letter" (so here it is).',
                              'how': 'A complete stem such as <i>amāv-</i>, <i>monu-</i> or <i>rēx-</i> shows a complete tense. Several perfect endings look like present endings, so check the stem '
                                     'before the ending: <i>amāvit</i>, not <i>amat</i>.',
                              'ex': [('Epistulam **scrīpsī**.', 'I have written the letter. (It is finished.)', ''),
                                     ('Caesar **vēnit**, **vīdit**, **vīcit**.', 'Caesar came, saw and conquered.', '')]},
                    'think': ('Has loved or loved?',
                              '<p>The perfect can be hard to understand at first, because English grammar rarely talks about <b>aspect</b>: whether an action is finished, separate from when it '
                              'happens. Even so, we use the difference every day.</p><p>Imagine that you are late to work, and your boss calls just after you walk into the building. You would say "I '
                              '<i>have</i> arrived," because you want to stress both that the arriving is done (complete) and that it affects the present (you are currently there). "I arrive" or "I '
                              'am arriving" would imply that you haven\'t gotten there yet, while "I arrived" or "I had arrived" would suggest that you might no longer be there.</p><p>Latin uses the '
                              'perfect for both "I have arrived" and "I arrived." The context tells you which one fits.</p>'),
                    'uses': [{'name': 'A perfect with a present meaning',
                              'sec': '476',
                              'what': 'A few verbs use the perfect to describe a present state. <i>Nōvī</i> literally means "I have learned," so it is translated "I know." <i>Meminī</i> means "I '
                                      'remember," and <i>ōdī</i> means "I hate."',
                              'clue': 'Translate <i>nōvī</i>, <i>meminī</i>, <i>ōdī</i> and <i>cōnsuēvī</i> with the English present tense.',
                              'ex': [('Tē **nōvī**.', 'I know you.', '')]}],
                    'forms': ('Roman writers often shortened the perfect. These shorter forms have exactly the same meaning as the full ones (A&amp;G §181).',
                              [('<i>-ēre</i> is used instead of <i>-ērunt</i> in the 3rd plural, especially in poetry and history.', 'amāvēre', 'amāvērunt'),
                               ('<i>-vi-</i> or <i>-ve-</i> is dropped after a long vowel.', 'amāstī · amārunt', 'amāvistī · amāvērunt'),
                               ('<i>-v-</i> is dropped in the 4th conjugation.', 'audiī · audiit', 'audīvī · audīvit')])},
 'pluperfect-active': {'cur': 'pluperfect',
                       'q': 'had loved',
                       'secs': '477',
                       'summary': 'The pluperfect describes an action that had already happened before another event in the past: "he had loved." It usually appears next to another past-tense verb '
                                  'and tells you which event came first.',
                       'basic': {'name': 'putting past events in order',
                                 'sec': '477',
                                 'rule': 'When a sentence mentions two past events, the pluperfect marks the earlier one. Translate it with "had ___ed," and translate the other verb with the simple '
                                         'past.',
                                 'how': 'Look for a complete stem followed by <i>-era-</i>.',
                                 'ex': [('Cum advēnī, **discesserat**.', 'When I arrived, he had left.', ''), ('Urbem iam **cēperant**.', 'They had already taken the city.', '')]},
                       'think': ('Has loved or had loved?',
                                 '<p>It is easy to confuse "he has loved" (complete in present time: the perfect) with "he had loved" (complete in past time: the pluperfect). Think again about '
                                 'calling your boss when you are late for work.</p><p>"I <i>have</i> arrived" means that you have just walked through the door: the arriving is over, and you are '
                                 'there now. "I <i>had</i> arrived" places the arrival further back and implies that something happened afterwards. Perhaps you had to go home for an emergency, or '
                                 'you left something in your car. Either way, your boss will assume you are not at work.</p>'),
                       'uses': [{'name': 'Verbs like nōveram: a simple past meaning',
                                 'sec': '476',
                                 'what': 'Verbs that have a present meaning in the perfect (<i>nōvī</i>, "I know") have a simple past meaning in the pluperfect (<i>nōveram</i>, "I knew").',
                                 'clue': 'Translate <i>nōveram</i>, <i>memineram</i> and <i>ōderam</i> with the English simple past.',
                                 'ex': [('Eum **nōveram**.', 'I knew him.', '')]}],
                       'forms': ('Like the perfect, the pluperfect is often shortened (A&amp;G §181).',
                                 [('<i>-ve-</i> is dropped after a long vowel.', 'amāram · dēlērat', 'amāveram · dēlēverat'),
                                  ('<i>-v-</i> is dropped in the 4th conjugation.', 'audierat', 'audīverat')])},
 'future-perfect-active': {'cur': 'futperf',
                           'q': 'will have loved',
                           'secs': '478',
                           'summary': 'The future perfect describes an action that will already be finished by some point in the future: "he will have loved." It is common in "if" and "when" '
                                      'clauses, where English usually uses the present tense instead.',
                           'basic': {'name': 'an action finished by a future point',
                                     'sec': '478',
                                     'rule': 'Translate the future perfect with "will have ___ed" when the sentence names or implies the future point by which the action will be finished, such as '
                                             '"by tomorrow."',
                                     'how': 'Look for a complete stem followed by <i>-eri-</i>, or <i>-erō</i> for "I." The 3rd plural ends in <i>-erint</i>, not <i>-erunt</i>, so do not confuse '
                                            '<i>amāverint</i> with the perfect <i>amāvērunt</i>.',
                                     'ex': [('Crās hoc **cōnfēcerō**.', 'I will have finished this by tomorrow.', '')]},
                           'think': ('Will love or will have loved?',
                                     '<p>The future perfect can be awkward to translate, but you can think of it as a more definite future. If I tell you that I will be grading this weekend (an '
                                     'incomplete future), that is a much vaguer promise than telling you that I will have graded everything by the weekend (a complete future).</p><p>This sense of '
                                     'certainty is also why the future perfect is common in prophecies: it describes what will be done and finished.</p>'),
                           'uses': [{'name': 'In "if" and "when" clauses',
                                     'sec': '478',
                                     'what': 'When the action of an "if" or "when" clause will be finished before the main action, Latin puts that verb in the future perfect. English uses the '
                                             'present ("if you do this") or the present perfect ("when you have done this").',
                                     'clue': 'Look for a future perfect after <i>sī</i>, <i>cum</i> or <i>ubi</i>, with a future verb in the main clause.',
                                     'ex': [('Sī hoc **fēceris**, laetus erō.', 'If you do this, I will be happy.', '')]}],
                           'forms': ('The future perfect can be shortened in the same way as the perfect (A&amp;G §181).',
                                     [('<i>-ve-</i> is dropped after a long vowel.', 'amārō · amāris', 'amāverō · amāveris')])},
 'incomplete-passive': {'cur': 'passive',
                        'q': 'is loved, was being loved, will be loved',
                        'secs': '163, 405, 409',
                        'summary': 'In the passive voice, the subject receives the action instead of doing it: "the girl is loved," not "the girl loves." This page covers the passive of the present, '
                                   'the imperfect and the future.',
                        'basic': {'name': 'translating the passive',
                                  'sec': '163',
                                  'rule': 'Translate the present passive as "is loved" or "is being loved," the imperfect passive as "was being loved" or "used to be loved," and the future passive '
                                          'as "will be loved."',
                                  'how': 'Look for an <i>r</i> in the personal ending (<i>-r, -ris, -tur, -mur, -ntur</i>), or for the ending <i>-minī</i>.',
                                  'ex': [('Puella **amātur**.', 'The girl is loved.', ''),
                                         ('Urbs **dēlēbātur**.', 'The city was being destroyed.', ''),
                                         ('Mīlitēs **vocābuntur**.', 'The soldiers will be called.', '')]},
                        'uses': [{'name': 'The person doing the action',
                                  'sec': '405',
                                  'what': 'To say who performs the action of a passive verb, Latin uses <i>ā</i> or <i>ab</i> with the ablative. English uses "by."',
                                  'clue': 'Look for <i>ā</i> or <i>ab</i> followed by a person in the ablative, near a passive verb.',
                                  'ex': [('Puella ā mātre **amātur**.', 'The girl is loved by her mother.', '')]},
                                 {'name': 'The thing used to do the action',
                                  'sec': '409',
                                  'what': 'To say what thing or means is used, Latin uses the ablative on its own, without a preposition. English uses "by" or "with."',
                                  'clue': 'Look for a thing in the ablative, with no preposition, near a passive verb.',
                                  'ex': [('Urbs flammīs **dēlēbātur**.', 'The city was being destroyed by flames.', '')]}],
                        'forms': ('', [('<i>-re</i> is used instead of <i>-ris</i> in the 2nd person singular, especially in poetry.', 'amābāre · amābere', 'amābāris · amāberis')])},
 'complete-passive': {'cur': 'cpassive',
                      'q': 'has been loved, had been loved, will have been loved',
                      'secs': '286, 405, 473–478',
                      'summary': 'The complete passives are the passive forms of the perfect, the pluperfect and the future perfect. Unlike the incomplete passives, they are not single words: '
                                 'each one is a participle with a form of <i>sum</i>, as in <i>amātus est</i>, "he has been loved." Like the perfect active, the perfect passive also has a simple-past '
                                 'translation: <i>amātus est</i> can mean "he was loved."',
                      'basic': {'name': 'translating the complete passive',
                                'sec': '473',
                                'rule': 'Translate the perfect passive as "has been loved" or "was loved," the pluperfect passive as "had been loved," and the future perfect passive as '
                                        '"will have been loved." Do not translate the form of <i>sum</i> on its own: <i>amātus est</i> does not mean "he is loved."',
                                'how': 'Look for a participle ending in <i>-tus</i> or <i>-sus</i> (or <i>-ta, -tum, -tī, -tae</i>) next to a form of <i>sum</i>. The two words can be separated, '
                                       'and the form of <i>sum</i> sometimes comes first.',
                                'ex': [('Puella **laudāta est**.', 'The girl has been praised, or the girl was praised.', ''),
                                       ('Urbs iam **dēlēta erat**.', 'The city had already been destroyed.', ''),
                                       ('Crās epistulae **missae erunt**.', 'Tomorrow the letters will have been sent.', '')]},
                      'uses': [{'name': 'The participle agrees with the subject',
                                'sec': '286',
                                'what': 'The participle is an adjective, so it agrees with the subject in gender, number and case. It is always nominative here, but its gender and number change with the subject.',
                                'clue': 'Match the participle\'s ending to the subject: <i>-us</i> or <i>-ī</i> for masculine, <i>-a</i> or <i>-ae</i> for feminine, <i>-um</i> or <i>-a</i> for neuter.',
                                'ex': [('Mīlitēs **vocātī sunt**.', 'The soldiers were called.', ''),
                                       ('Oppida **capta sunt**.', 'The towns were captured.', '')]},
                               {'name': 'The person doing the action',
                                'sec': '405',
                                'what': 'As with the incomplete passives, Latin uses <i>ā</i> or <i>ab</i> with the ablative to say who performed the action. English uses "by."',
                                'clue': 'Look for <i>ā</i> or <i>ab</i> followed by a person in the ablative, near the participle.',
                                'ex': [('Urbs ā Rōmānīs **capta est**.', 'The city was captured by the Romans.', '')]}],
                      'forms': ('', [('<i>fuī, fueram, fuerō</i> sometimes take the place of <i>sum, eram, erō</i>, with little or no difference in meaning.',
                                      'amātus fuit · amātus fuerat', 'amātus est · amātus erat')])}}
