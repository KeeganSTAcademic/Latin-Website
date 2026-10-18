"""Build the pronoun grammar pages (grammar/pronouns-*.html), one per type, in the style of the noun pages:
charts in noun-style cards, the inspector on the right (Ambiguous: could also be / Only a macron away),
look-alike dots, coloured pattern buttons whose notes show in the inspector (js/pattern-notes.js), and a legend.
The patterns follow the noun pages: where the noun endings still hold (-m, long-vowel ablative, -ī dative,
-a neuter plural, -rum genitive plural, -īs / -ibus), and where pronouns go their own way (-īus, -d, -e, -c).
Forms and English come from data/decks/pronouns.json, the rules from pronoun_content.py.
Usage: python3 make_pronoun_page.py <site dir>"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pronoun_content import TABS
SITE = sys.argv[1]
deck = json.load(open(os.path.join(SITE, "data/decks/pronouns.json")))
P = {}
for c in deck["cards"]:
    p = P.setdefault(c["pron"], {"lemma": c["lemma"], "gloss": c["gloss"], "cols": {}})
    col = p["cols"].setdefault(c["g"], [None] * 10)
    cell = {"f": c["la"], "en": c["en"]}
    if c.get("note"): cell["n"] = c["note"]
    if c.get("tableOnly"): cell["x"] = 1
    col[c["pi"]] = cell
for k, p in P.items():
    for g, col in p["cols"].items(): assert all(col), (k, g)

PAGES = {  # tab id -> (file, page title, sidebar short name, primer chips)
 "personal": ("pronouns-personal", "Personal Pronouns", "Personal: ego, tū, is",
   ["<b>Accusative = ablative</b> singular: <i>mē, tē</i>", "<b>-cum</b> on the end: <i>mēcum, tēcum</i>"]),
 "reflexive": ("pronouns-reflexive", "The Reflexive Pronoun", "Reflexive: suī",
   ["<b>No nominative</b>", "<b>Singular = plural</b>: <i>suī, sibi, sē</i>"]),
 "demonstrative": ("pronouns-demonstrative", "Demonstratives: Overview", "Overview",
   ["<b>hic</b> near me · <b>iste</b> near you · <b>ille</b> over there", "<b>Genitive</b> <i>-īus</i> · <b>dative</b> <i>-ī</i> in every gender"]),
 "dem-is": ("pronouns-is", "Is, ea, id", "is, ea, id", ["<b>Genitive</b> <i>eius</i> · <b>dative</b> <i>eī</i>", "Mostly <b>he, she, it</b>"]),
 "dem-hic": ("pronouns-hic", "Hic, haec, hoc", "hic, haec, hoc", ["<b>Near</b> the speaker: this", "<b>-c</b> from <i>-ce</i>: <i>hunc, hanc, huic</i>"]),
 "dem-ille": ("pronouns-ille", "Ille, illa, illud", "ille, illa, illud", ["<b>Away</b> from the speaker: that", "<b>Genitive</b> <i>illīus</i> · <b>dative</b> <i>illī</i>"]),
 "dem-iste": ("pronouns-iste", "Iste, ista, istud", "iste, ista, istud", ["<b>Near</b> the person spoken to", "Declined like <i>ille</i>"]),
 "dem-idem": ("pronouns-idem", "Īdem, eadem, idem", "īdem, eadem, idem", ["<b>is</b> + <b>-dem</b>", "<b>m → n</b> before d: <i>eundem</i>"]),
 "intensive": ("pronouns-intensive", "The Intensive Pronoun: Ipse", "Intensive: ipse",
   ["<b>Genitive</b> <i>ipsīus</i> · <b>dative</b> <i>ipsī</i>", "<b>Neuter</b> <i>ipsum</i>"]),
 "relative": ("pronouns-relative", "The Relative Pronoun", "Relative: quī",
   ["<b>Genitive</b> <i>cuius</i> · <b>dative</b> <i>cui</i> in every gender", "<b>quae</b>: f. sg. · f. pl. · n. pl."]),
 "interrogative": ("pronouns-interrogative", "The Interrogative Pronoun", "Interrogative: quis",
   ["<b>quis</b> who? · <b>quid</b> what?", "<b>quī</b> + a noun: which?"]),
 "indefinite": ("pronouns-indefinite", "Indefinites: Overview", "Overview",
   ["<b>quis</b> anyone · <b>aliquis</b> someone · <b>quīdam</b> a certain one", "All built on <i>quis</i> or <i>quī</i>"]),
 "indef-aliquis": ("pronouns-aliquis", "Aliquis, aliquid", "aliquis, aliquid",
   ["<b>ali-</b> + <i>quis</i>: someone", "<b>aliqua</b>, not <i>aliquae</i>"]),
 "indef-quidam": ("pronouns-quidam", "Quīdam, quaedam, quiddam", "quīdam, quaedam, quiddam",
   ["<b>quī</b> + <b>-dam</b>: a certain one", "<b>m → n</b> before d: <i>quendam</i>"]),
 "indef-quis": ("pronouns-quis-indef", "Quis after Sī, Nisi, Num, Nē", "quis after sī, nisi, num, nē", []),
 "indef-quisquam": ("pronouns-quisquam", "Quisquam, quidquam", "quisquam, quidquam", []),
 "indef-quisque": ("pronouns-quisque", "Quisque, quidque", "quisque, quidque", []),
 "indef-quisquis": ("pronouns-quisquis", "Quisquis, quidquid", "quisquis, quidquid", []),
 "indef-quicumque": ("pronouns-quicumque", "Quīcumque, quaecumque, quodcumque", "quīcumque, quaecumque, quodcumque", []),
 "unusnauta": ("pronouns-unus-nauta", "Pronominal Adjectives (Ūnus Nauta)", "Pronominal adjectives (ūnus nauta)",
   ["<b>Genitive</b> <i>-īus</i> · <b>dative</b> <i>-ī</i>", "Otherwise like <i>bonus, -a, -um</i>"]),
}
V = {"theme": "202610151000", "sb": "202610172300", "g": "202610071800", "common": "202610011900", "levels": "202610172240",
     "sbjs": "202610172300", "pn": "202610172240"}
FOOTER = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pronoun_footer.html")).read()

HTML = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pronoun_page_template.html")).read()
entries = []
for t in TABS:
    f, title, short, primer = PAGES[t["id"]]
    page = HTML
    for k, v in {"__TITLE__": title, "__PRIMER__": "\n".join(f"    <span>{x}</span>" for x in primer), "__FOOTER__": FOOTER,
                 "__G__": V["g"], "__SB__": V["sb"], "__THEME__": V["theme"], "__COMMON__": V["common"], "__LEVELS__": V["levels"],
                 "__SBJS__": V["sbjs"], "__PN__": V["pn"],
                 "__P__": json.dumps({p: P[p] for p in t["prons"]}, ensure_ascii=False), "__T__": json.dumps(t, ensure_ascii=False)}.items():
        page = page.replace(k, v)
    open(os.path.join(SITE, "grammar", f + ".html"), "w").write(page)
    e = {"page": f, "title": title, "short": short, "group": "Pronouns"}
    if t["id"] == "demonstrative" or t["id"].startswith("dem-"): e["path"] = ["Pronouns", "Demonstrative"]
    if t["id"] == "indefinite" or t["id"].startswith("indef-"): e["path"] = ["Pronouns", "Indefinite"]
    entries.append(e)
    print(f, len(page))
json.dump(entries, open("pron_grammar_entries.json", "w"), ensure_ascii=False)
