#!/bin/bash
# Render the worksheet HTML to print-ready A4 PDFs with headless Chrome.
# Chrome is used because it shapes Devanagari correctly (matras, conjuncts,
# nukta) - reportlab/fpdf do not without extra work.
set -e
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DIR="$(cd "$(dirname "$0")" && pwd)/bengali_to_hindi"
for f in "$DIR"/0*.html; do
  out="${f%.html}.pdf"
  "$CHROME" --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf="$out" --virtual-time-budget=20000 \
    "file://$f" 2>/dev/null
  echo "  $(basename "$out")  $(pdfinfo "$out" 2>/dev/null | awk '/^Pages/{print $2" pages"}')"
done
