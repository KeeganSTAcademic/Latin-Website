"""Build data/decks/pronouns.json: demonstrative, relative, personal, interrogative, indefinite pronouns
and the pronominal (-īus) adjectives. Usage: python3 make_pronouns.py <decks dir>"""
import json, sys, os
D = sys.argv[1]
CASES = ["Nominative", "Genitive", "Dative", "Accusative", "Ablative"]
GN = {"m": "Masculine", "f": "Feminine", "n": "Neuter"}

def split(s): return [x.strip() for x in s.split(",")]

# English by case for a pronoun used on its own. sg/pl: (subject form, object form, possessive)
def eng(subj, obj, poss, q=""):
    return [f"{subj}{q} (subject)", f"of {obj}{q}" + (f", {poss}" if poss else ""), f"to / for {obj}{q}",
            f"{obj}{q} (direct object)", f"by / with / from {obj}{q}"]

# ---------- the pronouns: id -> (label, lemma, gloss, view, {g: (10 forms, 10 English)}, notes {(g,pi): note}) ----------
P = {}
def add(pid, label, lemma, gloss, view, cols, notes=None, table_only=()):
    P[pid] = dict(label=label, lemma=lemma, gloss=gloss, view=view, cols=cols, notes=notes or {}, table_only=set(table_only))

# is, ea, id
add("is", "is, ea, id", "is, ea, id", "he, she, it; this, that", "is", {
 "m": (split("is, eius, eī, eum, eō, eī, eōrum, eīs, eōs, eīs"), eng("he", "him", "his") + eng("they", "them", "their")),
 "f": (split("ea, eius, eī, eam, eā, eae, eārum, eīs, eās, eīs"), eng("she", "her", "her") + eng("they", "them", "their")),
 "n": (split("id, eius, eī, id, eō, ea, eōrum, eīs, ea, eīs"), eng("it", "it", "its") + eng("they", "them", "their")),
}, {("m", 5): "also spelled iī", ("m", 7): "also spelled iīs", ("m", 9): "also spelled iīs",
    ("f", 7): "also spelled iīs", ("f", 9): "also spelled iīs", ("n", 7): "also spelled iīs", ("n", 9): "also spelled iīs"})

def demo(stem_en, pl_en):
    """English for a demonstrative used on its own: this man / this woman / this thing."""
    out = {}
    for g, who in (("m", "man"), ("f", "woman"), ("n", "thing")):
        sg = f"{stem_en} {who}"; pl = f"{pl_en} {'men' if g == 'm' else 'women' if g == 'f' else 'things'}"
        out[g] = eng(sg, sg, "") + eng(pl, pl, "")
    return out

E = demo("this", "these")
add("hic", "hic, haec, hoc", "hic, haec, hoc", "this; he, she, it", "hic", {
 "m": (split("hic, huius, huic, hunc, hōc, hī, hōrum, hīs, hōs, hīs"), E["m"]),
 "f": (split("haec, huius, huic, hanc, hāc, hae, hārum, hīs, hās, hīs"), E["f"]),
 "n": (split("hoc, huius, huic, hoc, hōc, haec, hōrum, hīs, haec, hīs"), E["n"]),
})

def rel(n_word):
    return [f"{n_word} (subject)", f"whose, of {'whom' if n_word == 'who' else 'which'}", f"to / for {'whom' if n_word == 'who' else 'which'}",
            f"{'whom' if n_word == 'who' else 'which'} (direct object)", f"by / with / from {'whom' if n_word == 'who' else 'which'}"]
add("qui", "quī, quae, quod", "quī, quae, quod", "who, which, that", "qui", {
 "m": (split("quī, cuius, cui, quem, quō, quī, quōrum, quibus, quōs, quibus"), rel("who") * 2),
 "f": (split("quae, cuius, cui, quam, quā, quae, quārum, quibus, quās, quibus"), rel("who") * 2),
 "n": (split("quod, cuius, cui, quod, quō, quae, quōrum, quibus, quae, quibus"), rel("which") * 2),
})

# ---------- Latin III and up ----------
add("ego", "ego (1st person)", "ego, meī", "I, me; we, us", "personal", {
 "p1": (["ego", "meī", "mihi", "mē", "mē", "nōs", "nostrum / nostrī", "nōbīs", "nōs", "nōbīs"],
        ["I (subject)", "of me", "to / for me", "me (direct object)", "by / with / from me",
         "we (subject)", "of us", "to / for us", "us (direct object)", "by / with / from us"]),
}, {("p1", 4): "with me = mēcum", ("p1", 9): "with us = nōbīscum",
    ("p1", 6): "nostrum: of us, one of us (ūnus nostrum); nostrī: of us, as in thinking of us (memor nostrī)"})
add("tu", "tū (2nd person)", "tū, tuī", "you", "personal", {
 "p2": (["tū", "tuī", "tibi", "tē", "tē", "vōs", "vestrum / vestrī", "vōbīs", "vōs", "vōbīs"],
        ["you (subject)", "of you", "to / for you", "you (direct object)", "by / with / from you",
         "you all (subject)", "of you all", "to / for you all", "you all (direct object)", "by / with / from you all"]),
}, {("p2", 4): "with you = tēcum", ("p2", 9): "with you all = vōbīscum",
    ("p2", 6): "vestrum: of you, one of you (ūnus vestrum); vestrī: of you, as in thinking of you (memor vestrī)"})
add("sui", "suī (reflexive)", "—, suī", "himself, herself, itself, themselves", "reflexive", {
 "rf": (["—", "suī", "sibi", "sē", "sē", "—", "suī", "sibi", "sē", "sē"],
        ["(no nominative)", "of himself / herself / itself", "to / for himself / herself / itself",
         "himself / herself / itself (direct object)", "by / with / from himself / herself / itself",
         "(no nominative)", "of themselves", "to / for themselves", "themselves (direct object)", "by / with / from themselves"]),
}, {("rf", 3): "also sēsē; it refers back to the subject of its own clause", ("rf", 4): "with himself = sēcum",
    ("rf", 8): "also sēsē; it refers back to the subject of its own clause", ("rf", 9): "with themselves = sēcum"},
 table_only=[("rf", 0), ("rf", 5)])

E = demo("that", "those")
add("ille", "ille, illa, illud", "ille, illa, illud", "that; he, she, it", "ille", {
 "m": (split("ille, illīus, illī, illum, illō, illī, illōrum, illīs, illōs, illīs"), E["m"]),
 "f": (split("illa, illīus, illī, illam, illā, illae, illārum, illīs, illās, illīs"), E["f"]),
 "n": (split("illud, illīus, illī, illud, illō, illa, illōrum, illīs, illa, illīs"), E["n"]),
})
E = demo("that", "those")
E = {g: [x.replace("that ", "that ").replace("those ", "those ") for x in v] for g, v in E.items()}
add("iste", "iste, ista, istud", "iste, ista, istud", "that (of yours)", "iste", {
 "m": (split("iste, istīus, istī, istum, istō, istī, istōrum, istīs, istōs, istīs"), E["m"]),
 "f": (split("ista, istīus, istī, istam, istā, istae, istārum, istīs, istās, istīs"), E["f"]),
 "n": (split("istud, istīus, istī, istud, istō, ista, istōrum, istīs, ista, istīs"), E["n"]),
})

def self_en():
    out = {}
    for g, s, o, pl in (("m", "he himself", "him himself", "they themselves"), ("f", "she herself", "her herself", "they themselves"),
                        ("n", "it itself", "it itself", "they themselves")):
        po = "them themselves"
        out[g] = [f"{s} (subject)", f"of {o}", f"to / for {o}", f"{o} (direct object)", f"by / with / from {o}",
                  f"{pl} (subject)", f"of {po}", f"to / for {po}", f"{po} (direct object)", f"by / with / from {po}"]
    return out
E = self_en()
add("ipse", "ipse, ipsa, ipsum", "ipse, ipsa, ipsum", "himself, herself, itself; the very", "ipse", {
 "m": (split("ipse, ipsīus, ipsī, ipsum, ipsō, ipsī, ipsōrum, ipsīs, ipsōs, ipsīs"), E["m"]),
 "f": (split("ipsa, ipsīus, ipsī, ipsam, ipsā, ipsae, ipsārum, ipsīs, ipsās, ipsīs"), E["f"]),
 "n": (split("ipsum, ipsīus, ipsī, ipsum, ipsō, ipsa, ipsōrum, ipsīs, ipsa, ipsīs"), E["n"]),
})
E = demo("the same", "the same")
add("idem", "īdem, eadem, idem", "īdem, eadem, idem", "the same", "idem", {
 "m": (split("īdem, eiusdem, eīdem, eundem, eōdem, eīdem, eōrundem, eīsdem, eōsdem, eīsdem"), E["m"]),
 "f": (split("eadem, eiusdem, eīdem, eandem, eādem, eaedem, eārundem, eīsdem, eāsdem, eīsdem"), E["f"]),
 "n": (split("idem, eiusdem, eīdem, idem, eōdem, eadem, eōrundem, eīsdem, eadem, eīsdem"), E["n"]),
}, {("m", 5): "also spelled īdem or iīdem", ("m", 7): "also spelled īsdem", ("m", 9): "also spelled īsdem",
    ("f", 7): "also spelled īsdem", ("f", 9): "also spelled īsdem", ("n", 7): "also spelled īsdem", ("n", 9): "also spelled īsdem"})

def q_en(word, obj):
    return [f"{word}? (subject)", f"whose? of {obj}?", f"to / for {obj}?", f"{obj}? (direct object)", f"by / with / from {obj}?"]
add("quis", "quis, quid (interrogative)", "quis, quid", "who? what?", "quis", {
 "m": (split("quis, cuius, cui, quem, quō, quī, quōrum, quibus, quōs, quibus"), q_en("who", "whom") * 2),
 "f": (split("quis, cuius, cui, quem, quō, quae, quārum, quibus, quās, quibus"), q_en("who", "whom") * 2),
 "n": (split("quid, cuius, cui, quid, quō, quae, quōrum, quibus, quae, quibus"),
       [x.replace("whose? of what?", "of what?") for x in q_en("what", "what")] * 2),
}, {("m", 0): "as an adjective (which man?): quī", ("n", 0): "as an adjective (which thing?): quod",
    ("n", 3): "as an adjective (which thing?): quod"})

def some_en(sg_m, sg_f, sg_n, pl):
    return {"m": eng(sg_m, sg_m, "") + eng(pl, pl, ""), "f": eng(sg_f, sg_f, "") + eng(pl, pl, ""),
            "n": eng(sg_n, sg_n, "") + eng(pl.replace("people", "things"), pl.replace("people", "things"), "")}
E = some_en("someone", "someone", "something", "some people")
add("aliquis", "aliquis, aliquid", "aliquis, aliquid", "someone, something", "aliquis", {
 "m": (split("aliquis, alicuius, alicui, aliquem, aliquō, aliquī, aliquōrum, aliquibus, aliquōs, aliquibus"), E["m"]),
 "f": (split("aliqua, alicuius, alicui, aliquam, aliquā, aliquae, aliquārum, aliquibus, aliquās, aliquibus"), E["f"]),
 "n": (split("aliquid, alicuius, alicui, aliquid, aliquō, aliqua, aliquōrum, aliquibus, aliqua, aliquibus"), E["n"]),
}, {("n", 0): "as an adjective (some thing): aliquod", ("n", 3): "as an adjective (some thing): aliquod",
    ("m", 0): "as an adjective (some man): aliquī"})
E = some_en("a certain man", "a certain woman", "a certain thing", "certain people")
add("quidam", "quīdam, quaedam, quiddam", "quīdam, quaedam, quiddam", "a certain (one)", "quidam", {
 "m": (split("quīdam, cuiusdam, cuidam, quendam, quōdam, quīdam, quōrundam, quibusdam, quōsdam, quibusdam"), E["m"]),
 "f": (split("quaedam, cuiusdam, cuidam, quandam, quādam, quaedam, quārundam, quibusdam, quāsdam, quibusdam"), E["f"]),
 "n": (split("quiddam, cuiusdam, cuidam, quiddam, quōdam, quaedam, quōrundam, quibusdam, quaedam, quibusdam"), E["n"]),
}, {("n", 0): "as an adjective (a certain thing): quoddam", ("n", 3): "as an adjective (a certain thing): quoddam"})

# ---------- more indefinites (A&G §§149, 151, 310–313) ----------
X = "—"   # no such form: shown as a dash in the charts, never studied
def rel_en(subj, obj):
    one = [f"{subj} (subject)", f"of {obj}", f"to / for {obj}", f"{obj} (direct object)", f"by / with / from {obj}"]
    return one * 2
E = some_en("anyone", "anyone", "anything", "any people")
add("quisindef", "quis, quid (indefinite)", "quis, qua, quid", "anyone, anything (after sī, nisi, num, nē)", "quisindef", {
 "m": (split("quis, cuius, cui, quem, quō, quī, quōrum, quibus, quōs, quibus"), E["m"]),
 "f": (split("qua, cuius, cui, quam, quā, quae, quārum, quibus, quās, quibus"), E["f"]),
 "n": (split("quid, cuius, cui, quid, quō, qua, quōrum, quibus, qua, quibus"), E["n"]),
}, {("f", 0): "also quae", ("n", 5): "also quae", ("n", 8): "also quae",
    ("m", 0): "as an adjective (any man): quī", ("n", 0): "as an adjective (any thing): quod", ("n", 3): "as an adjective (any thing): quod"})

E = some_en("anyone at all", "anyone at all", "anything at all", "any people at all")
NOPL = "no plural: ūllus supplies it"
add("quisquam", "quisquam, quidquam", "quisquam, quidquam", "anyone at all, anything at all (in negative sentences)", "quisquam", {
 "m": (split("quisquam, cuiusquam, cuiquam, quemquam, quōquam") + [X] * 5, E["m"]),
 "f": ([X] * 10, E["f"]),
 "n": (split("quidquam, cuiusquam, cuiquam, quidquam, quōquam") + [X] * 5, E["n"]),
}, {**{("m", i): NOPL for i in range(5, 10)}, **{("n", i): NOPL for i in range(5, 10)},
    **{("f", i): "no feminine: quisquam covers anyone at all, man or woman" for i in range(10)},
    ("n", 0): "also spelled quicquam", ("n", 3): "also spelled quicquam"},
 table_only=[("m", i) for i in range(5, 10)] + [("n", i) for i in range(5, 10)] + [("f", i) for i in range(10)])

E = some_en("each man", "each woman", "each thing", "each of them")
add("quisque", "quisque, quidque", "quisque, quaeque, quidque", "each, every", "quisque", {
 "m": (split("quisque, cuiusque, cuique, quemque, quōque, quīque, quōrumque, quibusque, quōsque, quibusque"), E["m"]),
 "f": (split("quaeque, cuiusque, cuique, quamque, quāque, quaeque, quārumque, quibusque, quāsque, quibusque"), E["f"]),
 "n": (split("quidque, cuiusque, cuique, quidque, quōque, quaeque, quōrumque, quibusque, quaeque, quibusque"), E["n"]),
}, {("m", 0): "as an adjective (each man): quīque", ("n", 0): "as an adjective (each thing): quodque; also spelled quicque",
    ("n", 3): "as an adjective (each thing): quodque; also spelled quicque", ("m", 5): "the plural is rare"})

add("quicumque", "quīcumque, quaecumque, quodcumque", "quīcumque, quaecumque, quodcumque", "whoever, whatever", "quicumque", {
 "m": (split("quīcumque, cuiuscumque, cuicumque, quemcumque, quōcumque, quīcumque, quōrumcumque, quibuscumque, quōscumque, quibuscumque"), rel_en("whoever", "whomever")),
 "f": (split("quaecumque, cuiuscumque, cuicumque, quamcumque, quācumque, quaecumque, quārumcumque, quibuscumque, quāscumque, quibuscumque"), rel_en("whoever", "whomever")),
 "n": (split("quodcumque, cuiuscumque, cuicumque, quodcumque, quōcumque, quaecumque, quōrumcumque, quibuscumque, quaecumque, quibuscumque"), rel_en("whatever", "whatever")),
})

add("quisquis", "quisquis, quidquid", "quisquis, quidquid", "whoever, whatever", "quisquis", {
 "m": (["quisquis", X, "cuicui", "quemquem", "quōquō", "quīquī", X, "quibusquibus", X, "quibusquibus"], rel_en("whoever", "whomever")),
 "f": ([X, X, X, X, "quāquā", X, X, X, X, X], rel_en("whoever", "whomever")),
 "n": (["quidquid", X, X, "quidquid", "quōquō", X, X, X, X, X], rel_en("whatever", "whatever")),
}, {("m", 2): "rare: found in cuicui modī, of whatever kind", ("m", 3): "rare", ("m", 5): "early Latin only", ("m", 7): "rare", ("m", 9): "rare",
    ("f", 4): "late and rare", ("n", 0): "also spelled quicquid", ("n", 3): "also spelled quicquid",
    ("m", 4): "mostly as an adjective: quōquō modō, in whatever way",
    **{("m", i): "no such form" for i in (1, 6, 8)}, **{("f", i): "quisquis is hardly ever feminine" for i in (0, 1, 2, 3, 5, 6, 7, 8, 9)},
    **{("n", i): "no such form" for i in (1, 2, 5, 6, 7, 8, 9)}},
 table_only=[("m", i) for i in (1, 6, 8)] + [("f", i) for i in (0, 1, 2, 3, 5, 6, 7, 8, 9)] + [("n", i) for i in (1, 2, 5, 6, 7, 8, 9)])

for _pid in ("quisquam", "quisquis"):   # the dashes get no English
    for _g, (_forms, _ens) in P[_pid]["cols"].items():
        for _i, _f in enumerate(_forms):
            if _f == X: _ens[_i] = "(no such form)"

# ---------- pronominal adjectives (genitive -īus, dative -ī): ūnus nauta ----------
def pa(m_nom, stem, n_nom=None, gen=None, gloss=""):
    n_nom = n_nom or stem + "um"
    g = gen or stem + "īus"
    m = [m_nom, g, stem + "ī", stem + "um", stem + "ō", stem + "ī", stem + "ōrum", stem + "īs", stem + "ōs", stem + "īs"]
    f = [stem + "a", g, stem + "ī", stem + "am", stem + "ā", stem + "ae", stem + "ārum", stem + "īs", stem + "ās", stem + "īs"]
    n = [n_nom, g, stem + "ī", n_nom, stem + "ō", stem + "a", stem + "ōrum", stem + "īs", stem + "a", stem + "īs"]
    return {"m": (m, [gloss] * 10), "f": (f, [gloss] * 10), "n": (n, [gloss] * 10)}
PA = [("unus", "ūnus, ūna, ūnum", "one; only", pa("ūnus", "ūn", gloss="one")),
      ("ullus", "ūllus, ūlla, ūllum", "any", pa("ūllus", "ūll", gloss="any")),
      ("nullus", "nūllus, nūlla, nūllum", "no, none", pa("nūllus", "nūll", gloss="no, none")),
      ("solus", "sōlus, sōla, sōlum", "alone, only", pa("sōlus", "sōl", gloss="alone, only")),
      ("neuter", "neuter, neutra, neutrum", "neither (of two)", pa("neuter", "neutr", gloss="neither (of two)")),
      ("alius", "alius, alia, aliud", "other, another", pa("alius", "ali", n_nom="aliud", gen="alterīus", gloss="other, another")),
      ("uter", "uter, utra, utrum", "which (of two)?", pa("uter", "utr", gloss="which (of two)?")),
      ("totus", "tōtus, tōta, tōtum", "whole, all", pa("tōtus", "tōt", gloss="whole, all")),
      ("alter", "alter, altera, alterum", "the other (of two)", pa("alter", "alter", gloss="the other (of two)"))]
for pid, lemma, gloss, cols in PA:
    cols["f"][0][0] = cols["f"][0][0]  # (forms already right; alter's feminine is altera from stem alter-)
    add(pid, lemma, lemma, gloss, "pronadj", cols,
        {("m", 1): "alīus is rare; the genitive used is alterīus"} if pid == "alius" else
        {("m", 5): "the plural means \"only\" or goes with plural-only nouns (ūna castra, one camp)"} if pid == "unus" else {})

# ---------- cards ----------
COLS = {"m": "Masculine", "f": "Feminine", "n": "Neuter", "p1": "1st person", "p2": "2nd person", "rf": "Reflexive"}
cards = []
for pid, p in P.items():
    for g, (forms, ens) in p["cols"].items():
        assert len(forms) == 10 and len(ens) == 10, (pid, g)
        for i in range(10):
            num = "sg" if i < 5 else "pl"
            gl = "" if g in ("p1", "p2", "rf") else " " + GN[g]
            c = {"la": forms[i], "en": ens[i], "pn": f"{CASES[i % 5]} {'Singular' if num == 'sg' else 'Plural'}{gl}",
                 "tag": f"{p['lemma']} · {p['gloss']}", "pron": pid, "g": g, "num": num, "pi": i,
                 "lemma": p["lemma"], "gloss": p["gloss"]}
            c["set"] = p["view"]
            if (g, i) in p["notes"]: c["note"] = p["notes"][(g, i)]
            if (g, i) in p["table_only"]: c["tableOnly"] = True
            cards.append(c)

VIEWS = [  # view id, title, short (sidebar), pronoun ids, path (tree in the sidebar, grouped by type)
 ("personal", "Personal Pronouns: ego, tū, is", "Personal: ego, tū, is", ["ego", "tu", "is"], ["Pronouns"]),
 ("reflexive", "Reflexive Pronoun: suī", "Reflexive: suī", ["sui"], ["Pronouns"]),
 ("is", "Is, ea, id", "is, ea, id", ["is"], ["Pronouns", "Demonstrative"]),
 ("hic", "Hic, haec, hoc", "hic, haec, hoc", ["hic"], ["Pronouns", "Demonstrative"]),
 ("ille", "Ille, illa, illud", "ille, illa, illud", ["ille"], ["Pronouns", "Demonstrative"]),
 ("iste", "Iste, ista, istud", "iste, ista, istud", ["iste"], ["Pronouns", "Demonstrative"]),
 ("idem", "Īdem, eadem, idem", "īdem, eadem, idem", ["idem"], ["Pronouns", "Demonstrative"]),
 ("ipse", "Intensive Pronoun: ipse", "Intensive: ipse", ["ipse"], ["Pronouns"]),
 ("qui", "Relative Pronoun: quī, quae, quod", "Relative: quī", ["qui"], ["Pronouns"]),
 ("quis", "Interrogative Pronoun: quis, quid", "Interrogative: quis", ["quis"], ["Pronouns"]),
 ("aliquis", "Aliquis, aliquid", "aliquis, aliquid", ["aliquis"], ["Pronouns", "Indefinite"]),
 ("quidam", "Quīdam, quaedam, quiddam", "quīdam, quaedam, quiddam", ["quidam"], ["Pronouns", "Indefinite"]),
 ("quisindef", "Quis after sī, nisi, num, nē", "quis after sī, nisi, num, nē", ["quisindef"], ["Pronouns", "Indefinite"]),
 ("quisquam", "Quisquam, quidquam", "quisquam, quidquam", ["quisquam"], ["Pronouns", "Indefinite"]),
 ("quisque", "Quisque, quidque", "quisque, quidque", ["quisque"], ["Pronouns", "Indefinite"]),
 ("quisquis", "Quisquis, quidquid", "quisquis, quidquid", ["quisquis"], ["Pronouns", "Indefinite"]),
 ("quicumque", "Quīcumque, quaecumque, quodcumque", "quīcumque, quaecumque, quodcumque", ["quicumque"], ["Pronouns", "Indefinite"]),
 ("pronadj", "Pronominal Adjectives (ūnus nauta)", "Pronominal adjectives (ūnus nauta)", [x[0] for x in PA], ["Pronouns"]),
]
intro = ("<ul>"
 "<li><b>Genitive and dative singular:</b> most pronouns have <span class=\"end\">-īus</span> in the genitive and "
 "<span class=\"end\">-ī</span> in the dative, for all three genders (illīus, illī; ipsīus, ipsī). <i>Is</i>, <i>quī</i> and <i>hic</i> "
 "do the same with their own spellings: eius, eī; cuius, cui; huius, huic.</li>"
 "<li><b>Is, ea, id</b> is the everyday 3rd-person pronoun (he, she, it). Its genitive (eius, eōrum, eārum) means "
 "his, her, its, their when it is <i>not</i> the subject's own; for the subject's own, Latin uses suus.</li>"
 "<li><b>Quī, quae, quod</b> takes its gender and number from the word it refers to, and its case from its own clause.</li>"
 "<li><b>Suī</b> has no nominative: it always points back to the subject of its own clause.</li>"
 "<li><b>Ūnus nauta</b> (ūnus, ūllus, nūllus, sōlus, neuter, alius, uter, tōtus, alter): ordinary -us, -a, -um adjectives except for "
 "the genitive <span class=\"end\">-īus</span> and dative <span class=\"end\">-ī</span> singular.</li>"
 "</ul>")
d = {"id": "pronouns", "title": "Pronouns", "course": "Pronouns", "intro": intro, "paradigmNote": "",
     "filters": [{"field": "set", "label": "Set", "values": [{"v": v[0], "label": v[1]} for v in VIEWS]},
                 {"field": "pron", "label": "Pronoun", "values": [{"v": k, "label": v["label"]} for k, v in P.items()]},
                 {"field": "g", "label": "Gender", "values": [{"v": k, "label": v} for k, v in COLS.items()]},
                 {"field": "num", "label": "Number", "values": [{"v": "sg", "label": "Singular"}, {"v": "pl", "label": "Plural"}]}],
     "modes": ["le", "el"], "allReadings": "pron", "cue": "Translate: give every possible reading",
     "meta": {"front": ["{tag}", ""], "back": ["{tag}", ""]},
     "paradigm": {"table": "g", "group": "pron", "headings": {k: v["lemma"] for k, v in P.items()},
                  "rows": CASES, "rowLabel": "Case", "tableSuffix": ""},
     "views": {vid: {"title": t, "sel": {"set": sorted({P[i]["view"] for i in ids} | {vid})}, "groups": ids} for vid, t, s, ids, path in VIEWS},
     "cards": cards}
json.dump(d, open(os.path.join(D, "pronouns.json"), "w"), ensure_ascii=False, indent=1)

# index entries + counts (study cards only; Latin → English shows each spelling once per pronoun)
entries = []
for vid, t, s, ids, path in VIEWS:
    n = sum(1 for c in cards if c["pron"] in ids and not c.get("tableOnly"))
    entries.append({"id": "pronouns", "title": t, "course": "Pronouns", "count": n, "view": vid, "path": path, "short": s})
json.dump(entries, open("pron_index.json", "w"), ensure_ascii=False)
for pid, p in P.items():
    for g, (forms, _) in p["cols"].items(): print(f"{pid:8} {g:2} " + " ".join(forms[:5]) + " | " + " ".join(forms[5:]))
print(len(cards), "cards;", [(e["view"], e["count"]) for e in entries])
