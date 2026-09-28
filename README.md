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
  "modes": ["le", "el", "pp"],          // Latin→English, English→Latin, Principal parts
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

Paradigm decks (e.g. `perfect-active.json`) use modes `"pf"` (Parse → Form) and `"fp"` (Form → Parse) and a few extra card fields:

| Field | Meaning |
|---|---|
| `stem`, `end` | the form split so the ending is highlighted (`la` is the whole form) |
| `pn`, `tl` | person/number (“1st Person Singular”) and tense label (“perfect active indicative”) |
| `tag` | verb shown at the top of the card |
| `detail`, `note` | an extra line (e.g. “ending: -ī · perfect stem: amāv-”) and a warning (look-alike forms) |
| `pi`, `lemma`, `gloss`, `tnote` | person index 0–5 and the verb's details, used to build the paradigm tables |

Deck-level `intro` (HTML grammar note), `paradigmNote`, and
`paradigm: {"table": "conj", "group": "t", "headings": {...}}` turn on the grammar note and the “Show paradigms” tables.

## Previewing on your computer

The pages load their data with `fetch`, so opening the file straight from Finder won't work. From the repo folder run:

```
python3 -m http.server
```

Then open <http://localhost:8000>.

## Publishing

Repo → Settings → Pages → Source: *Deploy from a branch*, branch `main`, folder `/ (root)`.
The site appears at `https://<username>.github.io/<repo-name>/` within a minute or two of each push.
