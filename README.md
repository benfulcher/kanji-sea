# かんじの うみ (Kanji Sea)

A sea-creature kanji writing app for a Grade 1 learner, made for the iPad.
It covers the kanji in 光文書院 くりかえし かんじドリル 1年 上, in the book's order.

- **Practice:** watch the stroke order (みる), trace it (なぞる), then write it from memory (かく), with every stroke checked for shape, direction and order.
- **Reviews (ふくしゅう):** WaniKani-style spaced repetition, where every review is writing from memory and each level is a sea creature.
  A session goes through every kanji that is due, brings misses back later in the session, and ends once each one has been written with no misses or hints.
  Each set's ▶ れんしゅう button gives free practice on that set instead, which picks low-level kanji most often and never changes levels.
  Half the prompts put the word in a short book-style sentence, with the reading over the box to write in.
- **Writing in sentences (ぶんで かく):** practice where every prompt is one of those sentences.
- **Writing readings (よみを かく):** the kanji sits in a sentence and you write its reading in hiragana, one kana at a time, each checked stroke by stroke.
- **Tests (🐳 テスト):** each set has a test that goes through its kanji once each, with no hints, inside a whale's mouth.
  A kanji written with no misses grows a tooth on the whale's jaws, so the teeth are the score.
  Two misses on one stroke mark that kanji wrong and draw the rest of it in.
  A right answer on a kanji that is due for review counts as that review and levels it up; nothing else in a test changes levels.
  The best full-test score for each set shows on its button.
- **Reading game (よめるかな？):** a stingray brings a kanji and you pick its reading.

## Build

After adding kanji to `SECTIONS` or sentences to `SENT` in `app.html`, run `python3 tools/strokes.py` to fetch their KanjiVG strokes (kanji, plus the kana in sentence readings) into `data/strokes.json`.

`python3 build.py` inlines the stroke data into `app.html` and writes:

- `dist/web/`: the standalone site, deployed to GitHub Pages by `.github/workflows/pages.yml` on every push to `main`.
- `dist/kanji-sea.html`: the version published as a claude.ai artifact.

Open the Pages site in Safari on the iPad and choose Share → Add to Home Screen.
Progress is saved in the browser on that device.
To guard against a wipe, the バックアップ button at the bottom of the home screen saves it as a small `.json` file (on the iPad: Share → Save to Files, e.g. into iCloud Drive), and もどす loads one back.
A reminder appears on the home screen when the last backup is more than 30 days old.

## Credits

Stroke-order data comes from [KanjiVG](https://kanjivg.tagaini.net) by Ulrich Apel, licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
The files in `data/kanjivg/` are unmodified, and `data/strokes.json` is derived from them under the same licence.
