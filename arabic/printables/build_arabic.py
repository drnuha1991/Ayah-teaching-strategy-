# -*- coding: utf-8 -*-
# Generates reading-pages.html, writing-pages.html, rules-sheet.html and guide.html.
# Convert to PDF with Chromium headless (see build.sh). Content lives in content.py.
import html as H, pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import content as C
try:
    import markdown
except ImportError:
    markdown = None

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

FONT_CSS = """
@font-face { font-family: "Amiri"; src: url("fonts/Amiri-Regular.ttf"); font-weight: normal; }
@font-face { font-family: "Amiri"; src: url("fonts/Amiri-Bold.ttf"); font-weight: bold; }
@font-face { font-family: "AmiriAR"; src: url("fonts/Amiri-Regular.ttf"); font-weight: normal; size-adjust: 118%;
  unicode-range: U+0600-06FF, U+0750-077F, U+08A0-08FF, U+FB50-FDFF, U+FE70-FEFF, U+200C-200F; }
@font-face { font-family: "AmiriAR"; src: url("fonts/Amiri-Bold.ttf"); font-weight: bold; size-adjust: 118%;
  unicode-range: U+0600-06FF, U+0750-077F, U+08A0-08FF, U+FB50-FDFF, U+FE70-FEFF, U+200C-200F; }
"""

PAGE_CSS = FONT_CSS + """
@page { size: Letter portrait; margin: 0.45in 0.5in; }
* { box-sizing: border-box; }
body { margin: 0; color: #222; font-family: "DejaVu Sans", Arial, sans-serif; font-size: 9.5pt; }
.page { page-break-after: always; min-height: 9.95in; display: flex; flex-direction: column; }
.page:last-child { page-break-after: auto; }
.ar { font-family: "Amiri", serif; direction: rtl; unicode-bidi: isolate; }
.hdr { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2.5px solid #222; padding-bottom: 3px; margin-bottom: 6px; }
.hdr .en { font-size: 12pt; font-weight: bold; }
.hdr .en small { font-weight: normal; color: #666; font-size: 9pt; margin-left: 6px; }
.hdr .ar { font-size: 18pt; font-weight: bold; }
.rule { border: 1.5px solid #222; border-radius: 6px; padding: 5px 9px; margin-bottom: 8px; background: #f7f7f7; }
.rule .ar { font-size: 14pt; line-height: 1.8; text-align: right; }
.rule .en { font-size: 8.5pt; color: #444; margin-top: 2px; }
.row { display: flex; align-items: center; direction: rtl; border-bottom: 1px dotted #bbb; padding: 4px 0; }
.row .ar { font-size: 23pt; line-height: 1.85; flex: 1; text-align: right; word-spacing: 2px; }
.row .hint { direction: ltr; font-size: 7.5pt; color: #777; width: 0.9in; text-align: left; padding-left: 4px; }
.row .cb { width: 0.24in; height: 0.24in; border: 1.5px solid #222; border-radius: 3px; margin-left: 8px; flex: none; }
.sent .ar { font-size: 21pt; line-height: 1.9; }
.copy { margin-top: 10px; }
.copy h3 { font-size: 9pt; margin: 0 0 4px; color: #444; text-transform: uppercase; letter-spacing: 1px; }
.copy h3 .ar { font-size: 13pt; text-transform: none; letter-spacing: 0; font-weight: bold; color: #222; margin-left: 8px; }
.line { position: relative; height: 0.62in; direction: rtl; display: flex; align-items: stretch; }
.line::after { content: ""; position: absolute; left: 0; right: 0; top: 68%; border-top: 1.5px solid #333; }
.line::before { content: ""; position: absolute; left: 0; right: 0; top: 36%; border-top: 1px dashed #bbb; }
.line .model { font-family: "Amiri"; font-size: 22pt; width: 1.9in; flex: none; position: relative; z-index: 1;
  text-align: right; padding: 0 6px 0 10px; border-left: 1px solid #999; }
.line .model span { position: absolute; right: 8px; top: 68%; transform: translateY(-84%); line-height: 1; }
.line.tall { height: 0.8in; }
.line .trace { font-family: "Amiri"; font-size: 30pt; color: #bdbdbd; position: relative; z-index: 1; flex: 1;
  text-align: right; padding-right: 10px; }
.line .trace span { position: absolute; right: 10px; top: 68%; transform: translateY(-84%); line-height: 1; }
.foot { margin-top: auto; padding-top: 4px; font-size: 7.5pt; color: #888; display: flex; justify-content: space-between; }
.story { border: 1px solid #999; border-radius: 6px; padding: 6px 12px; margin-bottom: 8px; }
.story h2 { font-family: "Amiri"; direction: rtl; text-align: right; font-size: 18pt; margin: 0 0 4px; }
.story p { font-family: "Amiri"; direction: rtl; text-align: right; font-size: 19pt; line-height: 2.1; margin: 0; }
.story .q { font-family: "Amiri"; direction: rtl; text-align: right; font-size: 15pt; line-height: 1.9; margin: 4px 0 0; color: #333; }
.story .q b { font-family: "DejaVu Sans"; font-size: 8pt; color: #777; direction: ltr; }
/* writing pages */
.fam { font-size: 8.5pt; color: #444; margin-bottom: 6px; }
.letterrow { display: flex; direction: rtl; align-items: stretch; margin-bottom: 4px; border-bottom: 1px solid #ddd; padding-bottom: 3px; }
.letterrow .nm { width: 0.85in; flex: none; font-family: "Amiri"; font-size: 15pt; text-align: center; padding-top: 6px; border-left: 1px solid #ccc; }
.letterrow .nm big { display: block; font-size: 30pt; line-height: 1.1; }
.letterrow .forms { flex: 1; display: flex; direction: rtl; }
.cell { flex: 1; position: relative; height: 0.78in; border-left: 1px dotted #ccc; }
.cell::after { content: ""; position: absolute; left: 0; right: 0; top: 66%; border-top: 1.5px solid #333; }
.cell::before { content: ""; position: absolute; left: 0; right: 0; top: 34%; border-top: 1px dashed #ccc; }
.cell .lab { position: absolute; top: 1px; right: 4px; font-size: 6.5pt; color: #888; direction: ltr; z-index: 2; }
.cell .t { position: absolute; top: 66%; right: 0; left: 0; transform: translateY(-84%); line-height: 1; text-align: center;
  font-family: "Amiri"; font-size: 30pt; color: #bdbdbd; z-index: 1; direction: rtl; }
.cell .t.dark { color: #222; }
.cell .t.mini { color: #bdbdbd; font-size: 30pt; }
.wordline { display: flex; direction: rtl; margin-top: 6px; }
.wordline .line { flex: 1; }
table.chart { width: 100%; border-collapse: collapse; direction: rtl; }
table.chart th, table.chart td { border: 1px solid #999; text-align: center; padding: 0 4px; font-family: "Amiri"; font-size: 16pt; line-height: 1.3; }
table.chart th { background: #eee; font-family: "DejaVu Sans"; font-size: 8pt; }
table.chart td.nm { font-size: 12pt; color: #555; }
table.chart td.ex { font-size: 14pt; }
table.chart tr.nc td { background: #fff4e0; }
.joinrow { display: flex; direction: rtl; align-items: center; border-bottom: 1px dotted #bbb; padding: 2px 0; }
.joinrow .ar { font-size: 22pt; line-height: 1.8; width: 2.6in; flex: none; text-align: right; }
.joinrow .eq { font-size: 18pt; padding: 0 10px; color: #666; }
.joinrow .line { flex: 1; height: 0.6in; }
.joinrow .boxes { flex: 1; display: flex; direction: rtl; gap: 8px; }
.joinrow .box { flex: 1; height: 0.5in; border: 1.5px solid #333; border-radius: 4px; }
.cols { display: flex; direction: rtl; gap: 12px; }
.col { flex: 1; border: 1.5px solid #333; border-radius: 6px; padding: 4px 8px; }
.col h4 { margin: 0 0 4px; font-family: "Amiri"; direction: rtl; font-size: 18pt; text-align: center; border-bottom: 1px solid #999; }
.col .line { height: 0.5in; }
.wordbank { font-family: "Amiri"; direction: rtl; font-size: 21pt; line-height: 1.9; text-align: right; border: 1px dashed #999; border-radius: 6px; padding: 4px 10px; margin-bottom: 8px; word-spacing: 4px; }
.instr { font-size: 8.5pt; color: #444; margin: 0 0 6px; }
.ruled .line { height: 0.66in; }
/* rules sheet */
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.box { border: 1.5px solid #222; border-radius: 6px; padding: 5px 8px; break-inside: avoid; }
.box h3 { margin: 0 0 3px; font-size: 10pt; border-bottom: 1px solid #999; padding-bottom: 2px; }
.box h3 .ar { font-size: 13pt; float: right; }
.box p { margin: 3px 0; font-size: 9pt; color: #333; line-height: 1.5; }
.box p .ar { font-size: 16pt; }
.box .ex { font-family: "Amiri"; direction: rtl; text-align: right; font-size: 20pt; line-height: 1.8; word-spacing: 3px; }
.box .ex.big { font-size: 24pt; }
.box table { border-collapse: collapse; width: 100%; }
.box td, .box th { border: 1px solid #aaa; padding: 2px 5px; font-size: 9pt; text-align: center; }
.box td.ar { font-size: 19pt; line-height: 1.6; }
"""

def page(body, foot_l="", foot_r=""):
    return f'<div class="page">{body}<div class="foot"><span>{foot_l}</span><span>{foot_r}</span></div></div>'

def hdr(en, ar, sub=""):
    return f'<div class="hdr"><div class="en">{en}<small>{sub}</small></div><div class="ar">{ar}</div></div>'

def line(model="", trace="", tall=False):
    cls = "line tall" if tall else "line"
    m = f'<div class="model"><span>{model}</span></div>' if model else ""
    t = f'<div class="trace"><span>{trace}</span></div>' if trace else '<div class="trace"></div>'
    return f'<div class="{cls}">{m}{t}</div>'

# ---------------- reading pages ----------------
def reading_page(w):
    b = hdr(f"Week {w['n']} · {w['title']}", w["ar_title"], "Reading page " + str(w["n"]))
    b += f'<div class="rule"><div class="ar">{w["rule_ar"]}</div><div class="en">{w["rule_en"]}</div></div>'
    if "stories" in w:
        for s in w["stories"]:
            qs = "".join(f'<div class="q">{i+1}. {q}</div>' for i, q in enumerate(s["q"]))
            b += f'<div class="story"><h2>{s["title"]}</h2><p>{s["text"]}</p>{qs}</div>'
        if w.get("own_lines"):
            b += '<div class="copy"><h3><span class="ar">اُكْتُبِي عَنْ نَفْسِكِ</span> Write three sentences about you</h3>'
            b += "".join(line() for _ in range(w["own_lines"])) + "</div>"
        else:
            b += '<div class="copy"><h3><span class="ar">اُكْتُبِي جَوَابًا وَاحِدًا لِكُلِّ قِصَّةٍ</span> Write one answer for each story</h3>'
            b += line() + line() + "</div>"
    else:
        sent = w["n"] >= 10
        for hint, words in w["rows"]:
            b += f'<div class="row{" sent" if sent else ""}"><div class="cb"></div><div class="ar">{words}</div><div class="hint">{hint}</div></div>'
        if sent:
            b += '<div class="copy"><h3><span class="ar">اُكْتُبِي</span> Copy each sentence on the line under it</h3>'
            for wd in w["copy"]:
                b += f'<div class="ar" style="font-size:20pt;text-align:right;line-height:1.7">{wd}</div>' + line()
        else:
            b += '<div class="copy"><h3><span class="ar">اُكْتُبِي</span> Copy each word (dots after the body, vowels last)</h3>'
            for wd in w["copy"]:
                b += line(model=wd)
        b += "</div>"
    return page(b, f"Every row three times: Mama reads · together · alone. Tick the box.", "Arabic reading pages · week " + str(w["n"]))

def reading_html():
    return "".join(reading_page(w) for w in C.READING)

# ---------------- writing pages ----------------
def forms_chart():
    b = hdr("Letter forms chart", "أَشْكَالُ الْحُرُوفِ", "Writing page 1")
    b += '<p class="instr">Every letter keeps its body and dots; only the tail changes. Shaded rows are the six letters that never join to the letter after them (ا د ذ ر ز و).</p>'
    b += '<table class="chart"><tr><th>Name</th><th>Alone</th><th>Start</th><th>Middle</th><th>End</th><th>Example</th></tr>'
    for name, L, ex in C.ALPHABET:
        nc = L in C.NON_CONNECTORS
        f = C.forms4(L)
        b += f'<tr class="{"nc" if nc else ""}"><td class="nm">{name}</td>' + "".join(f"<td>{s}</td>" for _, s in f) + f'<td class="ex">{ex}</td></tr>'
    b += "</table>"
    return page(b, "Hang this up. In the writing block, point to the form she needs.", "Arabic writing pages")

def family_page(f, idx):
    b = hdr(f"Family {f['n']}: {f['name']}", f"حُرُوفُ الْمَجْمُوعَةِ {f['n']}", f"Writing page {idx}")
    b += f'<p class="fam">{f["note"]} Trace each grey shape in pencil, saying its position, then write it once more in the empty space. Then trace and copy the words.</p>'
    def row(name, L, forms):
        cells = ""
        for lab, s in forms:
            cells += f'<div class="cell"><span class="lab">{lab}</span><div class="t">{s}&nbsp;&nbsp;{s}</div></div>'
        cells += '<div class="cell"><span class="lab">you</span></div>'
        return f'<div class="letterrow{" two" if f.get("two") else ""}"><div class="nm">{name}<big>{L}</big></div><div class="forms">{cells}</div></div>'
    if f.get("two"):
        b = b.replace('<p class="fam">', '<style>.two .cell{height:0.68in}</style><p class="fam">')
    for name, L in f["letters"]:
        b += row(name, L, C.forms2(L) if f.get("two") else C.forms4(L))
    for name, forms in f.get("extra", []):
        b += row(name, forms[0][1], forms)
    b += '<div style="margin-top:6px">'
    for wd in f["words"]:
        b += line(model=wd, trace=wd)
    b += "</div>"
    return page(b, "One family per session. Body first, dots after, vowels last.", "Arabic writing pages")

def join_page(rows, idx, title, sub):
    b = hdr(title, "صِلِي الْحُرُوفَ", f"Writing page {idx}")
    b += f'<p class="instr">{sub}</p>'
    for letters, word in rows:
        b += f'<div class="joinrow"><div class="ar">{letters.replace(" ", " + ")}</div><div class="eq">=</div>{line()}</div>'
    return page(b, "Say each letter with its vowel, then write the word joined, right to left.", "Arabic writing pages")

def split_page(idx):
    b = hdr("Split the word", "فَرِّقِي الْحُرُوفَ", f"Writing page {idx}")
    b += '<p class="instr">Read the word, then write each letter alone, with its vowel, in the boxes (right to left). Words with 2 letters use 2 boxes.</p>'
    for wd in C.SPLIT:
        n = len([ch for ch in wd if "ء" <= ch <= "ي"])
        boxes = "".join('<div class="box"></div>' for _ in range(n))
        b += f'<div class="joinrow"><div class="ar">{wd}</div><div class="eq">=</div><div class="boxes">{boxes}</div></div>'
    return page(b, "This is reading backwards: it makes joining automatic.", "Arabic writing pages")

def madd_page(idx):
    b = hdr("Madd hunt: which long vowel?", "أَيْنَ حَرْفُ الْمَدِّ؟", f"Writing page {idx}")
    b += '<p class="instr">Circle the madd letter in each word (the ا / و / ي with no vowel on it), then copy the word into the right column. Two words have no madd: leave them out.</p>'
    b += '<div class="wordbank">' + " · ".join(C.MADD_SORT + ["كَتَبَ", "لَعِبَ"]) + "</div>"
    cols = "".join(f'<div class="col"><h4>{h}</h4>' + "".join(line() for _ in range(5)) + "</div>" for h in ["ـَا", "ـُو", "ـِي"])
    b += f'<div class="cols">{cols}</div>'
    return page(b, "Weeks 3–4.", "Arabic writing pages")

def sukoon_page(idx):
    b = hdr("Find the sukoon, then copy", "أَيْنَ السُّكُونُ؟", f"Writing page {idx}")
    b += '<p class="instr">Circle every sukoon (ـْ). Read the word gluing the silent letter to the one before. Then copy it.</p>'
    for wd in C.SUKOON_WORDS:
        b += line(model=wd)
    return page(b, "Week 5.", "Arabic writing pages")

def tanween_page(idx):
    b = hdr("Tanween triplets", "التَّنْوِينُ", f"Writing page {idx}")
    b += '<p class="instr">Write each word three times: with tanween damm (ـٌ), tanween fath (ـًا, don\'t forget the alif!) and tanween kasr (ـٍ). The first row is done for you.</p>'
    b += '<div class="joinrow"><div class="ar" style="width:1.6in">كِتَاب</div><div class="boxes">' + "".join(f'<div class="box" style="height:auto;border:0"><div class="line"><div class="trace"><span>{x}</span></div></div></div>' for x in ["كِتَابٌ", "كِتَابًا", "كِتَابٍ"]) + "</div></div>"
    for st in C.TANWEEN_STEMS[1:]:
        b += f'<div class="joinrow"><div class="ar" style="width:1.6in">{st}</div><div class="boxes">' + "".join('<div class="box" style="height:auto;border:0">' + line() + "</div>" for _ in range(3)) + "</div></div>"
    return page(b, "Week 6.", "Arabic writing pages")

def shadda_page(idx):
    b = hdr("Double it", "الشَّدَّةُ", f"Writing page {idx}")
    b += '<p class="instr">Two letters (the first with sukoon) become one letter with shadda. Trace, then write it yourself. Then copy the shadda words.</p>'
    for a, s in C.SHADDA_PAIRS:
        b += f'<div class="joinrow"><div class="ar" style="width:1.4in">{a}</div><div class="eq">=</div><div class="ar" style="width:1in;color:#bdbdbd">{s}</div><div class="eq">→</div>{line()}</div>'
    b += '<div class="copy" style="margin-top:6px"><h3><span class="ar">اُكْتُبِي</span> Copy</h3>'
    for wd in C.SHADDA_WORDS[:6]:
        b += line(model=wd)
    b += "</div>"
    return page(b, "Week 7.", "Arabic writing pages")

def sunmoon_page(idx):
    b = hdr("Sun or moon?", "قَمَرِيَّةٌ أَمْ شَمْسِيَّةٌ؟", f"Writing page {idx}")
    b += '<p class="instr">Read each word. If you say the ل, it goes under the moon. If the ل is silent and the next letter has a shadda, it goes under the sun. Copy it into its column.</p>'
    b += '<div class="wordbank">' + " · ".join(C.SUNMOON) + "</div>"
    cols = "".join(f'<div class="col"><h4>{h}</h4>' + "".join(line() for _ in range(8)) + "</div>" for h in ["☾ قَمَرِيَّةٌ", "☀ شَمْسِيَّةٌ"])
    b += f'<div class="cols">{cols}</div>'
    return page(b, "Week 8. Moon letters: ا ب ج ح خ ع غ ف ق ك م ه و ي · Sun letters: ت ث د ذ ر ز س ش ص ض ط ظ ل ن", "Arabic writing pages")

def endings_page(idx):
    b = hdr("Which ending?", "ة أَمْ ه؟ ى أَمْ ي؟", f"Writing page {idx}")
    b += '<p class="instr">Say the word out loud (Mama says it if needed). Choose the right ending, then write the whole word on the line.</p>'
    for stem, a, bb in C.ENDINGS:
        b += f'<div class="joinrow"><div class="ar" style="width:1.6in">{stem}ـــ</div><div class="ar" style="width:1.1in;color:#555">{a} &nbsp;/&nbsp; {bb}</div><div class="eq">→</div>{line()}</div>'
    return page(b, "Week 9. Hint: 'his/her something' ends in ه (كِتَابُهُ); girls' words and most feminine nouns end in ة.", "Arabic writing pages")

def ruled_page(idx, title="Dictation paper"):
    b = hdr(title, "إِمْلَاءٌ", f"Writing page {idx}")
    b += '<p class="instr">Date: ____________ &nbsp;&nbsp; Words from reading page: ____ &nbsp;&nbsp; She writes on the line, then checks against the page and fixes in another colour.</p>'
    b += '<div class="ruled">' + "".join(line() for _ in range(12)) + "</div>"
    return page(b, "Print as many as you need.", "Arabic writing pages")

def writing_html():
    pages = [forms_chart()]
    i = 2
    for f in C.FAMILIES:
        pages.append(family_page(f, i)); i += 1
    pages.append(join_page(C.JOIN1, i, "Join the letters (1)", "Weeks 1–2. Letters with short vowels only.")); i += 1
    pages.append(join_page(C.JOIN2, i, "Join the letters (2)", "Weeks 3–9. Includes madd, sukoon, tanween, shadda, ة.")); i += 1
    pages.append(split_page(i)); i += 1
    pages.append(madd_page(i)); i += 1
    pages.append(sukoon_page(i)); i += 1
    pages.append(tanween_page(i)); i += 1
    pages.append(shadda_page(i)); i += 1
    pages.append(sunmoon_page(i)); i += 1
    pages.append(endings_page(i)); i += 1
    pages.append(ruled_page(i)); i += 1
    pages.append(ruled_page(i, "Dictation paper (copy)")); i += 1
    return "".join(pages)

# ---------------- rules sheet ----------------
def box(title_en, title_ar, inner):
    return f'<div class="box"><h3>{title_en}<span class="ar">{title_ar}</span></h3>{inner}</div>'

def rules_html():
    p1 = hdr("Arabic reading rules, on one sheet", "قَوَاعِدُ الْقِرَاءَةِ", "Rules sheet 1 of 2")
    g = ""
    g += box("Short vowels (she knows these)", "الْحَرَكَاتُ",
        '<table><tr><th>fatha ـَ</th><th>kasra ـِ</th><th>damma ـُ</th></tr><tr><td class="ar">بَ تَ جَ</td><td class="ar">بِ تِ جِ</td><td class="ar">بُ تُ جُ</td></tr></table>'
        '<p>One clap each. Say them in random order until instant.</p>')
    g += box("Letters hold hands", "الْحُرُوفُ تَتَّصِلُ",
        '<div class="ex big">ب &nbsp; بـ &nbsp; ـبـ &nbsp; ـب</div><p>Body and dots stay; the tail changes. Tap each letter with its vowel, then slide: كَ – تَ – بَ ← كَتَبَ</p>'
        '<p><b>Six letters let go</b> (join only from the right): <span class="ar" style="font-size:14pt">ا د ذ ر ز و</span> &nbsp; <span class="ar">دَرَسَ · وَلَد · زَرَعَ</span></p>')
    g += box("Long vowels (madd): two claps", "حُرُوفُ الْمَدِّ",
        '<table><tr><th>ـَا</th><th>ـُو</th><th>ـِي</th></tr><tr><td class="ar">قَالَ نَامَ بَاب</td><td class="ar">يَقُولُ نُور</td><td class="ar">فِي كَبِير</td></tr></table>'
        '<p>The madd letter has no vowel of its own. Short vs long: <span class="ar">جَمَل / جَمَال</span></p>')
    g += box("Sukoon: glue it", "السُّكُونُ",
        '<div class="ex">مِنْ · هَلْ · يَكْتُبُ · يَلْعَبُ</div><p>No vowel: join it to the letter before. Special pairs: fatha + يْ = "ay" <span class="ar">بَيْت</span>, fatha + وْ = "aw" <span class="ar">يَوْم</span></p>')
    g += box("Tanween: add an n", "التَّنْوِينُ",
        '<table><tr><th>ـٌ un</th><th>ـًا an</th><th>ـٍ in</th></tr><tr><td class="ar">كِتَابٌ</td><td class="ar">كِتَابًا</td><td class="ar">كِتَابٍ</td></tr></table>'
        '<p>Only at the end of a word. Fath rides an alif (except after ة: <span class="ar">مَدْرَسَةً</span>). The n is heard, not written.</p>')
    g += box("Shadda: say it twice", "الشَّدَّةُ",
        '<div class="ex">رَبّ = رَبْ + بَ &nbsp;·&nbsp; مُعَلِّم · سَيَّارَة · أُمٌّ</div><p>First with sukoon, then with its vowel. Clap twice.</p>')
    p1 += f'<div class="grid">{g}</div>'
    page1 = page(p1, "Teach them in this order, one a week.", "Arabic rules sheet")

    p2 = hdr("Arabic reading rules, on one sheet", "قَوَاعِدُ الْقِرَاءَةِ", "Rules sheet 2 of 2")
    g = ""
    g += box("ال with moon letters: say the ل", "الْحُرُوفُ الْقَمَرِيَّةُ",
        '<div class="ex big">ا ب ج ح خ ع غ ف ق ك م ه و ي</div><div class="ex">الْقَمَر · الْبَاب · الْكِتَاب · الْوَلَد</div><p>The ل carries a sukoon. Chant: <span class="ar">إِبْغِ حَجَّكَ وَخَفْ عَقِيمَهُ</span></p>')
    g += box("ال with sun letters: skip the ل", "الْحُرُوفُ الشَّمْسِيَّةُ",
        '<div class="ex big">ت ث د ذ ر ز س ش ص ض ط ظ ل ن</div><div class="ex">الشَّمْس · النَّهْر · الدَّرْس · السَّمَاء</div><p>The ل is written but silent; the next letter gets a shadda. Look at the ل: nothing on it → don\'t say it.</p>')
    g += box("Taa marbuta and alif maqsura", "ة · ى",
        '<div class="ex">مَدْرَسَة · شَجَرَة · فَاطِمَة &nbsp;|&nbsp; عَلَى · إِلَى · مُوسَى</div><p><b>ة</b> only at the end: "t" when continuing, "h" when stopping. <b>ى</b> only at the end: sounds like a long "aa". Compare <span class="ar">كِتَابُهُ</span> (his book, ه) and <span class="ar">فِي، عَلِي</span> (ي with dots).</p>')
    g += box("Five shapes of hamza, one sound", "الْهَمْزَةُ",
        '<table><tr><th>أ</th><th>إ</th><th>ؤ</th><th>ئ</th><th>ء</th></tr><tr><td class="ar">أَحْمَد سَأَلَ</td><td class="ar">إِلَى إِنَّ</td><td class="ar">سُؤَال</td><td class="ar">بِئْر سَائِل</td><td class="ar">مَاء شَيْء</td></tr></table>'
        '<p>Read the vowel on it. Which seat is a spelling rule for later. <span class="ar">آ</span> = hamza + alif madd: <span class="ar">آدَم، قُرْآن</span></p>')
    g += box("Reading sentences", "قِرَاءَةُ الْجُمَلِ",
        '<div class="ex">ذَهَبَ الْوَلَدُ إِلَى الْمَدْرَسَةِ.</div><p><b>Stop</b> at the end: drop the last vowel (ة → "h", tanween fath → long "aa": <span class="ar">قَلَمًا</span> = "qalamaa").<br><b>ال after a word</b> loses its alif sound: <span class="ar">فِي الْبَيْتِ</span> = "fil-bayt".<br>Silent alif after و in plurals: <span class="ar">كَتَبُوا</span>. Small alif = madd: <span class="ar">هَٰذَا، لَٰكِنْ</span>.<br>Punctuation: ، ؟ . &nbsp; Numbers: <span class="ar">٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩</span></p>')
    g += box("Little words she will see everywhere", "كَلِمَاتٌ صَغِيرَةٌ",
        '<div class="ex">مِنْ · عَنْ · فِي · إِلَى · عَلَى · مَعَ · هَلْ · لَمْ · لَنْ · قَدْ · لَا · مَا · يَا<br>أَنَا · أَنْتَ · أَنْتِ · هُوَ · هِيَ · نَحْنُ · هُمْ · هَذَا · هَذِهِ<br>مَنْ · مَاذَا · أَيْنَ · كَيْفَ · مَتَى · كَمْ · نَعَمْ</div>')
    p2 += f'<div class="grid">{g}</div>'
    page2 = page(p2, "Order: joining → madd → sukoon → tanween → shadda → ال → endings → sentences.", "Arabic rules sheet")
    return page1 + page2

# ---------------- guide (markdown chapters) ----------------
GUIDE_CSS = FONT_CSS + """
@page { size: Letter portrait; margin: 0.6in 0.65in; }
body { font-family: "AmiriAR", "DejaVu Sans", Arial, sans-serif; color:#222; font-size: 10pt; line-height: 1.45; margin:0; }
.chapter { page-break-before: always; }
.cover { height: 9.4in; display:flex; flex-direction:column; justify-content:center; text-align:center; page-break-after: always; }
.cover h1 { font-size: 30pt; margin: 0 0 10px; border: 0; }
.cover .ar { font-family: "Amiri"; font-size: 28pt; direction: rtl; }
.cover p { font-size: 12pt; color:#555; margin: 4px 0; }
.cover .toc { margin-top: 30px; text-align:left; display:inline-block; font-size: 11pt; line-height: 1.9; }
h1 { font-size: 19pt; border-bottom: 3px solid #222; padding-bottom: 4px; margin: 0 0 10px; }
h2 { font-size: 13.5pt; margin: 16px 0 6px; border-bottom: 1px solid #bbb; padding-bottom: 2px; page-break-after: avoid; }
h3 { font-size: 11pt; margin: 12px 0 4px; page-break-after: avoid; }
p { margin: 4px 0 6px; }
ul, ol { margin: 2px 0 6px; padding-left: 18px; }
li { margin-bottom: 2px; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 10px; font-size: 9pt; }
th, td { border: 1px solid #999; padding: 3px 6px; vertical-align: top; text-align: left; }
th { background: #eee; }
tr { page-break-inside: avoid; }
code { font-family: "AmiriAR", "DejaVu Sans Mono", monospace; font-size: 9pt; background:#f2f2f2; padding: 0 3px; }
hr { border: 0; border-top: 1px solid #ccc; margin: 12px 0; }
a { color: #222; text-decoration: none; }
input[type=checkbox] { margin: 0 4px 0 0; }
"""
CHAPTERS = ["README.md", "01-arabic-reading-rules.md", "02-how-to-teach-arabic.md", "03-twelve-week-plan.md", "04-activity-bank.md", "05-progress-tracker.md"]

def md_to_html(path):
    text = pathlib.Path(path).read_text()
    text = re.sub(r'\[([^\]]+)\]\((?:\d\d-[^)]+\.md|README\.md|printables/[^)]+)\)', r'\1', text)
    text = text.replace("- [ ] ", "- ☐ ")
    return markdown.markdown(text, extensions=["tables", "sane_lists"])

def guide_html():
    cover = """<div class="cover"><h1>Arabic Reading &amp; Writing at Home</h1>
    <div class="ar">الْقِرَاءَةُ وَالْكِتَابَةُ فِي الْبَيْتِ</div>
    <p>For a child who knows the letters with tashkeel and is ready to read and write words</p>
    <p>One rule a week · 25 minutes a day · 12 weeks</p>
    <div class="toc">1. Overview and golden rules<br>2. The rules of reading, in teaching order<br>3. How to teach: reading, writing, dictation<br>
    4. The 12-week plan<br>5. Activity bank (35 games)<br>6. Progress tracker<br><span style="color:#777">Then: reading pages, writing pages, rules sheet</span></div></div>"""
    chapters = "".join(f'<div class="chapter">{md_to_html(ROOT / c)}</div>' for c in CHAPTERS)
    return cover + chapters

def doc(body, css, title):
    return f"<!doctype html><html lang='en'><head><meta charset='utf-8'><title>{title}</title><style>{css}</style></head><body>{body}</body></html>"

if __name__ == "__main__":
    (HERE / "reading-pages.html").write_text(doc(reading_html(), PAGE_CSS, "Arabic reading pages"))
    (HERE / "writing-pages.html").write_text(doc(writing_html(), PAGE_CSS, "Arabic writing pages"))
    (HERE / "rules-sheet.html").write_text(doc(rules_html(), PAGE_CSS, "Arabic rules sheet"))
    if markdown:
        (HERE / "guide.html").write_text(doc(guide_html(), GUIDE_CSS, "Arabic guide"))
    else:
        print("python 'markdown' package missing: guide.html not rebuilt")
    print("html written")
