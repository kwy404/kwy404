#!/usr/bin/env bash
# Builds the portfolio into ../docs (GitHub Pages, main branch, /docs folder).
set -euo pipefail
cd "$(dirname "$0")"
BUN="${BUN:-/root/.bun/bin/bun}"
rm -rf ../docs/assets/js
"$BUN" build src/main.js --splitting --minify --sourcemap=linked --target=browser --format=esm \
  --outdir ../docs/assets/js --entry-naming '[name]-[hash].[ext]' --chunk-naming '[name]-[hash].[ext]' \
  --banner '/*! kwy404 portfolio · built with Voodoo.js + Monsoon + glyphfox · github.com/kwy404 */'
for f in ../docs/assets/js/*.js; do node --check "$f"; done
python3 gen_site.py
