# Latin Site

Interactive grammar, flashcards and games for a three-year high-school Latin course.
Hosted with GitHub Pages. There's no build step: edit a file, push, and the site updates.

## Layout

The pages have no site menu of their own: the Google Site is the menu, linking to (or embedding) each flashcard deck, grammar page and game. The lists at `flashcards/`, `grammar/` and `games/` are there for finding a page's address.

```
index.html              site home
css/site.css            shared theme (style guide v1): every page links this
css/flashcards.css      flashcard player styles (also the games list)
css/grammar.css         shared look of the grammar pages (grammar-verbs.css adds the verb parts)
js/common.js            shared helpers (shuffle, safe storage, loading data)
js/pagelist.js          the grouped list on the games and grammar pages
js/flashcards.js        the flashcard engine, used by every deck
flashcards/index.html   deck list + player  →  flashcards/?deck=latin2-vocab
data/decks/*.json       one file per deck (content only, no code)
data/decks/index.json   the deck list shown on the flashcards page
grammar/index.html      grammar list  →  reads data/grammar.json
grammar/*.html          one interactive grammar page each
games/index.html        games list  →  reads data/games.json
games/*.html            one self-contained page per game
games/img/              images the games use
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

### Vocabulary lists: DCC Latin Core (Latin IV)

`dcc-core.json` is the [DCC Latin Core Vocabulary](https://dcc.dickinson.edu/vocab/core-vocabulary) (Dickinson College Commentaries), the thousand most common Latin words, as cards in frequency order. Each card has its `rank`, a `band` (1 = words 1–50, 2 = 51–100, … 20 = 951–1000) and a part of speech `p`; `id` is fixed (`r1`, `r2`, …) so progress survives edits to the wording. Spaced repetition introduces new cards in deck order, so students meet the most frequent words first. Link a band with `flashcards/?deck=dcc-core&band=3` (words 101–150). A deck's `introTitle` renames the "Grammar note" panel (here "About this list").

The word list is licensed **CC BY-SA 3.0**: keep the attribution in the deck's intro, and any changed version of `dcc-core.json` stays under the same licence. The source has a few quirks, fixed in the file: rank 12 is missing, rank 280 is shared by quisquam and vērō (`r280`, `r280b`), fore (985) had no definition, and vōs was tagged as an adjective.

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
- `flashcards/?deck=dcc-core&band=1,2&mode=el`: the 100 most common words, English → Latin
- `flashcards/?deck=imperatives-infinitives&form=inf-pres`: present infinitives only (also `imp`, `inf-perf`, `inf-fut`; combine with commas)

Presets apply to that visit and aren't saved over a student's own settings.

## Grammar

Interactive charts in `grammar/`: hover or tap any form to see what it is, how to translate it, and what it could be mistaken for; pattern buttons light up the rules.

| Page | Covers |
|---|---|
| `first-second-declension.html` | puella, equus, forum (and -er nouns) |
| `third-declension.html` | rēx, corpus, i-stems, how the nominative is formed |
| `fourth-declension.html` | frūctus, cornū, exceptions |
| `fifth-declension.html` | rēs, diēs |
| `declensions-overview.html` | all five side by side: cross-declension rules and look-alike endings |
| `case-usages.html` | each case's basic and further uses, with A&G references (link to a tab: `case-usages.html#ablative`) |
| `present-active.html` | present active indicative, all conjugations and sum |
| `imperfect-active.html` | imperfect active indicative, all conjugations and sum |

Each page holds its own content and script (the forms, notes and patterns are in the `<script>` at the bottom). The look is shared: `css/grammar.css` for every page and `css/grammar-verbs.css` for verb pages, so a change there changes them all. A page's own `<style>` only has its pattern colours (`--p-…`), `--card-h` (the height of the detail card, where a page needs a different one) and anything only that page uses.

**Adding a page:** copy the nearest existing page (e.g. `imperfect-active.html` for another tense), change its content and script, and add it to `data/grammar.json` (`page`, `title`, `group`, `about`).

## Games

Each game is one self-contained page in `games/` with its own look (style, data and code all in the file), so a game can be edited or replaced without touching anything else. They came from the Google Sites embeds; the only changes were a full page wrapper and pictures moved out of the code into `games/img/`. The Arena's start screen was also fixed on phones (its heading and button were cut off).

| Page | Game | From the Google Site |
|---|---|---|
| `first-letters.html` | First Letters (Latin I) | games/restoring-the-archive-latin-i |
| `restore-the-archive.html` | Restore the Archive | games/restoring-the-archive |
| `arena-latin-2.html` | Arena Formarum, Latin II form sheet | latin-ii/practice-games/gladiator-2 |
| `arena-latin-3.html` | Arena Formarum, Latin III/IV form sheet | latin-iii/practice-games/gladiator-game |
| `haruspex.html` | The Haruspex's Liver (uses of the subjunctive) | latin-iii/practice-games/haruspex-game |

**Adding a game:** save it as `games/<name>.html` and add an entry to `data/games.json` (`page`, `title`, `group`, `about`); the list groups games by `group` in file order.

**Arena score reports are switched off.** The Google Sites version had a "Send my score" button (name and period, then email or a Google Form post). It's been removed until there's a safe way to collect scores: the end screen still shows the result, and nothing leaves the student's browser. The original code is still on the Google Site if it's needed as a starting point.

## Readability

Every page, games included, follows the same rules:

- **Font:** Source Sans 3 (sans-serif, loaded from Google Fonts), set once as `--font` in `css/site.css` and `css/grammar.css`. The games keep their own colours but use the same font.
- **Size:** every font size is in `rem`, so text scales with the browser's text-size setting, and nothing is smaller than `1rem` (16px). Body text is `1.125rem` (18px).
- **Contrast:** text is at least 4.5:1 against its background (3:1 for large text); the site's body text and the grammar pattern colours are 7:1 or better, in light and dark mode. Colours live in the theme tokens (`--ink`, `--muted`, `--accent`, …) at the top of `css/site.css` and `css/grammar.css`, and each grammar page's `--p-…` pattern colours.
- **Spacing:** line height is at least 1.5, and paragraphs of reading text are 2 × the font size apart.

When adding a page or a colour, keep to these: a new colour for text needs 4.5:1 against every background it sits on (7:1 to match the rest of the site).

## Spaced repetition

Decks open in **Standard** mode, the free run-through (Got it / Still learning), which never touches the schedule. Spaced repetition is opt-in: Settings → Study: Standard / Spaced repetition (a student's choice is remembered per deck; in links and code, Standard is `study=practice` and spaced repetition is `study=review`). The scheduler is Anki-style, in `js/srs.js`:

- **In a deck:** a session is cards still being learned, then that deck's due cards (shuffled), then up to **15 new cards per deck per day** (`NEW_PER_DAY`). This is where new cards are learned.
- **Across all decks:** the button at the top of the deck list (`flashcards/?review=all`) gathers every card due today from every deck the student has studied into one session. It doesn't introduce new cards, and each card keeps its own deck's formatting (readings, parse, notes).
- After flipping, the student grades **Again / Hard / Good / Easy**; each button shows when the card will come back. Again (and Hard on a new card) brings it back a few cards later in the same session.
- Scheduling is SM-2 as in Anki: new cards graduate to 1 day (Good) or 4 days (Easy); after that the interval grows by the card's ease (starting at 2.5; Again −0.20, Hard −0.15, Easy +0.15, never below 1.3). A lapse resets the card to relearning. Intervals are capped at a year, and the day rolls over at 4 a.m.
- Each card has one history, whichever direction it's studied in (Latin → English, English → Latin, principal parts), and views and filters share it too.
- Card identity is the Latin form + parse (`la`, `pn`, `tl`, `parse`), so fixing an English gloss keeps a student's progress. Changing a Latin form or a parse label starts that card fresh; give the card an explicit `"id"` if you need to change those without resetting it.
- Everything is stored in the browser (`localStorage` key `latin:srs`). The deck list shows due counts per deck and a **Your progress** panel to download a progress file, load one on another device (merging, newest review wins), or reset.

## Search

- **Deck list:** the search box narrows the decks by name and, below, lists matching cards from every deck, grouped by deck, best matches first. "Study these cards" opens that deck in Standard mode with the search applied (`flashcards/?deck=dcc-core&q=war&study=practice`), ignoring the student's saved filters for that visit.
- **In a deck:** Settings → Search narrows the open deck, on top of the other settings. The search isn't saved.
- Matching ignores macrons and capitals (`fero` finds ferō), and each word typed must start a word on the card (Latin, English, principal parts or parse), so `war` finds war and warfare but not toward. Esc clears the box.

## Screen layout

On screens 980px and wider the player uses two columns: a sticky sidebar (Settings, Grammar note) beside the card. Settings, the grammar note, "Show paradigms", the progress panel and each group on the deck list are collapsible, and each remembers whether it was left open (separately for wide and narrow screens). Collapsed, Settings shows a one-line summary of the current choices. On phones, Settings and the grammar note start collapsed so the card is on screen straight away.

## Updating CSS or JavaScript: bump the version

Browsers keep copies of `css/` and `js/` files, so after an update students can keep running the old code for a while. The pages link these files with a version stamp (`flashcards.js?v=202609301530`). **Whenever a CSS or JS file changes, change that number** in `flashcards/index.html` (and `index.html` for `site.css`) so every browser fetches the new copy; any new number works, a date-time is easiest. Deck data (`data/decks/*.json`) is always fetched fresh and doesn't need this.

## Previewing on your computer

The pages load their data with `fetch`, so opening the file straight from Finder won't work. From the repo folder run:

```
python3 -m http.server
```

Then open <http://localhost:8000>.

## Publishing

Repo → Settings → Pages → Source: *Deploy from a branch*, branch `main`, folder `/ (root)`.
The site appears at `https://<username>.github.io/<repo-name>/` within a minute or two of each push.
