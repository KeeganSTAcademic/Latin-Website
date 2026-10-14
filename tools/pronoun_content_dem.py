# Demonstratives: an overview page plus one page per pronoun (A&G §§146, 296-298), adapted for Latin II-IV students.
# Spliced into TABS in place of the single "demonstrative" entry (see the end of pronoun_content.py).

def DIST(cur=None):
    """The distance diagram: hic / iste / ille along a line, is underneath as the in-between one.
    cur marks the pronoun of the page ("idem" marks is, which idem is built on)."""
    on = lambda k: ' on' if cur == k or (cur == "idem" and k == "is") else ''
    here = lambda k: '<span class="here">This page</span>' if cur == k else (
        '<span class="here">Īdem is built on this</span>' if cur == "idem" and k == "is" else '')
    st = lambda k, who, la, eg: (f'<div class="st{on(k)}">{here(k)}<span class="who">{who}</span>'
                                 f'<span class="la" lang="la">{la}</span><span class="eg">{eg}</span></div>')
    return ('<figure class="dist"><figcaption>How far away is it?</figcaption>'
            '<div class="dist-row">'
            + st("hic", "Near me", "hic, haec, hoc", "<b>this</b> book, the one in my hand")
            + st("iste", "Near you", "iste, ista, istud", "<b><em>that</em></b> book, the one by you")
            + st("ille", "Over there", "ille, illa, illud", "<b>that</b> book, the one across the room")
            + '</div><div class="dist-axis" aria-hidden="true"><span>closer</span><span>further away</span></div>'
            + st("is", "In between: doesn't say", "is, ea, id",
                 "<b>this</b>, <b>that</b>, or just <b>it</b>: the book we were talking about")
            + '</figure>')

MEANINGS = ('<div class="dem-table"><table><thead><tr><th>Pronoun</th><th>Points to</th><th>English</th><th>A&amp;G</th></tr></thead><tbody>'
  '<tr><td lang="la"><i>hic, haec, hoc</i></td><td>something near me, the speaker</td><td>this, these</td><td>§297.a</td></tr>'
  '<tr><td lang="la"><i>iste, ista, istud</i></td><td>something near you, the person I\'m talking to; often scornful</td><td><em>that</em> (of yours)</td><td>§297.c</td></tr>'
  '<tr><td lang="la"><i>ille, illa, illud</i></td><td>something away from both of us</td><td>that, those</td><td>§297.b</td></tr>'
  '<tr><td lang="la"><i>is, ea, id</i></td><td>something already mentioned, without saying how far away</td><td>this, that; mostly he, she, it</td><td>§297.d</td></tr>'
  '<tr><td lang="la"><i>īdem, eadem, idem</i></td><td>the very one already mentioned, again</td><td>the same</td><td>§298</td></tr>'
  '</tbody></table></div>')

DEM = [
 {"id": "demonstrative", "name": "Demonstratives", "q": "this, that", "prons": ["is", "hic", "ille", "iste", "idem"], "secs": "146, 296–298",
  "summary": "A <b>demonstrative</b> (from <i>dēmōnstrāre</i>, to point out) is a word that points: <i>this</i> book, <i>that</i> house. "
             "English has two, and they're about distance: <i>this</i> for what's near us, <i>that</i> for what's further off. "
             "Latin splits it more finely. <i>Hic</i> is near me, <i>iste</i> is near you, <i>ille</i> is over there, away from both of us. "
             "<i>Is</i> sits in between and doesn't say how far at all, and <i>īdem</i> (the same) is built on <i>is</i>. "
             "(If you take Spanish, <i>este, ese, aquel</i> work much the same way.) Each one has its own page; this page sets them side by side.",
  "extra": DIST() + MEANINGS,
  "pattern": "<b>Pattern:</b> all five share the pronoun genitive <i>-īus</i> and dative <i>-ī</i> in the singular (<i>illīus, illī</i>), which <i>is</i> and <i>hic</i> spell their own way (<i>eius, eī</i>; <i>huius, huic</i>). The neuter nominative and accusative singular end in <i>-d</i> (<i>id, illud, istud, idem</i>), except <i>hoc</i>. The plural is like <i>bonus, -a, -um</i>.",
  "basic": {"name": "Adjective or pronoun", "sec": "296",
   "rule": "Every demonstrative can do two functions. <b>As an adjective</b>, it goes with a noun and tells you <i>which one</i>: <i>haec puella</i>, this girl (not some other girl). "
           "Like any adjective it <b>agrees</b> with its noun, which means it takes the same case, number and gender. "
           "<b>As a pronoun</b>, it stands on its own, in place of a noun: <i>haec</i> by itself means this woman, or simply she. "
           "Its gender tells you what it stands for: masculine for a man, feminine for a woman, neuter for a thing.",
   "how": "Look for a noun nearby in the same case, number and gender. If there is one, the demonstrative is an adjective describing it. If there isn't, it's a pronoun: supply man, woman or thing (or he, she, it).",
   "ex": [["**Haec** puella cantat.", "This girl is singing. (<i>haec</i> goes with <i>puella</i>: an adjective)", ""],
          ["**Haec** cantat.", "This woman is singing, or simply: she is singing. (no noun: a pronoun)", ""],
          ["**hōc** proeliō factō", "after this battle was fought (<i>hōc</i> goes with <i>proeliō</i>)", "A&G §296"]]},
  "uses": [
   {"name": "Matching the noun after est", "sec": "296.a", "lvl": "core",
    "what": "In a sentence of the type <i>this is the X</i>, the demonstrative takes the gender of X, the noun after <i>est</i>, even when it's pointing at something else. "
            "In the example below, Cicero points at one place three times, but says <i>hic</i> with <i>portus</i> (masculine) and <i>haec</i> with <i>arx</i> (feminine).",
    "clue": "A demonstrative + a noun, meaning <i>this is the …</i>: check its gender against that noun.",
    "ex": [["**Hic** locus est ūnus quō perfugiant; **hic** portus, **haec** arx.", "This is the only place to which they can flee; this is the harbour, this the citadel.", "A&G §296.a"]]},
   {"name": "Neuter for a whole idea", "sec": "297.f", "lvl": "core",
    "what": "A neuter demonstrative (<i>id, hoc, illud</i>) can stand for a whole idea or fact, not just one thing. English does the same: <i>That</i> is a great thing, to see the soul. Here <i>that</i> means the whole idea of seeing the soul.",
    "clue": "A neuter <i>hoc, id</i> or <i>illud</i>, explained by an infinitive (a <i>to …</i> verb) or a whole clause (a group of words with its own verb).",
    "ex": [["Est **illud** quidem vel maximum, animum vidēre.", "That is truly a very great thing, to see the soul.", "A&G §297.f"]]},
   {"name": "Pointing back or forward", "sec": "297.e", "lvl": "adv",
    "what": "A demonstrative can point back to something already said (<i>this</i>, what I just told you) or forward to something about to be said (<i>this</i>: here's what happened).",
    "clue": "If a colon, an infinitive or a clause right after it explains what it means, it points forward.", "ex": []},
  ]},

 {"id": "dem-is", "name": "Is, ea, id", "q": "he, she, it; this, that", "prons": ["is"], "secs": "146, 296, 297.d",
  "summary": "<i>Is, ea, id</i> is the in-between demonstrative. <i>Hic</i> means this (near me) and <i>ille</i> means that (over there); <i>is</i> sits between them and doesn't say how far away anything is. "
             "It just points back to someone or something already mentioned. That's why English has no one word for it: depending on the sentence it comes out as this, that, or, most often, plain he, she, it, they. "
             "Latin has no separate word for he, she or it, so <i>is</i> performs that function, and for that reason it is also listed with the <a href=\"pronouns-personal.html\">personal pronouns</a>.",
  "extra": DIST("is"),
  "pattern": "<b>Pattern:</b> stem <i>e-</i> (<i>i-</i> in <i>is, id</i>). Genitive <i>eius</i> and dative <i>eī</i> in every gender; otherwise like <i>bonus</i>: <i>eum, eam, eō, eā; eōrum, eārum, eīs</i>. The plural <i>eī, eīs</i> is also spelled <i>iī, iīs</i> (§146).",
  "basic": {"name": "He, she, it, or this, that", "sec": "296",
   "rule": "Like the other demonstratives, <i>is</i> has two functions. <b>On its own</b>, as a pronoun, it stands in for a person or thing already mentioned: he, she, it, they. "
           "Its genitive (<i>eius</i>, of him, of her; <i>eōrum, eārum</i>, of them) gives you his, her, its, their. "
           "<b>With a noun</b>, as an adjective, it agrees with the noun and means this or that, without much stress: <i>ea rēs</i>, this matter.",
   "how": "If a noun in the same case, number and gender stands next to it, read this or that. If not, read he, she, it, him, her, them, and look back for the person or thing it means.",
   "ex": [["Mārcus vēnit. **Eum** videō.", "Marcus has come. I see him. (<i>eum</i> points back to Marcus)", ""],
          ["Caesar et exercitus **eius**", "Caesar and his army (<i>eius</i>: of him)", "A&G §296"],
          ["**ea** rēs", "this matter, that thing (with a noun)", ""]]},
  "uses": [
   {"name": "Is … quī: the one who", "sec": "297.d", "lvl": "core",
    "what": "A <b>relative clause</b> is a group of words that starts with <i>quī, quae, quod</i> (who, which) and describes someone or something: the man <i>who came</i>. "
            "<i>Is</i> often sets one up: <i>is quī</i>, the man who, the one who; <i>ea quae</i>, the woman who; <i>id quod</i>, the thing that.",
    "clue": "A form of <i>is</i> followed closely by a form of <i>quī</i>.",
    "ex": [["**Is** quī vēnit amīcus est.", "The man who came is a friend.", ""], ["**eum** quem", "the one whom", "A&G §297.d"]]},
   {"name": "Eius or suus?", "sec": "299", "lvl": "core",
    "what": "Both can be translated his or her. Latin uses <i>suus</i> when it belongs to the subject, the person doing the action, and <i>eius</i> when it belongs to someone else.",
    "clue": "Ask whose it is: the subject's own (<i>suus</i>), or someone else's (<i>eius</i>).",
    "ex": [["Caesar **suōs** mīlitēs laudat.", "Caesar praises his (own) soldiers.", ""], ["Caesar mīlitēs **eius** laudat.", "Caesar praises his soldiers (another man's).", ""]]},
   {"name": "Et is: and that too", "sec": "298.a", "lvl": "adv",
    "what": "<i>Et is</i> (or <i>et īdem</i>) adds an important detail about something just named, the way English says and that, and what's more.",
    "clue": "<i>Et ea, et id</i> right after a noun.",
    "ex": [["vincula, et **ea** sempiterna", "imprisonment, and that for life", "A&G §298.a"]]},
  ]},

 {"id": "dem-hic", "name": "Hic, haec, hoc", "q": "this (near me)", "prons": ["hic"], "secs": "146, 297.a",
  "summary": "<i>Hic, haec, hoc</i> is the near demonstrative: it points to something close to the speaker. It's the English <i>this</i>: this book is the one in my hand, this city is the one I'm in, these days are the ones we're living in. "
             "Near can mean near in place, near in time, or near in the conversation, so <i>hic</i> can also point to the thing just mentioned.",
  "extra": DIST("hic"),
  "pattern": "<b>Pattern:</b> <i>hic</i> is the stem <i>ho-</i> with the pointing word <i>-ce</i> (here, look) stuck on and worn down to <i>-c</i> (§146): <i>hic, haec, hoc, huic, hunc, hanc, hōc, hāc</i>. Genitive <i>huius</i>, dative <i>huic</i> in every gender. The rest of the plural is like <i>bonus</i>: <i>hī, hae, hōrum, hīs</i>.",
  "basic": {"name": "This, near me", "sec": "297.a",
   "rule": "<i>Hic</i> points at what is near the speaker. <b>With a noun</b>, as an adjective, it agrees with the noun and means this, these: <i>hic liber</i>, this book; <i>haec urbs</i>, this city. "
           "<b>On its own</b>, as a pronoun, it means this man, this woman, this thing, or simply he, she, it.",
   "how": "Read this or these. If no noun goes with it, let the gender tell you: <i>hic</i>, this man; <i>haec</i>, this woman (or these things); <i>hoc</i>, this thing.",
   "ex": [["**Hic** liber meus est.", "This book (here in my hand) is mine.", ""],
          ["**Haec** urbs magna est.", "This city (the one we're in) is large.", ""],
          ["**hōc** proeliō factō", "after this battle (the one just described) was fought", "A&G §296"]]},
  "uses": [
   {"name": "The latter", "sec": "297.a", "lvl": "core",
    "what": "When a writer names two people or things and then uses <i>hic</i> and <i>ille</i>, <i>hic</i> means <b>the latter</b>: the second one named, which is nearer in the sentence. <i>Ille</i> means <b>the former</b>, the first one named, further back.",
    "clue": "<i>Hic … ille</i> in the same sentence, after two things have been named.",
    "ex": [["Mārcus et Sextus vēnērunt; **hic** rīdet, ille flet.", "Marcus and Sextus came; the latter (Sextus) is laughing, the former (Marcus) is crying.", ""]]},
   {"name": "Haec: three forms", "sec": "146", "lvl": "core",
    "what": "<i>Haec</i> can be feminine nominative singular (this woman, this ___) or neuter nominative or accusative plural (these things). The verb and the noun it goes with decide: a singular verb or a feminine noun means one; a plural verb or a neuter noun means more than one.",
    "clue": "<i>Haec</i> with a plural verb is usually neuter plural: these things.",
    "ex": [["**Haec** est puella.", "This is the girl.", ""], ["**Haec** sunt vēra.", "These things are true.", ""]]},
   {"name": "Hīc, the adverb", "sec": "146", "lvl": "core",
    "what": "<i>Hīc</i> with a long <i>ī</i> is not the pronoun but the adverb here (an adverb tells you where, when or how). Without macrons the two look the same.",
    "clue": "<i>Hic</i> with no noun to agree with and a sense of place: here.",
    "ex": [["habitant **hīc** quaedam mulierēs pauperculae", "some poor women live here", "Ter. Ad. 647"]]},
  ]},

 {"id": "dem-ille", "name": "Ille, illa, illud", "q": "that (over there)", "prons": ["ille"], "secs": "146, 297.b",
  "summary": "<i>Ille, illa, illud</i> is the far demonstrative: it points to something away from the speaker. It's the English <i>that</i>: that mountain over there, those days long ago. "
             "As with <i>hic</i>, the distance can be in place, in time (<i>illō tempore</i>, at that time, back then), or in the conversation. Paired with <i>hic</i>, it means the former; after a name, it can mean that famous.",
  "extra": DIST("ille"),
  "pattern": "<b>Pattern:</b> masculine nominative singular in <i>-e</i>, neuter in <i>-d</i> (<i>ille, illud</i>), genitive <i>illīus</i> and dative <i>illī</i> in every gender. Everything else is like <i>bonus</i>: <i>illum, illam, illō; illī, illae, illa, illōrum</i>.",
  "basic": {"name": "That, over there", "sec": "297.b",
   "rule": "<i>Ille</i> points at what is away from the speaker. <b>With a noun</b>, as an adjective, it agrees with the noun and means that, those: <i>ille mōns</i>, that mountain. "
           "<b>On its own</b>, as a pronoun, it means that man, that woman, that thing, or often just he or she.",
   "how": "Read that or those. If no noun goes with it, let the gender tell you: <i>ille</i>, that man, he; <i>illa</i>, that woman, she; <i>illud</i>, that thing.",
   "ex": [["**Ille** mōns altus est.", "That mountain (over there) is high.", ""],
          ["**illō** tempore", "at that time, back then", ""],
          ["**Ille** vir fortis erat.", "That man was brave.", ""]]},
  "uses": [
   {"name": "The former", "sec": "297.b", "lvl": "core",
    "what": "Paired with <i>hic</i>, <i>ille</i> means <b>the former</b>: the first of two things named, which is further back in the sentence. <i>Hic</i> is <b>the latter</b>, the second one named.",
    "clue": "<i>Ille … hic</i> after two things have been named.",
    "ex": [["Mārcus et Sextus vēnērunt; hic rīdet, **ille** flet.", "Marcus and Sextus came; the latter (Sextus) is laughing, the former (Marcus) is crying.", ""]]},
   {"name": "That famous", "sec": "297.b", "lvl": "core",
    "what": "After a name, <i>ille</i> often means that well-known, that famous: the one everybody has heard of. English does this too: <i>that</i> Medea.",
    "clue": "A name + <i>ille</i>.",
    "ex": [["Mēdēa **illa**", "the famous Medea", ""]]},
   {"name": "Illud: the following", "sec": "297.b", "lvl": "adv",
    "what": "The neuter <i>illud</i> often points forward to something about to be quoted or explained, like English the following, this: …",
    "clue": "<i>Illud</i> followed by a colon, a quotation or an infinitive.",
    "ex": [["Est **illud** quidem vel maximum, animum vidēre.", "That is truly a very great thing, to see the soul.", "A&G §297.f"]]},
  ]},

 {"id": "dem-iste", "name": "Iste, ista, istud", "q": "that (of yours)", "prons": ["iste"], "secs": "146, 297.c",
  "summary": "<i>Iste, ista, istud</i> points to something near the person you're talking to: that thing of yours, that thing you've got there. "
             "English has no separate word for it. The closest is <em>that</em> said with a bit of stress, which is also why it so often sounds dismissive: think of What's <em>that</em> supposed to be? "
             "Cicero calls Verres, the governor he is prosecuting, <i>iste</i> all the way through his speeches against him: <em>that</em> man.",
  "extra": DIST("iste"),
  "pattern": "<b>Pattern:</b> declined exactly like <i>ille</i>: <i>iste, ista, istud</i>; genitive <i>istīus</i>, dative <i>istī</i> in every gender.",
  "basic": {"name": "That, near you", "sec": "297.c",
   "rule": "<i>Iste</i> points at something near the person spoken to, or belonging to them. <b>With a noun</b>, as an adjective: <i>iste liber</i>, that book (of yours). "
           "<b>On its own</b>, as a pronoun: that man, that woman, that thing.",
   "how": "Read <em>that</em>, and add of yours or that you've got if it helps. In a speech, try that man or that fellow, said with a sneer.",
   "ex": [["**iste** liber", "that book of yours", ""],
          ["**Istud** quod tenēs", "that thing you're holding", ""],
          ["Quid **iste** dīcit?", "What is <em>that</em> man saying?", ""]]},
  "uses": [
   {"name": "Scorn", "sec": "297.c", "lvl": "core",
    "what": "In speeches, <i>iste</i> often refers to an opponent with contempt: <em>that</em> man, that fellow. The speaker is pointing across the courtroom at someone on the other side.",
    "clue": "<i>Iste</i> in a speech in court, for the person on the other side.", "ex": []},
  ]},

 {"id": "dem-idem", "name": "Īdem, eadem, idem", "q": "the same", "prons": ["idem"], "secs": "146, 298",
  "summary": "<i>Īdem, eadem, idem</i> means the same. It is <i>is, ea, id</i> with <i>-dem</i> stuck on the end, so if you know <i>is</i> you already know most of <i>īdem</i>. "
             "Like <i>is</i>, it doesn't say near or far: it points back to someone or something already named and says <i>this is that very one again</i>.",
  "extra": DIST("idem"),
  "pattern": "<b>Pattern:</b> <i>is</i> + <i>-dem</i>, with two adjustments (§146): m becomes n before the d (<i>eundem, eandem, eōrundem, eārundem</i>), and the masculine nominative is <i>īdem</i> (not <i>isdem</i>), neuter <i>idem</i>. The plural <i>eīdem, eīsdem</i> is also spelled <i>iīdem, īsdem</i>.",
  "basic": {"name": "The same", "sec": "298",
   "rule": "<i>Īdem</i> says that something is the very one already mentioned. <b>With a noun</b>, as an adjective: <i>eōdem diē</i>, on the same day. "
           "<b>On its own</b>, as a pronoun: the same man, the same woman, the same thing.",
   "how": "Find the <i>-dem</i> on the end, then read the rest as a form of <i>is</i>: <i>eundem</i> is <i>eum</i> + <i>-dem</i>, the same man (accusative).",
   "ex": [["**eōdem** proeliō", "in the same battle", "A&G §296"],
          ["**eadem** puella", "the same girl", ""],
          ["**Idem** dīcō.", "I say the same thing.", ""]]},
  "uses": [
   {"name": "Also, yet", "sec": "298.b", "lvl": "core",
    "what": "<i>Īdem</i> can add a second, sometimes surprising quality to the same person or thing. English says and also, and at the same time.",
    "clue": "<i>Et īdem, et eadem</i> after a list of qualities.",
    "ex": [["ōrātiō splendida et grandis et **eadem** in prīmīs facēta", "a speech that was brilliant and grand, and also very witty", "A&G §298.b"]]},
  ]},
]
