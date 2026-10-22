"""Fetch KanjiVG stroke paths for the app's kanji and the kana in its sentence readings into data/strokes.json.

Run after adding kanji to SECTIONS or sentences to SENT in app.html. SVGs are cached in data/kanjivg/.
"""
import json
import re
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parent.parent
html = (root / "app.html").read_text(encoding="utf-8")
kanji = set("".join(re.findall(r"kanji:'([^']+)'", html)))
kana = set("".join(re.findall(r"\[([ぁ-ゖ]+)\]", html)))

cache = root / "data" / "kanjivg"
out = {}
for ch in sorted(kanji | kana):
    f = cache / f"{ord(ch):05x}.svg"
    if not f.exists():
        url = f"https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji/{f.name}"
        f.write_bytes(urllib.request.urlopen(url, timeout=30).read())
    svg = f.read_text(encoding="utf-8")
    # Stroke paths carry ids like kvg:06728-s1, in stroke order.
    strokes = sorted(((int(n), d) for n, d in re.findall(r'id="kvg:[0-9a-f]+-s(\d+)"[^>]*\sd="([^"]+)"', svg)))
    out[ch] = [d for _, d in strokes]
    assert out[ch], ch
(root / "data" / "strokes.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"{len(kanji)} kanji, {len(kana)} kana: {''.join(sorted(kana))}")
