#!/bin/bash
set -e
uv sync
uv run myst build --html --ci

ADSENSE_PUB_ID="ca-pub-6919567340515109"

# Inject Google AdSense script into the <head> of all built HTML files
ADSENSE_SCRIPT="<script async src=\"https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${ADSENSE_PUB_ID}\" crossorigin=\"anonymous\"></script>"

for html_file in $(find _build/html -name "*.html" -type f); do
  sed -i "s|</head>|${ADSENSE_SCRIPT}</head>|" "$html_file"
done

# Copy static files (ads.txt, etc.) to build output
cp ads.txt _build/html/ads.txt
