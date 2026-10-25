# かんじの うみ (Kanji Sea)

A sea-creature kanji writing app for a Grade 1 learner, made for the iPad.
It covers the kanji in 光文書院 くりかえし かんじドリル 1年 上, in the book's order.

- **Practice:** watch the stroke order (みる), trace it (なぞる), then write it from memory (かく), with every stroke checked for shape, direction and order.
- **Host (タカアシガニ):** a Japanese spider crab walks sideways along the sand in the home-screen tank.
  It says hello when the app opens, or when she comes back after 20 minutes or more away, with how many reviews are waiting.
  When she comes back to the home screen after doing something good (a level up, a new sea friend, a perfect test, a new fossil, a good reading game) it hops and says what she did and よく できたね！; after other practice it says よく がんばったね！.
  Its words are read aloud when the sound is on, and tapping it gets a fact or a cheer.
  She can drag it up the tank (its legs dangle and it squeals わあっ！); let go and it falls back to the sand with a bounce and a puff of sand, then walks on.
  The octopus stays as the writing coach.
- **Reviews (ふくしゅう):** WaniKani-style spaced repetition, where every review is writing from memory and each level is a sea creature.
  A session goes through each kanji that is due once and then ends.
  A missed kanji is never asked again in the same session; its level is settled straight away instead.
  Writing it with no misses or hints levels it up.
  Small slips (missed strokes where no stroke was shown, or the picture hint) keep its level and restart its wait.
  Any stroke shown (after two misses on it, or one drawn backwards), ちょっと みる or わからない drops it a level (two from じょうず up).
  Each set's ▶ れんしゅう button gives free practice on that set instead, which picks low-level kanji most often and never changes levels.
  Half the prompts put the word in a short book-style sentence, with the reading over the box to write in.
- **Writing in sentences (ぶんで かく):** practice where every prompt is one of those sentences.
- **Writing readings (よみを かく):** the kanji sits in a sentence and you write its reading in hiragana, one kana at a time, each checked stroke by stroke.
- **Tests (🐳 テスト):** each set has a test that goes through its kanji once each, with no hints, inside a whale's mouth.
  Strokes stay as she wrote them rather than snapping to the model, but each still has to fit to count.
  Once a stroke fits, the model stroke appears in light grey underneath hers, so she can see where it should have gone.
  A kanji written with no misses grows a tooth on the whale's jaws, so the teeth are the score.
  Two misses on one stroke mark that kanji wrong and draw the rest of it in.
  A right answer on a kanji that is due for review counts as that review and levels it up; nothing else in a test changes levels.
  The best full-test score for each set shows on its button.
  A perfect test sets off a chicken dance by a line of sea animals, to an original polka (tap to skip).
- **Fossil dig (かせき):** after the chicken dance, a perfect test digs up that set's fossil of an ancient sea animal.
  The fossil is small and hidden at a random spot, so most of the slab is empty and she has to hunt for it.
  She rubs away loose sand and then harder rock with a fingertip-sized scraper, and once most of the fossil is uncovered the rest crumbles away and the fossil is named.
  Each set has its own fossil (しおだまり an アンモナイト, さんごしょう a サンヨウチュウ, くじらの うみ a クビナガリュウ, ふかい うみ a シーラカンス, こんぶの もり a ウミユリ), shown next to the set's manta: a ？ until it's dug up, then the fossil, which she can tap to see bigger with a line about it.
  Another perfect test on the same set digs up the same fossil again, just for fun.
  Seven more fossils are drawn and ready for sets added later.
- **Adventure (ぼうけん):** a Prince of Persia–style maze in a sunken temple, where she is the タカアシガニ and has to find the treasure chest holding the kanji for a word (「やま」の かんじは どれ？).
  Each maze fills one screen with four storeys of stone corridors, and the other two chests are in other rooms.
  To get there she climbs kelp up through the floors, drops through holes, jumps over spikes and clambers over steps.
  Four rounds, each in a different maze.
  It's about finding the way rather than quick fingers: ◀ ▶ walk, ▲ climbs kelp or jumps, ▼ climbs down, and the curved-arrow buttons above ◀ and ▶ call a sea turtle that carries her on its back up and about three cells left or right (over spikes, gaps and steps), so she never has to press two buttons at once.
  A step one block high is climbed just by walking into it, every room has a way back up, and spikes only send her back to where she last stood.
  A wrong chest greys out and shows the picture hint; the right one opens with a pearl, and finding it first time counts as a reading.
- **Practice squares:** after a mistake writing a kanji from memory (in a test, a review, practice or a lesson's かく), four squares open for optional free practice, as in the drill book.
  Trace the first two over a faint outline, then write it in the other two; the ink isn't checked.
- **Reading game (よめるかな？):** a stingray brings a kanji, and you find its reading in a fish tank and tap it.
  Each reading rides on a creature's back: a fish cruising or dashing about near the top, a turtle, sea snake or jellyfish in the middle, and on the sand a ワニ plodding along, a scuttling crab, a チンアナゴ popping in and out of its holes, or an octopus peeking out from behind a rock.

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
