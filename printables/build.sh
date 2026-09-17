#!/bin/sh
# Rebuild all printable PDFs (needs python3 with 'markdown' and 'pypdfium2', and Chromium).
cd "$(dirname "$0")"
python3 build_guide.py
CHROME=${CHROME:-/opt/pw-browsers/chromium}
for f in weekly-plans checklists complete-guide; do
  "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf="$f.pdf" "file://$PWD/$f.html" 2>/dev/null
done
python3 merge.py
ls -la *.pdf
