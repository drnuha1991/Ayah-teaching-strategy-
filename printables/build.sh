#!/bin/sh
# Rebuild the printable PDFs from build.py (needs python3 and Chromium).
cd "$(dirname "$0")"
python3 build.py
CHROME=${CHROME:-/opt/pw-browsers/chromium}
for f in weekly-plans checklists; do
  "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf="$f.pdf" "file://$PWD/$f.html" 2>/dev/null
done
ls -la *.pdf
