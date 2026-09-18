#!/bin/sh
# إعادة بناء ملفات PDF العربية (يحتاج python3 مع markdown و pypdfium2، وكروميوم).
cd "$(dirname "$0")"
python3 build_arabic.py
CHROME=${CHROME:-/opt/pw-browsers/chromium}
for f in الدليل صفحات-القراءة صفحات-الكتابة ورقة-القواعد; do
  "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf="$f.pdf" "file://$PWD/$f.html" 2>/dev/null
done
python3 - <<'PY'
import pypdfium2 as pdfium
out = pdfium.PdfDocument.new()
for f in ["الدليل.pdf", "ورقة-القواعد.pdf", "صفحات-القراءة.pdf", "صفحات-الكتابة.pdf"]:
    out.import_pages(pdfium.PdfDocument(f))
out.save("الكل-في-ملف-واحد.pdf"); print("الكل-في-ملف-واحد.pdf:", len(out), "صفحة")
PY
ls -la *.pdf
