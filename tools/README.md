# Page builders

These scripts generate some of the grammar pages and flashcard data. Run them from this folder, with the repo root as the site folder. Each one overwrites the pages it builds, so edit the content files here rather than the generated HTML, or your edits will be lost the next time the script runs.

## Pronoun pages and deck

- `python3 make_pronouns.py ..` rebuilds `data/decks/pronouns.json` and writes the deck-view entries to `pron_index.json` (copy them into `data/decks/index.json` by hand).
- `python3 make_pronoun_page.py ..` rebuilds the `grammar/pronouns-*.html` pages from the deck, `pronoun_content.py` (with `pronoun_content_dem.py` and `pronoun_content_indef.py`) and `pronoun_page_template.html`. It writes the sidebar entries to `pron_grammar_entries.json`.

## Indicative verb pages

- `python3 restructure_verbs2.py verb-sources ..` rebuilds the seven indicative tense pages and `complete-passive.html`.
- The charts, pattern buttons and inspector notes come from the pages in `verb-sources/`. The descriptions, uses and the time-and-aspect grid come from `verb_content.py`. The "How to build it" figures, the 3rd principal part section and the shared CSS block come from `verb_build.py`.
- After changing the CSS in `verb_build.py`, copy it into the end of `css/grammar-verbs.css` (everything from `/* how a form breaks down` on) and bump the `?v=` stamp.

## Subjunctive pages

- `python3 make_subj.py ..` rebuilds the four subjunctive tense pages, `subjunctive.html` and `subjunctive-uses.html`. The overview and uses pages are in `subj_pages.py`, and they borrow the page styles from `grammar/verbs.html`.

## Hand-written pages

The noun pages, `nouns.html`, `pronouns.html`, `verbs.html` and `incomplete-system.html` are not generated. Edit them directly.
