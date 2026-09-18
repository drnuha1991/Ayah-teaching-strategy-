#!/bin/sh
# Rebuild the Arabic printable PDFs (needs python3 with 'markdown' and 'pypdfium2', and Chromium).
cd "$(dirname "$0")"
python3 build_arabic.py
CHROME=${CHROME:-/opt/pw-browsers/chromium}
for f in guide reading-pages writing-pages rules-sheet; do
  "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf="$f.pdf" "file://$PWD/$f.html" 2>/dev/null
done
python3 - <<'PY'
import pypdfium2 as pdfium
out = pdfium.PdfDocument.new()
for f in ["guide.pdf", "rules-sheet.pdf", "reading-pages.pdf", "writing-pages.pdf"]:
    out.import_pages(pdfium.PdfDocument(f))
out.save("all-in-one.pdf"); print("all-in-one.pdf:", len(out), "pages")
PY
ls -la *.pdf
