# Builds complete-guide.html (all guide chapters) and all-in-one.html (guide + weekly pages + checklists).
import markdown, re, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import build  # regenerates weekly-plans.html / checklists.html and exposes page builders

ROOT = pathlib.Path(__file__).resolve().parent.parent
CHAPTERS = ["README.md","01-resources-and-recommendations.md","02-how-to-teach.md","03-three-month-plan.md","04-activity-bank.md","05-progress-tracker.md"]

GUIDE_CSS = """
@page { size: Letter portrait; margin: 0.6in 0.65in; }
body { font-family: "DejaVu Sans", Arial, Helvetica, sans-serif; color:#222; font-size: 10pt; line-height: 1.38; margin:0; }
.chapter { page-break-before: always; }
.chapter:first-of-type { page-break-before: auto; }
.cover { height: 9.4in; display:flex; flex-direction:column; justify-content:center; text-align:center; page-break-after: always; }
.cover h1 { font-size: 34pt; margin: 0 0 10px; }
.cover p { font-size: 13pt; color:#555; margin: 4px 0; }
.cover .toc { margin-top: 40px; text-align:left; display:inline-block; font-size: 11.5pt; line-height: 1.9; }
h1 { font-size: 20pt; border-bottom: 3px solid #222; padding-bottom: 4px; margin: 0 0 10px; }
h2 { font-size: 14pt; margin: 16px 0 6px; border-bottom: 1px solid #bbb; padding-bottom: 2px; page-break-after: avoid; }
h3 { font-size: 11.5pt; margin: 12px 0 4px; page-break-after: avoid; }
p { margin: 4px 0 6px; }
ul, ol { margin: 2px 0 6px; padding-left: 18px; }
li { margin-bottom: 2px; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 10px; font-size: 9pt; page-break-inside: auto; }
th, td { border: 1px solid #999; padding: 4px 6px; vertical-align: top; text-align: left; }
th { background: #eee; }
tr { page-break-inside: avoid; }
code { font-family: "DejaVu Sans Mono", monospace; font-size: 8.5pt; background:#f2f2f2; padding: 0 3px; }
hr { border: 0; border-top: 1px solid #ccc; margin: 12px 0; }
a { color: #222; text-decoration: none; }
strong { font-weight: bold; }
"""

def md_to_html(path):
    text = pathlib.Path(path).read_text()
    # links to other chapters / printables become plain text in print
    text = re.sub(r'\[([^\]]+)\]\((?:\d\d-[^)]+\.md|README\.md|printables/[^)]+)\)', r'\1', text)
    return markdown.markdown(text, extensions=["tables","sane_lists"])

cover = """<div class="cover">
  <h1>Teaching Ayah at Home</h1>
  <p>Pre-K guide, age 4 · reading, writing, and math in under an hour a day</p>
  <p>12-week plan following the <i>ABC See, Hear, Do</i> letter groups</p>
  <div class="toc">
    1. Overview and golden rules<br>
    2. Resources and recommendations<br>
    3. How to teach: reading, writing, math<br>
    4. The 3-month plan (12 weeks)<br>
    5. Activity bank (67 games)<br>
    6. Progress tracker and "if she's stuck"<br>
    <span style="color:#777">Then: weekly pages to hang up, and checklists</span>
  </div>
</div>"""

chapters = "".join(f'<div class="chapter">{md_to_html(ROOT/c)}</div>' for c in CHAPTERS)
guide_body = cover + chapters
html = lambda body, css, title: f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{css}</style></head><body>{body}</body></html>"
pathlib.Path("complete-guide.html").write_text(html(guide_body, GUIDE_CSS, "Ayah complete guide"))

print("guide html written")
