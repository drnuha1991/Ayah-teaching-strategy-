# Arabic printables

- `all-in-one.pdf` — **everything in one file:** the guide, the 2-page rules sheet, the 12 reading pages, and the writing pages.
- `guide.pdf` — the guide only (overview, rules, method, 12-week plan, activity bank, tracker).
- `rules-sheet.pdf` — 2 pages to hang up: every reading rule with examples, sun/moon letters, hamza shapes, little words.
- `reading-pages.pdf` — 12 pages, one per week. Rows of vowelled words (later sentences and stories) with tick boxes, and a "copy these words" section at the bottom.
- `writing-pages.pdf` — letter-forms chart, 7 tracing pages (one per letter family), join-the-letters (2), split-the-word, madd hunt, sukoon, tanween triplets, shadda, sun/moon sort, endings, and 2 pages of ruled dictation paper (print more as needed).

The Arabic font is [Amiri](https://github.com/aliftype/amiri) (SIL Open Font License, in `fonts/`), a clear Naskh with well-placed tashkeel.

**To change words or add pages:** edit `content.py` (all words, stories and word lists) or `build_arabic.py` (layout), then run `./build.sh`.
It needs Python 3 with `markdown` and `pypdfium2`, and Chromium (set `CHROME=/path/to/chromium` if it isn't at the default path).
The `.html` files are the print sources; you can also open them in a browser and print from there.
