# Merge the finished PDFs into all-in-one.pdf (guide, then weekly pages, then checklists).
import pypdfium2 as pdfium
out = pdfium.PdfDocument.new()
for f in ["complete-guide.pdf", "weekly-plans.pdf", "checklists.pdf"]:
    src = pdfium.PdfDocument(f)
    out.import_pages(src)
out.save("all-in-one.pdf")
print("all-in-one.pdf:", len(out), "pages")
