#!/bin/bash
# Render worksheet HTML to print-ready A4 PDFs with headless Chrome.
# Chrome is used because it shapes Devanagari correctly (matras, conjuncts,
# nukta); reportlab and fpdf do not without a lot of extra work.
# Usage: ./build_pdfs.sh [pair ...]      (default: every pair directory)
set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ROOT="$(cd "$(dirname "$0")" && pwd)"
PAIRS=("$@")
if [ ${#PAIRS[@]} -eq 0 ]; then
  PAIRS=()
  for d in "$ROOT"/*_to_*/; do PAIRS+=("$(basename "$d")"); done
fi
for pair in "${PAIRS[@]}"; do
  echo "$pair:"
  for f in "$ROOT/$pair"/0*.html; do
    out="${f%.html}.pdf"
    "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
      --print-to-pdf="$out" --virtual-time-budget=20000 "file://$f" 2>/dev/null
    echo "  $(basename "$out")  $(pdfinfo "$out" 2>/dev/null | awk '/^Pages/{print $2" pages"}')"
  done
done
