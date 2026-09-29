# Latin Site

Interactive grammar, flashcards and games for a three-year high-school Latin course.
Hosted with GitHub Pages. There's no build step: edit a file, push, and the site updates.

## Layout

```
index.html              site home
css/site.css            shared theme (style guide v1): every page links this
css/flashcards.css      flashcard player styles
js/common.js            shared helpers (shuffle, safe storage, loading data)
js/flashcards.js        the flashcard engine, used by every deck
flashcards/index.html   deck list + player  →  flashcards/?deck=latin2-vocab
data/decks/*.json       one file per deck (content only, no code)
data/decks/index.json   the deck list shown on the flashcards page
```

**Changing the look** → `css/site.css`. **Adding a feature to all flashcards** → `js/flashcards.js`.
**Adding or fixing vocabulary** → the deck's JSON file.

## Adding a deck

1. Copy an existing file in `data/decks/` (e.g. `latin2-vocab.json`) and rename it. The file name is the deck id.
2. Change `id`, `title`, `subtitle`, and replace `cards`.
3. Add a line for it to `data/decks/index.json`.

### Deck format

```jsonc
{
  "id": "latin2-vocab",
  "title": "Latin II Vocabulary",
  "course": "Latin II",                 // groups decks on the list page
  "subtitle": "Core vocabulary by week",
  "filters": [                          // each becomes a row of toggle buttons
    { "field": "w", "label": "Week",
      "values": [ { "v": 1, "label": "Week 1" } ] },
    { "field": "p", "label": "Words",
      "values": [ { "v": "verb", "label": "Verbs", "short": "verb" } ] }
  ],
  "modes": ["le", "el", "pp"],          // Latin→English (default: the first one), English→Latin, Principal parts
  "meta": { "front": ["{w}", "{p}"],    // small corner labels; {field} is filled in
            "back":  ["{w}", "{p}"] },
  "lookalikes": false,                  // true = warn when two cards share a Latin form
  "cards": [
    { "w": 1, "p": "verb", "la": "dō, dare", "en": "to give", "pp": "dō, dare, dedī, datum" }
  ]
}
```

Card fields: `la` (Latin), `en` (English), and optionally `pp` (principal parts, enables that mode for the card)
and `parse` (a parse label such as “1st sg., pres., ind., act”). Any filter field (`w`, `p`, `mood`…) must be on every card.

### Verb-form decks

Paradigm decks (e.g. `perfect-active.json`) use the same two modes as every deck, `"le"` (Latin → English, the default) and `"el"` (English → Latin), plus a few extra card fields:

| Field | Meaning |
|---|---|
| `stem`, `end` | the form split so the ending is highlighted (`la` is the whole form) |
| `pn`, `tl` | person/number (“1st Person Singular”) and tense label (“perfect active indicative”) |
| `tag` | verb shown at the top of the card |
| `detail`, `note` | an extra line (e.g. “ending: -ī · perfect stem: amāv-”) and a warning (look-alike forms) |
| `pi`, `lemma`, `gloss`, `tnote` | person index 0–5 and the verb's details, used to build the paradigm tables |

Deck-level `intro` (HTML grammar note), `paradigmNote`, and
`paradigm: {"table": "conj", "group": "t", "headings": {...}}` turn on the grammar note and the “Show paradigms” tables.

### Noun decks

The noun deck (`noun-declensions.json`) reuse the same card fields: `pn` holds the case (“Genitive Singular”), and `pi` runs 0–4 for the singular cases and 5–9 for the plural. Two deck-level settings adapt the engine:

- `"allReadings": "noun"`: in Latin → English mode, the answer lists every card of the same noun with that spelling (equī = genitive singular *and* nominative plural).
- `"paradigm": {"table": "noun", "rows": ["Nominative", …], "rowLabel": "Case", "tableSuffix": ""}` builds one case table per noun.

### Adjective deck

`adjective-degrees.json` works like the noun deck, with `"allReadings": "deg"` so every reading of a form within its degree is listed (clārius = neuter comparative adjective *and* comparative adverb). A card that lacks a filter's field ignores that filter, so the adverb cards (no gender or number) stay in when you filter by gender. `"cue"` sets the prompt shown under the Latin.

### Participles and irregular verbs

`participles.json` works like the adjective deck (`"allReadings": "part"`); only amō has full paradigms, so the other verbs' cards have no `pi` and stay out of the tables. `irregular-verbs.json` groups its tables by a `tm` (mood + tense) field that has no filter of its own: when a paradigm `group` has no matching filter, the groups come from the cards in order, titled by `headings`. A paradigm can also vary its rows, columns and row heading per group with `rowsBy`, `colsBy` and `rowLabelBy` (see `imperatives-infinitives.json`, whose imperative tables are Voice × Number and whose infinitive tables are Tense × Voice).

### Views: one deck, several entries on the deck list

A deck can define named slices in `"views"`, each shown as its own entry on the deck list:

```jsonc
"views": {
  "perf": { "title": "Perfect Passive Participle", "subtitle": "…",
            "sel": { "part": ["perf"] },      // filters this view fixes (their rows are hidden)
            "groups": ["perf"],               // optional: which paradigm sections to show
            "paradigmNote": "…" }             // optional: replaces the deck's note above the tables (HTML)
}
```

In `index.json`, point an entry at the view with `"view": "perf"` (link: `flashcards/?deck=participles&view=perf`). A view also hides any filter row none of its cards use (adverbs have no gender) and any chip that would match nothing. The participles, imperatives & infinitives, and adjectives & adverbs decks use views; each also keeps a "mixed review" entry for the whole deck.

### Linking to part of a deck

Any filter can be preset in the link, which is handy for assigning one piece of a bigger deck:

- `flashcards/?deck=noun-declensions&decl=3`: third declension only
- `flashcards/?deck=noun-declensions&decl=1,2&mode=el`: 1st and 2nd, starting in English → Latin
- `flashcards/?deck=complete-passive&t=plup`: pluperfect passive only
- `flashcards/?deck=adjective-degrees&deg=comp,sup`: comparatives and superlatives only
- `flashcards/?deck=irregular-verbs&verb=volo,nolo,malo&mood=ind`: volō, nōlō and mālō in the indicative
- `flashcards/?deck=imperatives-infinitives&form=inf-pres`: present infinitives only (also `imp`, `inf-perf`, `inf-fut`; combine with commas)

Presets apply to that visit and aren't saved over a student's own settings.

## Spaced repetition (Review mode)

Every deck has **Study: Practice / Review**. Practice is the free run-through (Got it / Still learning) and never touches the schedule. Review is Anki-style spaced repetition, in `js/srs.js`:

- A session is: cards still being learned, then due cards (shuffled), then up to **15 new cards per deck per day** (`NEW_PER_DAY`).
- After flipping, the student grades **Again / Hard / Good / Easy**; each button shows when the card will come back. Again (and Hard on a new card) brings it back a few cards later in the same session.
- Scheduling is SM-2 as in Anki: new cards graduate to 1 day (Good) or 4 days (Easy); after that the interval grows by the card's ease (starting at 2.5; Again −0.20, Hard −0.15, Easy +0.15, never below 1.3). A lapse resets the card to relearning. Intervals are capped at a year, and the day rolls over at 4 a.m.
- Each card has one history, whichever direction it's studied in (Latin → English, English → Latin, principal parts), and views and filters share it too.
- Card identity is the Latin form + parse (`la`, `pn`, `tl`, `parse`), so fixing an English gloss keeps a student's progress. Changing a Latin form or a parse label starts that card fresh; give the card an explicit `"id"` if you need to change those without resetting it.
- Everything is stored in the browser (`localStorage` key `latin:srs`). The deck list shows due counts and a **Your progress** panel to download a progress file, load one on another device (merging, newest review wins), or reset.

## Layout

On screens 980px and wider the player uses two columns: a sticky sidebar (Settings, Grammar note) beside the card. Settings, the grammar note, "Show paradigms", the progress panel and each group on the deck list are collapsible, and each remembers whether it was left open (separately for wide and narrow screens). Collapsed, Settings shows a one-line summary of the current choices. On phones, Settings and the grammar note start collapsed so the card is on screen straight away.

## Previewing on your computer

The pages load their data with `fetch`, so opening the file straight from Finder won't work. From the repo folder run:

```
python3 -m http.server
```

Then open <http://localhost:8000>.

## Publishing

Repo → Settings → Pages → Source: *Deploy from a branch*, branch `main`, folder `/ (root)`.
The site appears at `https://<username>.github.io/<repo-name>/` within a minute or two of each push.
