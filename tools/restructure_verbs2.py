"""Rebuild the verb pages in the pronoun-page layout (no folds below the charts):
header -> intro with the time/aspect grid -> The forms (charts, sum, inspector) -> How to build it
-> The basic use -> the site's own analogy panel -> Other uses -> Other forms -> extra reference blocks.
Starts from the original pages (with their Background folds), so it can be re-run.
Usage: python3 restructure_verbs2.py <original pages dir> <site dir>"""
import re, sys, os, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verb_content import PAGES, TA, SIMPLE, WHERE
from verb_build import breakdown, PERFECT_STEM

SRC, SITE = sys.argv[1], sys.argv[2]

BUILD_NOTES = {
 "present-active": ('<p>Cut <i>-re</i> off the infinitive, the 2nd principal part, to get the incomplete stem (<i>amā-, monē-</i>), then add the personal ending, which tells you who is doing the action. '
   'The ending must agree with the subject. These endings are used throughout the verb system, so they are worth memorizing first.</p>'
   '<p>In the 3rd conjugation the short linking vowel <i>-e-</i> changes to <i>-i-</i> in most forms and to <i>-u-</i> in the 3rd plural: <i>regis, regit; regunt</i>. '
   'The Romans seem simply to have preferred the sound. The change is inconvenient, but it is worth learning now, because later it is how you tell the present (<i>regit</i>) from the future (<i>reget</i>).</p>', ''),
 "imperfect-active": ('<p>The imperfect uses the same stem and personal endings as the present, with <i>-ba-</i> placed between them. The one different ending is <i>-m</i>, not <i>-ō</i>, for "I." '
   'The <i>a</i> in <i>-ba-</i> is the time vowel: Latin tends to use <i>a</i> for past time (compare <i>eram</i>, "I was"), and the same vowel appears in English "was," which can help you remember it.</p>',
   '<p>In the 3rd conjugation the linking vowel goes back to <i>-ē-</i> (<i>regēbam</i>), and the 3rd <i>-iō</i> and 4th conjugations use <i>-iē-</i> (<i>capiēbam, audiēbam</i>).</p>'),
 "future-active": ('<p>In the 1st and 2nd conjugations, the future places <i>-bi-</i> between the stem and the personal ending. The <i>i</i> in <i>-bi-</i> is the time vowel: Latin tends to use <i>i</i> for future time '
   '(compare <i>erit</i>, "he will be"), and the same vowel appears in English "will," which can help you remember it.</p>',
   '<p>Two forms change the <i>-i-</i>: the 1st singular ends in <i>-bō</i> and the 3rd plural in <i>-bunt</i>. In <i>amābō</i> the <i>ō</i> seems to have swallowed the <i>i</i>; '
   'in <i>amābunt</i> it became <i>u</i>, the same change as <i>regunt</i> in the present.</p>'
   '<p>The 3rd, 3rd <i>-iō</i> and 4th conjugations do not use <i>-bi-</i>. Their future is marked by a vowel shift: <i>-a-</i> in the 1st singular and <i>-ē-</i> in the other forms, '
   'shortened to <i>-e-</i> before <i>-t</i> and <i>-nt</i>: <i>regam, regēs, reget, regēmus, regētis, regent</i>. These vowels are not the time vowels described above; '
   'the <i>a</i> of <i>regam</i> does not mean past. Watch the look-alikes this creates: <i>reget</i>, "he will rule," and <i>regit</i>, "he rules," differ by one vowel.</p>'),
 "perfect-active": ('<p>Take the 3rd principal part and drop the <i>-ī</i> to get the complete stem. The 3rd principal part is the base for every complete tense in the active, '
   'the way the 2nd principal part is the base for the incomplete ones. The perfect has its own set of endings: <i>-ī, -istī, -it, -imus, -istis, -ērunt</i>.</p>', ''),
 "pluperfect-active": ('<p>Take the complete stem (the 3rd principal part minus <i>-ī</i>) and add <i>-eram, -erās, -erat, -erāmus, -erātis, -erant</i>, which are the forms of <i>eram</i>, "I was." '
   'So <i>amāv-era-t</i> has three parts: the complete stem, <i>-era-</i>, and the personal ending <i>-t</i>. The <i>a</i> in <i>-era-</i> is the time vowel; Latin tends to use <i>a</i> for past time, as in the imperfect\'s <i>-ba-</i>.</p>', ''),
 "future-perfect-active": ('<p>Take the complete stem (the 3rd principal part minus <i>-ī</i>) and add <i>-erō, -eris, -erit, -erimus, -eritis, -erint</i>, which are the forms of <i>erō</i>, "I will be," '
   'except that the 3rd plural is <i>-erint</i>, not <i>-erunt</i>. The <i>i</i> in <i>-eri-</i> is the time vowel; Latin tends to use <i>i</i> for future time, as in the future\'s <i>-bi-</i>.</p>', ''),
 "complete-passive": ('<p>Take the 4th principal part, the perfect passive participle (<i>amātus, -a, -um</i>, "loved"), and add a form of <i>sum</i>. '
   'The participle carries the complete aspect, and <i>sum</i> carries the time, person and number: the present <i>sum</i> for the perfect, the imperfect <i>eram</i> for the pluperfect, '
   'and the future <i>erō</i> for the future perfect. Because the participle is an adjective, its ending agrees with the subject: <i>amātus est</i> for a man, <i>amāta est</i> for a woman, '
   '<i>amātī sunt</i> for a group.</p>', ''),
 "incomplete-passive": ('<p>The passive uses the same stem, stem vowel and time marker as the active; only the personal ending is different. <i>Amā-ba-t</i>, "he was loving," becomes <i>amā-bā-tur</i>, "he was being loved." '
   'Most passive endings look like the active endings with an <i>r</i> added; only <i>-minī</i> is completely different. In the 3rd and 4th conjugations the future passive uses the same vowel shift as the future active in place of <i>-bi-</i>: <i>regar, regēris, regētur</i>.</p>', ''),
}

# pages whose other conjugations add nothing new: (only these tense groups, or None for all; note beside the button)
SAME = 'Every conjugation builds this tense the same way, from its own {pp} principal part.'
MORE = {'imperfect-active': (None, 'The other conjugations add <i>-ba-</i> the same way. The 3rd puts <i>ē</i> before it (<i>regēbam</i>), and the 3rd <i>-iō</i> and 4th put <i>iē</i> (<i>capiēbam, audiēbam</i>).'),
        'perfect-active': (None, SAME.format(pp='3rd')),
        'pluperfect-active': (None, SAME.format(pp='3rd')),
        'future-perfect-active': (None, SAME.format(pp='3rd')),
        'incomplete-passive': ('impf', 'The other conjugations change the imperfect the same way as the active: <i>regēbar, capiēbar, audiēbar</i>.'),
        'complete-passive': (None, SAME.format(pp='4th'))}

md = lambda s: re.sub(r'\*\*(.+?)\*\*', r'<b class="hl">\1</b>', s)

def exs(rows, big=False):
    return (f'<div class="exs{" big" if big else ""}">' + ''.join(
        f'<div class="ex"><div class="la" lang="la">{md(la)}</div><div class="en">{en}{f" <span class=src>{src}</span>" if src else ""}</div></div>'
        for la, en, src in rows) + '</div>')

TV = lambda la: re.sub(r'\[(.)\]', r'<b class="tv">\1</b>', la)

def ta_grid(cur):
    passive = cur in ("passive", "cpassive")
    voice = "passive" if passive else "active"
    rows = TA[voice]
    page_of = {tid: page for row in rows for tid, page, *_ in row}
    stems = (["built on <i lang=la>amā-</i> (2nd principal part)", "built on <i lang=la>amāv-</i> (3rd principal part)"] if not passive
             else ["built on <i lang=la>amā-</i> (2nd principal part)", "built on <i lang=la>amāt-</i> (4th principal part)"])
    out = [f'<figure class="ta{" show-simple" if cur in ("perfect", "cpassive") else ""}"><figcaption>Time and aspect</figcaption>',
           '<div class="ta-grid">',
           '<span class="ta-corner"></span>' + ''.join(f'<span class="ta-col">{c}</span>' for c in ("Past time", "Present time", "Future time"))]

    def cell(inner, on, href, extra=''):
        if on:
            return f'<span class="ta-c on{extra}" aria-current="page">{inner}</span>'
        if href:
            return f'<a class="ta-c{extra}" href="{href}">{inner}</a>'
        return f'<span class="ta-c off{extra}">{inner}<span class="eg">coming later</span></span>'

    def full_row(r, label, desc):
        out.append(f'<span class="ta-row"><b>{label}</b><br>{desc}<br>{stems[r]}</span>')
        simple_en = {src: sen for src, _n, _la, sen, _w in SIMPLE[voice]}
        for tid, page, name, la, en in rows[r]:
            on = (tid == cur) or (cur == "passive" and r == 0) or (cur == "cpassive" and r == 1)
            # with the simple row hidden, the box gives both translations; the simple row takes over the second when it is open
            if tid in simple_en:
                en = f'{en}<span class="ta-alt"> or {simple_en[tid]}</span>'
            here = '<span class="here">This page</span>' if on else ''
            out.append(cell(f'{here}<span class="nm">{name}</span><span class="la" lang="la">{TV(la)}</span><span class="eg">{en}</span>',
                            on, f'{page}.html'))

    full_row(0, "Incomplete", "the action is not finished")
    out.append('<span class="ta-row ta-s"><b>Simple</b><br>the action is neither finished nor unfinished<br>(secondary translation)</span>')
    for src, name, la, en, where in SIMPLE[voice]:
        also = src == cur or (cur == "passive" and src in ("present", "future")) or (cur == "cpassive" and src == "perfect")
        arw = '↖' if where == "diag" else '↓'
        title = f'also a meaning of the {name.lower()}'
        inner = (f'<span class="arw {where}" aria-hidden="true">{arw}</span>'
                 f'<span class="nm"><span class="arw-in" aria-hidden="true">{arw} </span>{name}</span><span class="la" lang="la">{TV(la)}</span><span class="eg">{en}</span>'
                 f'<span class="sr">({title})</span>')
        href = f'{page_of[src]}.html'
        if also:
            mine = src == cur or (cur == "cpassive" and src == "perfect")
            here = '<span class="here">This page</span>' if mine else ''
            out.append(f'<span class="ta-c simple on ta-s"{" aria-current=page" if mine else ""}>{here}{inner}</span>')
        else:
            out.append(cell(inner, False, href, ' simple ta-s'))
    full_row(1, "Complete", "the action is finished")
    out.append('</div>')
    out.append('<button type="button" class="ta-btn" aria-expanded="{exp}" onclick="var f=this.closest(\'.ta\');f.classList.toggle(\'show-simple\');this.setAttribute(\'aria-expanded\',f.classList.contains(\'show-simple\'))">Simple translations</button>'.replace('{exp}', 'true' if cur in ('perfect', 'cpassive') else 'false'))
    out.append('<p class="ta-note ta-s">The simple aspect describes an action that simply happens at a point in time. It works a little like a photograph: it captures an action at one moment, whether or not the action finished afterward. "He loved," rather than "he was loving" (incomplete past) or "he had loved" (complete past). By the time of the Romans, Latin had lost a separate stem for the simple aspect, but the {see} still carried the meaning of the simple past, and the present and future are used where English prefers a simple present or simple future.</p>'.replace('{see}', 'perfect' if cur == 'perfect' else '<a href="perfect-active.html">perfect</a>'))
    out.append('</figure>')
    return ''.join(out)

def folds_of(section):
    return {re.sub(r'<[^>]+>', '', m.group(1)).strip(): m.group(2).strip()
            for m in re.finditer(r'<details class="fold">\s*<summary>(.*?)</summary>(.*?)</details>', section, flags=re.S)}

def block(title, inner, cls=''):
    return f'  <div class="block{" " + cls if cls else ""}">\n    <h3>{title}</h3>\n    {inner}\n  </div>\n'

for page, T in PAGES.items():
    s = open(os.path.join(SRC, page + '.html')).read()
    m = re.search(r'<section id="background" class="bg">.*?</section>\n*', s, flags=re.S)
    old = folds_of(m.group(0)); s = s[:m.start()] + s[m.end():]
    s = re.sub(r'\s*<p class="subtitle">.*?</p>', '', s, count=1, flags=re.S)

    # the irregular sum chart stays visible: a plain panel instead of a fold
    s = re.sub(r'<details class="er" id="er">\s*<summary>(.*?)</summary>(.*?)</details>',
               lambda mm: f'<div class="er er-open" id="er">\n        <h4 class="er-h">{mm.group(1)}</h4>{mm.group(2)}</div>', s, count=1, flags=re.S)

    intro = (f'  <div class="intro" id="intro"><div class="intro-h"><span class="q">{T["q"]}</span><span class="sec">A&amp;G §§{T["secs"]}</span></div>'
             f'<p>{T["summary"]}</p>{ta_grid(T["cur"])}</div>\n\n')
    # intro goes right after the toolbar; the charts get a "The forms" heading
    i = s.index('  <div class="work">')
    s = s[:i] + intro + '  <div class="block">\n    <h3>The forms</h3>\n' + s[i:]
    # close the forms block after the work area, then add the rest
    j = s.index('</section>', i)
    before, after = BUILD_NOTES[page]
    table = next((v for k, v in old.items() if k.startswith('How to build')), '')
    table = re.sub(r'<p>\s*Take the incomplete stem.*?</p>', '', table, flags=re.S)  # imperfect: said in the notes already
    rest = ['  </div>\n']
    table = ''   # the breakdown shows amō; the all-conjugation tables are dropped
    table = re.sub(r'<p class="aside">The endings are.*?</p>', '', table, flags=re.S)   # listed in the breakdown table
    rest.append(block('How to build it', f'<div class="prose">{before}</div>{breakdown(T["cur"])}{table}{f"<div class=prose>{after}</div>" if after else ""}'))
    if T['cur'] in ('perfect', 'pluperfect', 'futperf'):
        rest.append('  <div class="block"><details class="fold adv"><summary><h3>How the 3rd principal part is formed <span class="adv-tag">advanced</span></h3></summary>\n'
                    f'    <div class="prose">{PERFECT_STEM}</div>\n  </details></div>\n')
    b = T["basic"]
    rest.append(f'  <div class="block basic"><h3>The basic use: {b["name"]} <span class="sec">A&amp;G §{b["sec"]}</span></h3>'
                f'<p class="rule">{b["rule"]}</p><p class="how"><b>{b.get("how_label", "How to spot it")}:</b> {b["how"]}</p>{exs(b["ex"], True)}</div>\n')
    if T.get("think"):
        rest.append(block(T["think"][0], f'<div class="prose">{T["think"][1]}</div>', 'think'))
    if T.get("uses"):
        cards = ''.join(f'<article class="use"><header><h4>{u["name"]}</h4><span class="sec">A&amp;G §{u["sec"]}</span></header>'
                        f'<p class="what">{u["what"]}</p><p class="clue"><b>Clue:</b> {u["clue"]}</p>{exs(u["ex"])}</article>' for u in T["uses"])
        rest.append(block('Other uses', f'<div class="uses">{cards}</div>'))
    if T.get("forms"):
        note, rows = T["forms"]
        body = ''.join(f'<tr><td>{w}</td><td><i lang="la">{ex}</i></td><td><i lang="la">{std}</i></td></tr>' for w, ex, std in rows)
        rest.append(block("Other forms you'll see", (f'<p class="how">{note}</p>' if note else '') +
                          '<div class="conj-box"><table class="rule-table conj-table forms-table"><thead><tr><th>What happens</th><th>You may see</th><th>Same as</th></tr></thead>'
                          f'<tbody>{body}</tbody></table></div>'))
    for title, tag in T.get("more", []):
        inner = old['What is a conjugation?'] if tag == '@conj' else re.sub(
            r'<p[^>]*>\s*<(?:b|strong)>What the present means\.</(?:b|strong)>.*?</p>', '',
            next(v for k, v in old.items() if k.startswith('Personal endings')), flags=re.S)
        rest.append(block(title, inner))
    s = s[:j] + ''.join(rest) + s[j:]

    # credit the use sections in the Sources note
    secs = sorted({int(u["sec"]) for u in T.get("uses", [])} | {int(T["basic"]["sec"])})
    word = "Uses" if page == "incomplete-passive" else "Tense uses"
    s = s.replace('</p>\n</footer>', f' {word} follow A&amp;G {"§§" if len(secs) > 1 else "§"}{", ".join(map(str, secs))}.</p>\n</footer>', 1)
    s = re.sub(r'\n[ \t]*<div class="primer">.*?</div>', '', s, count=1, flags=re.S)  # no chip row under the title
    c = '<script src="../js/common.js?v=202610011900"></script>\n'   # the account script loads right after common.js
    if 'account.js' not in s: s = s.replace(c, c + '<script src="../js/account.js?v=202610122000"></script>\n', 1)
    s = re.sub(r'glossary\.js\?v=\d+', 'glossary.js?v=202610131500', s)
    s = re.sub(r'grammar-verbs\.css\?v=\d+', 'grammar-verbs.css?v=202610150900', s)
    s = re.sub(r'verb-chart\.js\?v=\d+', 'verb-chart.js?v=202610150900', s)
    # conjugations that build the tense the same way as amō start collapsed (js/more-charts.js)
    if page in MORE:
        groups, note = MORE[page]
        attrs = f' data-show="amo"' + (f' data-groups="{groups}"' if groups else '') + f' data-more-note="{note}"'
        s = s.replace('<div class="charts-col" id="charts-col">', f'<div class="charts-col" id="charts-col"{attrs}>', 1)
        s = s.replace(c, c + '<script src="../js/more-charts.js?v=202610142000"></script>\n', 1)
    if 'hovercard.js' not in s and 'pattern-notes.js' in s:   # the hover/tap inspector (js/hovercard.js) goes after the pattern notes
        s = re.sub(r'(<script src="\.\./js/pattern-notes\.js\?v=\d+"></script>\n)', r'\1<script src="../js/hovercard.js?v=202610180900"></script>\n', s, 1)
    open(os.path.join(SITE, 'grammar', page + '.html'), 'w').write(s)
    print(page, len(s))
