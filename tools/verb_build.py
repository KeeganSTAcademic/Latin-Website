import re
"""How a verb form breaks down: stem + time marker + personal ending, for the 'How to build it' block,
and the advanced note on how the 3rd principal part is formed (A&G §177)."""

PERS = ["1st sing.", "2nd sing.", "3rd sing.", "1st pl.", "2nd pl.", "3rd pl."]
EN_SUBJ = ["I", "you", "he, she, it", "we", "you (pl.)", "they"]

# (stem, time marker, ending) for amō, by tense
SEG = {
 "present":   [("am", "", "ō"), ("amā", "", "s"), ("ama", "", "t"), ("amā", "", "mus"), ("amā", "", "tis"), ("ama", "", "nt")],
 "imperfect": [("amā", "ba", "m"), ("amā", "bā", "s"), ("amā", "ba", "t"), ("amā", "bā", "mus"), ("amā", "bā", "tis"), ("amā", "ba", "nt")],
 "future":    [("amā", "b", "ō"), ("amā", "bi", "s"), ("amā", "bi", "t"), ("amā", "bi", "mus"), ("amā", "bi", "tis"), ("amā", "bu", "nt")],
 "perfect":   [("amāv", "", "ī"), ("amāv", "", "istī"), ("amāv", "", "it"), ("amāv", "", "imus"), ("amāv", "", "istis"), ("amāv", "", "ērunt")],
 "pluperfect":[("amāv", "era", "m"), ("amāv", "erā", "s"), ("amāv", "era", "t"), ("amāv", "erā", "mus"), ("amāv", "erā", "tis"), ("amāv", "era", "nt")],
 "futperf":   [("amāv", "er", "ō"), ("amāv", "eri", "s"), ("amāv", "eri", "t"), ("amāv", "eri", "mus"), ("amāv", "eri", "tis"), ("amāv", "eri", "nt")],
 "pres-p":    [("am", "", "or"), ("amā", "", "ris"), ("amā", "", "tur"), ("amā", "", "mur"), ("amā", "", "minī"), ("ama", "", "ntur")],
 "impf-p":    [("amā", "ba", "r"), ("amā", "bā", "ris"), ("amā", "bā", "tur"), ("amā", "bā", "mur"), ("amā", "bā", "minī"), ("amā", "ba", "ntur")],
 "fut-p":     [("amā", "b", "or"), ("amā", "be", "ris"), ("amā", "bi", "tur"), ("amā", "bi", "mur"), ("amā", "bi", "minī"), ("amā", "bu", "ntur")],
}
VERB_EN = {"present": "love", "imperfect": "was loving", "future": "will love", "perfect": "have loved", "pluperfect": "had loved",
           "futperf": "will have loved"}
LABEL = {"pres-p": "Present", "impf-p": "Imperfect", "fut-p": "Future"}
STEM_NOTE = {"present": "In <i>amō</i> and <i>amor</i>, the <i>ā</i> of the stem has merged into the ending.",
             "passive": "In <i>amor</i>, the <i>ā</i> of the stem has merged into the ending."}

def piece(s, m, e):
    out = f'<span class="bd-s">{s}</span>'
    out += f'<span class="bd-m">{m}</span>' if m else ''
    return out + f'<span class="bd-e">{e}</span>'

def en(tense, i):
    subj = EN_SUBJ[i]
    if tense == "present": return f"{subj} {'loves' if i == 2 else 'love'}"
    if tense == "imperfect": return f"{subj} {'was' if i in (0, 2) else 'were'} loving"
    if tense == "perfect": return f"{subj} {'has' if i == 2 else 'have'} loved"
    return f"{subj} {VERB_EN[tense]}"

def formula(stem_lab, s, m, e, form, gloss, marker_lab="time marker"):
    mk = (f'<span class="bd-box m"><span class="bd-f">{m}</span><span class="bd-l">{marker_lab}</span></span><span class="bd-plus">+</span>'
          if m else '<span class="bd-box m none"><span class="bd-f">—</span><span class="bd-l">no time marker</span></span><span class="bd-plus">+</span>')
    return ('<div class="bd-formula">'
            f'<span class="bd-box s"><span class="bd-f">{s}</span><span class="bd-l">{stem_lab}</span></span><span class="bd-plus">+</span>'
            + mk +
            f'<span class="bd-box e"><span class="bd-f">{e}</span><span class="bd-l">personal ending</span></span>'
            f'<span class="bd-plus">=</span><span class="bd-out"><span class="bd-f" lang="la">{piece(s, m, e)}</span><span class="bd-l">{gloss}</span></span></div>')

KEY = ('<p class="bd-key"><span class="bd-s">stem</span>: aspect · <span class="bd-m">time marker</span>: time · '
       '<span class="bd-e">personal ending</span>: person and number{voice}. This three-part reading works for the indicative tenses; '
       'not every Latin verb form divides so neatly.</p>')

SUM = {"perfect": ["sum", "es", "est", "sumus", "estis", "sunt"],
       "pluperfect": ["eram", "erās", "erat", "erāmus", "erātis", "erant"],
       "futperf": ["erō", "eris", "erit", "erimus", "eritis", "erunt"]}
CP_LABEL = {"perfect": "Perfect", "pluperfect": "Pluperfect", "futperf": "Future perfect"}

def cp_piece(i, t):
    return f'<span class="bd-s">amāt{"us" if i < 3 else "ī"}</span> <span class="bd-e">{SUM[t][i]}</span>'

def cp_breakdown():
    head = ('<div class="bd-formula">'
            '<span class="bd-box s"><span class="bd-f">amātus</span><span class="bd-l">participle</span></span><span class="bd-plus">+</span>'
            '<span class="bd-box e"><span class="bd-f">est</span><span class="bd-l">form of <i>sum</i></span></span><span class="bd-plus">=</span>'
            f'<span class="bd-out"><span class="bd-f" lang="la">{cp_piece(2, "perfect")}</span><span class="bd-l">he has been loved</span></span></div>')
    key = ('<p class="bd-key"><span class="bd-s">participle</span>: aspect, and the gender and number of the subject · '
           '<span class="bd-e">form of <i>sum</i></span>: time, person and number.</p>')
    cols = ["perfect", "pluperfect", "futperf"]
    rows = ''.join(f'<tr><td class="bd-p">{PERS[i]}</td>' + ''.join(f'<td lang="la">{cp_piece(i, t)}</td>' for t in cols) + '</tr>' for i in range(6))
    tbl = ('<div class="bd-table"><table><thead><tr><th>Person</th>' + ''.join(f'<th>{CP_LABEL[t]}</th>' for t in cols)
           + '</tr></thead><tbody>' + rows + '</tbody></table></div>')
    note = ('<p class="bd-note">The table shows a masculine subject. For a feminine subject the participle is <i>amāta</i>, <i>amātae</i>; '
            'for a neuter one, <i>amātum</i>, <i>amāta</i>.</p>')
    return '<figure class="bd">' + head + key + tbl + note + '</figure>'

def breakdown(cur):
    """Figure + table for one page. cur is the tense id from verb_content (present, imperfect, ..., passive)."""
    if cur == "cpassive":
        return cp_breakdown()
    if cur == "passive":
        cols = ["pres-p", "impf-p", "fut-p"]
        head = formula("incomplete stem", "amā", "bā", "tur", "amābātur", "he was being loved")
        rows = ''.join(f'<tr><td class="bd-p">{PERS[i]}</td>' + ''.join(f'<td lang="la">{piece(*SEG[c][i])}</td>' for c in cols)
                       + f'<td class="bd-end"><span class="bd-e">-{SEG["pres-p"][i][2] if i else "or / -r"}</span></td></tr>' for i in range(6))
        tbl = ('<div class="bd-table"><table><thead><tr><th>Person</th>' + ''.join(f'<th>{LABEL[c]}</th>' for c in cols)
               + '<th class="bd-end">Passive ending</th></tr></thead><tbody>' + rows + '</tbody></table></div>')
        return '<figure class="bd">' + head + KEY.replace("{voice}", ", and here voice") + tbl + f'<p class="bd-note">{STEM_NOTE["passive"]}</p></figure>'
    complete = cur in ("perfect", "pluperfect", "futperf")
    stem_lab = "complete stem" if complete else "incomplete stem"
    s, m, e = SEG[cur][2]
    head = formula(stem_lab, s, m, e, s + m + e, en(cur, 2).replace("he, she, it", "he"))
    rows = ''.join(f'<tr><td class="bd-p">{PERS[i]}</td><td lang="la" class="bd-form">{piece(*SEG[cur][i])}</td>'
                   f'<td class="bd-end"><span class="bd-e">-{SEG[cur][i][2]}</span></td><td class="bd-en">{en(cur, i)}</td></tr>' for i in range(6))
    end_head = "Perfect ending" if cur == "perfect" else "Personal ending"
    tbl = ('<div class="bd-table"><table><thead><tr><th>Person</th><th>Form</th>'
           f'<th class="bd-end">{end_head}</th><th>English</th></tr></thead><tbody>' + rows + '</tbody></table></div>')
    note = f'<p class="bd-note">{STEM_NOTE["present"]}</p>' if cur == "present" else ''
    return '<figure class="bd">' + head + KEY.replace("{voice}", "") + tbl + note + '</figure>'

def _pp(pairs):
    # "secō>sec[u]ī" -> secō → sec<b>u</b>ī ; the bracketed part is what changed
    out = []
    for p in pairs.split(', '):
        a, b = p.split('>')
        b = re.sub(r'\[(.+?)\]', r'<b>\1</b>', b)
        out.append(f'<i lang="la">{a}</i> → <i lang="la">{b}</i>')
    return ', '.join(out)

def _group(title, usual, rows, note='', other='Other patterns:'):
    li = ''.join(f'<li><span class="ps-l">{lab}</span> {_pp(pp)}</li>' for lab, pp in rows)
    return (f'<div class="ps-card"><h4>{title}</h4><p class="ps-usual">{usual}</p>'
            + (f'<p class="ps-other">{other}</p><ul>{li}</ul>' if rows else '') + (f'<p class="ps-note">{note}</p>' if note else '') + '</div>')

PERFECT_STEM = (
  '<p>The 3rd principal part has to be learned with each verb, but most are made in one of five ways (A&amp;G §177). '
  'Each conjugation tends to prefer one of them, so knowing the patterns helps you learn new verbs faster and recognize a perfect you have not learned yet.</p>'
  '<ol class="ps-ways">'
  '<li><b>Add <i>-v-</i> or <i>-u-</i></b> after the stem: <i lang="la">amā<b>v</b>ī, mon<b>u</b>ī</i>.</li>'
  '<li><b>Add <i>-s-</i></b> to the root. A <i>c</i>, <i>g</i> or <i>h</i> before it combines with the <i>s</i> and is written <i>x</i>: <i lang="la">rē<b>x</b>ī</i> from <i lang="la">regō</i>.</li>'
  '<li><b>Repeat the first consonant</b> with a vowel in front of the root (reduplication): <i lang="la"><b>ce</b>cidī</i> from <i lang="la">cadō</i>.</li>'
  '<li><b>Lengthen the root vowel</b>, which sometimes also changes it: <i lang="la">l<b>ē</b>gī</i> from <i lang="la">legō</i>, <i lang="la"><b>ē</b>gī</i> from <i lang="la">agō</i>.</li>'
  '<li><b>Change nothing</b>: the root stays as it is and only the ending shows the tense: <i lang="la">vertī</i> from <i lang="la">vertō</i>.</li>'
  '</ol>'
  '<div class="ps-grid">'
  + _group('1st conjugation', 'Almost always <b>-āvī</b>: <i lang="la">amō → amāvī, vocō → vocāvī, laudō → laudāvī</i>. A new 1st-conjugation verb is a safe bet to follow it.',
      [('-uī', 'secō>sec[u]ī, domō>dom[u]ī, vetō>vet[u]ī, sonō>son[u]ī, cubō>cub[u]ī'),
       ('Reduplication', 'dō>[de]dī, stō>[ste]tī'),
       ('Lengthened vowel', 'iuvō>i[ū]vī, lavō>l[ā]vī')])
  + _group('2nd conjugation', 'Usually <b>-uī</b>: <i lang="la">moneō → monuī, habeō → habuī, terreō → terruī, doceō → docuī</i>. The <i>ē</i> of the stem drops out.',
      [('-ēvī', 'dēleō>dēl[ēv]ī, fleō>fl[ēv]ī, impleō>impl[ēv]ī'),
       ('-sī or -xī', 'maneō>mān[s]ī, rīdeō>rī[s]ī, iubeō>iu[ss]ī, augeō>au[x]ī, suādeō>suā[s]ī'),
       ('Lengthened vowel', 'videō>v[ī]dī, sedeō>s[ē]dī, moveō>m[ō]vī, caveō>c[ā]vī'),
       ('Reduplication', 'mordeō>[mo]mordī, pendeō>[pe]pendī, spondeō>[spo]pondī')])
  + _group('3rd conjugation', 'There is <b>no usual pattern</b>; the 3rd conjugation uses all five. Learn each perfect with the verb. The groups below help you recognize one you have forgotten.',
      [('-sī or -xī', 'regō>rē[x]ī, dīcō>dī[x]ī, dūcō>dū[x]ī, scrībō>scrīp[s]ī, mittō>mī[s]ī, gerō>ge[ss]ī, vīvō>vī[x]ī'),
       ('Reduplication', 'currō>[cu]currī, cadō>[ce]cidī, tangō>[te]tigī, pellō>[pe]pulī, discō>[di]dicī'),
       ('Lengthened vowel', 'legō>l[ē]gī, emō>[ē]mī, agō>[ē]gī, vincō>v[ī]cī, relinquō>rel[ī]quī, frangō>fr[ē]gī'),
       ('Unchanged', 'vertō>vertī, dēfendō>dēfendī, ostendō>ostendī, solvō>solvī, bibō>bibī, metuō>metuī'),
       ('-vī or -uī', 'petō>pet[īv]ī, quaerō>quaes[īv]ī, nōscō>nō[v]ī, pōnō>pos[u]ī, colō>col[u]ī')],
      'In the reduplicated perfects the root vowel often weakens: <i lang="la">cadō</i> has <i lang="la">cecidī</i>, not <i>*cecadī</i>.', 'The five patterns:')
  + _group('3rd conjugation -iō', 'These behave like the 3rd conjugation. The common ones mostly <b>lengthen the vowel</b>, and often change it to <i>ē</i>: <i lang="la">capiō → cēpī, faciō → fēcī, iaciō → iēcī, fugiō → fūgī</i>.',
      [('-īvī or -uī', 'cupiō>cup[īv]ī, rapiō>rap[u]ī'),
       ('-sī or -xī', 'aspiciō>aspe[x]ī'),
       ('Reduplication', 'pariō>[pe]perī')])
  + _group('4th conjugation', 'Usually <b>-īvī</b>: <i lang="la">audiō → audīvī, mūniō → mūnīvī, dormiō → dormīvī, sciō → scīvī</i>.',
      [('Lengthened vowel', 'veniō>v[ē]nī'),
       ('-uī', 'aperiō>aper[u]ī, saliō>sal[u]ī'),
       ('-sī or -xī', 'sentiō>sēn[s]ī, hauriō>hau[s]ī, vinciō>vīn[x]ī'),
       ('Reduplication', 'reperiō>[rep]perī')])
  + '</div>'
  '<p class="how"><b>Shortened forms:</b> <i>-v-</i> perfects are often shortened, especially in poetry. <i lang="la">Amāvistī</i> can appear as <i lang="la">amāstī</i>, <i lang="la">audīvit</i> as <i lang="la">audiit</i>, and <i lang="la">amāvērunt</i> as <i lang="la">amārunt</i>.</p>'
  '<p class="how"><b>Watch the lengthened-vowel perfects:</b> <i lang="la">venit</i> (he comes) and <i lang="la">vēnit</i> (he came) differ only in the length of the <i>e</i>, which most texts do not mark. Context, and other verbs in the sentence, usually tell you which one it is.</p>')

CSS = '''
/* how a form breaks down: stem + time marker + personal ending */
.bd{margin:0;display:grid;gap:12px}
.bd-s{color:#23487B;font-weight:700}.bd-m{color:#6E3F00;font-weight:700}.bd-e{color:var(--accent);font-weight:700}
.bd-formula{display:flex;flex-wrap:wrap;align-items:stretch;gap:8px}
.bd-box,.bd-out{display:grid;gap:2px;align-content:start;border-radius:12px;padding:10px 14px;border:1px solid var(--rule);background:var(--surface)}
.bd-box.s{border-top:4px solid #23487B}.bd-box.m{border-top:4px solid #6E3F00}.bd-box.e{border-top:4px solid var(--accent)}
.bd-box.none .bd-f{color:var(--muted)}
.bd-box .bd-f,.bd-out .bd-f{font-size:1.375rem;font-style:italic}
.bd-box.s .bd-f{color:#23487B}.bd-box.m .bd-f{color:#6E3F00}.bd-box.e .bd-f{color:var(--accent)}
.bd-l{font-size:1rem;color:var(--muted)}
.bd-plus{align-self:center;font-size:1.25rem;color:var(--muted)}
.bd-key,.bd-note{margin:0;font-size:1rem;color:var(--muted);max-width:80ch}
.bd-table{overflow-x:auto;background:var(--surface);border:1px solid var(--rule);border-radius:var(--radius,14px)}
.bd-table table{border-collapse:collapse;width:100%;font-size:1.0625rem}
.bd-table th{font-weight:400;font-size:1rem;color:var(--muted);font-variant:small-caps;text-transform:lowercase;letter-spacing:.1em;text-align:left;padding:8px 14px;border-bottom:1px solid var(--rule)}
.bd-table td{padding:8px 14px;border-top:1px solid var(--rule)}
.bd-table td[lang]{font-size:1.1875rem;font-style:italic}
.bd-table td[lang] span{font-weight:400}
.bd-table td[lang] .bd-m,.bd-table td[lang] .bd-e{font-weight:700}
.bd-p{color:var(--muted);white-space:nowrap}
.bd-en{color:var(--muted)}
.adv{padding:14px 22px}
.adv>summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:10px}
.adv>summary::-webkit-details-marker{display:none}
.adv>summary::before{content:"";width:9px;height:9px;border-right:2px solid var(--accent);border-bottom:2px solid var(--accent);transform:rotate(-45deg);transition:transform .15s;flex:none}
.adv[open]>summary::before{transform:rotate(45deg)}
.adv>summary h3{font-size:1.375rem;font-weight:700;margin:0;display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px}
.adv[open]>summary{margin-bottom:14px}
.adv .prose{display:block;max-width:none}.adv .prose>p,.adv .ps-ways{max-width:80ch}
.ps-ways{margin:0 0 14px;padding-left:1.4em;max-width:80ch}.ps-ways li{margin:0 0 6px}
.ps-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(340px,1fr));gap:14px;margin:4px 0 14px}
.ps-card{background:var(--bg);border:1px solid var(--rule);border-radius:12px;padding:14px 18px}
.ps-card h4{margin:0 0 6px;font-size:1.1875rem}
.ps-card p{margin:0 0 8px}.ps-card .ps-other{margin:10px 0 4px;color:var(--muted);font-size:1rem}
.ps-card ul{margin:0;padding-left:1.1em}.ps-card li{margin:0 0 5px}
.ps-l{font-weight:600}.ps-l::after{content:":"}
.ps-card i[lang] b,.ps-ways i[lang] b{color:var(--accent)}
.ps-note{color:var(--muted);font-size:1rem}
.ta-note a{color:var(--accent)}
/* the subjunctive sequence grid: two columns */
.ta.seq .ta-grid{grid-template-columns:auto repeat(2,minmax(0,1fr))}
.ta-sub{display:block;font-variant:normal;text-transform:none;letter-spacing:0;font-size:1rem;margin-top:2px}
.noun.more-off{display:none}
.charts.more-closed{justify-items:start}.charts.more-closed>.noun{width:100%;max-width:480px}
.more-bar{display:flex;flex-wrap:wrap;align-items:baseline;gap:6px 14px;margin-top:12px}
.more-btn{font:inherit;font-size:1rem;text-align:left;color:var(--accent);background:var(--surface);border:1px solid var(--rule);border-radius:18px;padding:4px 14px;cursor:pointer}
.more-btn::before{content:"+ "}.more-btn[aria-expanded="true"]::before{content:"− "}
.more-btn:hover{border-color:var(--accent)}.more-btn:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.more-note{margin:0;font-size:1rem;color:var(--muted);flex:1 1 300px}
.adv-tag{font-size:1rem;font-weight:600;color:var(--accent);font-variant:small-caps;text-transform:lowercase;letter-spacing:.08em;border:1px solid var(--accent);border-radius:999px;padding:0 10px}
@media (max-width:640px){.adv{padding:12px 14px}.ps-grid{grid-template-columns:1fr}.ps-card{padding:12px 14px}.bd-table td,.bd-table th{padding:7px 8px}.bd-end{display:none}.bd-box .bd-f,.bd-out .bd-f{font-size:1.1875rem}}
'''
