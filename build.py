"""Build Kanji Sea from app.html.

dist/kanji-sea.html  - page for the claude.ai artifact (the artifact host adds <head>)
dist/web/            - standalone site for any static host; add to the iPad home screen from Safari
"""
import shutil
from pathlib import Path

root = Path(__file__).parent
html = (root / "app.html").read_text(encoding="utf-8")
strokes = (root / "data" / "strokes.json").read_text(encoding="utf-8")
page = html.replace("/*__STROKES__*/null", strokes)

dist = root / "dist"
dist.mkdir(exist_ok=True)
(dist / "kanji-sea.html").write_text(page, encoding="utf-8")

HEAD = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="かんじの うみ">
<meta name="theme-color" content="#17607e">
<link rel="apple-touch-icon" href="icon-180.png">
<link rel="icon" href="icon-512.png">
<link rel="manifest" href="manifest.webmanifest">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}[hidden]{display:none!important}</style>
</head>
<body>
"""
MANIFEST = """{"name":"かんじの うみ","short_name":"かんじの うみ","start_url":".","display":"standalone",
"background_color":"#06192a","theme_color":"#17607e",
"icons":[{"src":"icon-180.png","sizes":"180x180","type":"image/png"},{"src":"icon-512.png","sizes":"512x512","type":"image/png"}]}
"""
web = dist / "web"
web.mkdir(exist_ok=True)
(web / "index.html").write_text(HEAD + page + "\n</body>\n</html>\n", encoding="utf-8")
(web / "manifest.webmanifest").write_text(MANIFEST, encoding="utf-8")
for name in ("icon-180.png", "icon-512.png"):
    shutil.copy(root / "assets" / name, web / name)
