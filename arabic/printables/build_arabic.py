# -*- coding: utf-8 -*-
# يولّد ملفات HTML للمطبوعات العربية (صفحات القراءة، صفحات الكتابة، ورقة القواعد، الدليل).
# التحويل إلى PDF عبر كروميوم (انظري build.sh). المحتوى في content.py.
import pathlib, re, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import content as C
try:
    import markdown
except ImportError:
    markdown = None

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent

def ar(n):
    """أرقام عربية مشرقية"""
    return str(n).translate(str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩"))

FONT_CSS = """
@font-face { font-family: "Amiri"; src: url("fonts/Amiri-Regular.ttf"); font-weight: normal; }
@font-face { font-family: "Amiri"; src: url("fonts/Amiri-Bold.ttf"); font-weight: bold; }
"""

PAGE_CSS = FONT_CSS + """
@page { size: Letter portrait; margin: 0.45in 0.5in; }
* { box-sizing: border-box; }
body { margin: 0; color: #222; font-family: "Amiri", serif; font-size: 11pt; direction: rtl; }
.page { page-break-after: always; min-height: 9.95in; display: flex; flex-direction: column; }
.page:last-child { page-break-after: auto; }
.ar { font-family: "Amiri", serif; direction: rtl; unicode-bidi: isolate; }
.hdr { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2.5px solid #222; padding-bottom: 3px; margin-bottom: 6px; }
.hdr .ttl { font-size: 19pt; font-weight: bold; }
.hdr .sub { font-size: 10pt; color: #666; }
.rule { border: 1.5px solid #222; border-radius: 6px; padding: 5px 9px; margin-bottom: 8px; background: #f7f7f7; }
.rule .ar { font-size: 14pt; line-height: 1.8; text-align: right; }
.rule .en { font-size: 10pt; color: #444; margin-top: 2px; line-height: 1.6; }
.row { display: flex; align-items: center; direction: rtl; border-bottom: 1px dotted #bbb; padding: 4px 0; }
.row .ar { font-size: 23pt; line-height: 1.85; flex: 1; text-align: right; word-spacing: 2px; }
.row .hint { font-size: 9pt; color: #777; width: 0.95in; text-align: left; padding-left: 4px; line-height: 1.4; }
.row .cb { width: 0.24in; height: 0.24in; border: 1.5px solid #222; border-radius: 3px; margin-left: 8px; flex: none; }
.sent .ar { font-size: 21pt; line-height: 1.9; }
.copy { margin-top: 10px; }
.copy h3 { font-size: 13pt; margin: 0 0 4px; color: #222; }
.copy h3 small { font-size: 9.5pt; color: #666; font-weight: normal; margin-right: 8px; }
.line { position: relative; height: 0.62in; direction: rtl; display: flex; align-items: stretch; }
.line::after { content: ""; position: absolute; left: 0; right: 0; top: 68%; border-top: 1.5px solid #333; }
.line::before { content: ""; position: absolute; left: 0; right: 0; top: 36%; border-top: 1px dashed #bbb; }
.line .model { font-size: 22pt; width: 1.9in; flex: none; position: relative; z-index: 1; text-align: right; padding: 0 6px 0 10px; border-left: 1px solid #999; }
.line .model span { position: absolute; right: 8px; top: 68%; transform: translateY(-84%); line-height: 1; }
.line .trace { font-size: 30pt; color: #bdbdbd; position: relative; z-index: 1; flex: 1; text-align: right; padding-right: 10px; }
.line .trace span { position: absolute; right: 10px; top: 68%; transform: translateY(-84%); line-height: 1; }
.foot { margin-top: auto; padding-top: 4px; font-size: 9pt; color: #888; display: flex; justify-content: space-between; }
.story { border: 1px solid #999; border-radius: 6px; padding: 6px 12px; margin-bottom: 8px; }
.story h2 { direction: rtl; text-align: right; font-size: 18pt; margin: 0 0 4px; }
.story p { direction: rtl; text-align: right; font-size: 19pt; line-height: 2.1; margin: 0; }
.story .q { direction: rtl; text-align: right; font-size: 15pt; line-height: 1.9; margin: 4px 0 0; color: #333; }
/* صفحات الكتابة */
.fam { font-size: 10.5pt; color: #444; margin: 0 0 6px; line-height: 1.6; }
.letterrow { display: flex; direction: rtl; align-items: stretch; margin-bottom: 4px; border-bottom: 1px solid #ddd; padding-bottom: 3px; }
.letterrow .nm { width: 0.85in; flex: none; font-size: 15pt; text-align: center; padding-top: 6px; border-left: 1px solid #ccc; }
.letterrow .nm big { display: block; font-size: 30pt; line-height: 1.1; }
.letterrow .forms { flex: 1; display: flex; direction: rtl; }
.cell { flex: 1; position: relative; height: 0.78in; border-left: 1px dotted #ccc; }
.two .cell { height: 0.68in; }
.cell::after { content: ""; position: absolute; left: 0; right: 0; top: 66%; border-top: 1.5px solid #333; }
.cell::before { content: ""; position: absolute; left: 0; right: 0; top: 34%; border-top: 1px dashed #ccc; }
.cell .lab { position: absolute; top: 0; right: 4px; font-size: 8.5pt; color: #888; z-index: 2; }
.cell .t { position: absolute; top: 66%; right: 0; left: 0; transform: translateY(-84%); line-height: 1; text-align: center; font-size: 30pt; color: #bdbdbd; z-index: 1; direction: rtl; }
table.chart { width: 100%; border-collapse: collapse; direction: rtl; }
table.chart th, table.chart td { border: 1px solid #999; text-align: center; padding: 0 4px; font-size: 16pt; line-height: 1.3; }
table.chart th { background: #eee; font-size: 11pt; }
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
.col h4 { margin: 0 0 4px; direction: rtl; font-size: 18pt; text-align: center; border-bottom: 1px solid #999; }
.col .line { height: 0.5in; }
.wordbank { direction: rtl; font-size: 21pt; line-height: 1.9; text-align: right; border: 1px dashed #999; border-radius: 6px; padding: 4px 10px; margin-bottom: 8px; word-spacing: 4px; }
.instr { font-size: 10.5pt; color: #444; margin: 0 0 6px; line-height: 1.6; }
.ruled .line { height: 0.66in; }
/* ورقة القواعد */
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
.box { border: 1.5px solid #222; border-radius: 6px; padding: 5px 8px; break-inside: avoid; }
.box h3 { margin: 0 0 3px; font-size: 14pt; border-bottom: 1px solid #999; padding-bottom: 2px; }
.box p { margin: 3px 0; font-size: 10.5pt; color: #333; line-height: 1.6; }
.box .ex { direction: rtl; text-align: right; font-size: 20pt; line-height: 1.8; word-spacing: 3px; }
.box .ex.big { font-size: 24pt; }
.box table { border-collapse: collapse; width: 100%; }
.box td, .box th { border: 1px solid #aaa; padding: 2px 5px; font-size: 11pt; text-align: center; }
.box td.ar { font-size: 19pt; line-height: 1.6; }
"""

def page(body, foot_r="", foot_l=""):
    return f'<div class="page">{body}<div class="foot"><span>{foot_r}</span><span>{foot_l}</span></div></div>'

def hdr(title, sub=""):
    return f'<div class="hdr"><div class="ttl">{title}</div><div class="sub">{sub}</div></div>'

def line(model="", trace="", tall=False):
    m = f'<div class="model"><span>{model}</span></div>' if model else ""
    t = f'<div class="trace"><span>{trace}</span></div>' if trace else '<div class="trace"></div>'
    return f'<div class="line">{m}{t}</div>'

# ---------------- صفحات القراءة ----------------
def reading_page(w):
    b = hdr(f"الأسبوع {ar(w['n'])} · {w['ar_title']}", f"صفحة القراءة {ar(w['n'])}")
    b += f'<div class="rule"><div class="ar">{w["rule_ar"]}</div><div class="en">{w["rule_en"]}</div></div>'
    if "stories" in w:
        for s in w["stories"]:
            qs = "".join(f'<div class="q">{ar(i+1)}. {q}</div>' for i, q in enumerate(s["q"]))
            b += f'<div class="story"><h2>{s["title"]}</h2><p>{s["text"]}</p>{qs}</div>'
        if w.get("own_lines"):
            b += '<div class="copy"><h3>اُكْتُبِي ثَلَاثَ جُمَلٍ عَنْ نَفْسِكِ</h3>' + "".join(line() for _ in range(w["own_lines"])) + "</div>"
        else:
            b += '<div class="copy"><h3>اُكْتُبِي جَوَابًا وَاحِدًا لِكُلِّ قِصَّةٍ</h3>' + line() + line() + "</div>"
    else:
        sent = w["n"] >= 10
        for hint, words in w["rows"]:
            b += f'<div class="row{" sent" if sent else ""}"><div class="cb"></div><div class="ar">{words}</div><div class="hint">{hint}</div></div>'
        if sent:
            b += '<div class="copy"><h3>اُكْتُبِي <small>انقلي كل جملة على السطر الذي تحتها</small></h3>'
            for wd in w["copy"]:
                b += f'<div class="ar" style="font-size:20pt;text-align:right;line-height:1.7">{wd}</div>' + line()
        else:
            b += '<div class="copy"><h3>اُكْتُبِي <small>انقلي كل كلمة (الجسم أولًا، ثم النقاط، ثم الحركات)</small></h3>'
            for wd in w["copy"]:
                b += line(model=wd)
        b += "</div>"
    return page(b, "كل سطر ثلاث مرات: ماما تقرأ · معًا · وحدي. ثم أشّري في المربع.", f"صفحات القراءة · الأسبوع {ar(w['n'])}")

def reading_html():
    return "".join(reading_page(w) for w in C.READING)

# ---------------- صفحات الكتابة ----------------
def forms_chart():
    b = hdr("جدول أشكال الحروف", "صفحة الكتابة ١")
    b += '<p class="instr">كل حرف يحتفظ بجسمه ونقاطه؛ الذيل وحده يتغير. الصفوف الملوّنة هي الحروف الستة التي لا تتصل بالحرف الذي بعدها (ا د ذ ر ز و).</p>'
    b += '<table class="chart"><tr><th>الاسم</th><th>مفرد</th><th>في الأول</th><th>في الوسط</th><th>في الآخر</th><th>مثال</th></tr>'
    for name, L, ex in C.ALPHABET:
        nc = L in C.NON_CONNECTORS
        b += f'<tr class="{"nc" if nc else ""}"><td class="nm">{name}</td>' + "".join(f"<td>{s}</td>" for _, s in C.forms4(L)) + f'<td class="ex">{ex}</td></tr>'
    b += "</table>"
    return page(b, "علّقيه. في فقرة الكتابة أشيري إلى الشكل الذي تحتاجه.", "صفحات الكتابة")

def family_page(f, idx):
    b = hdr(f"المجموعة {ar(f['n'])}: {f['name']}", f"صفحة الكتابة {ar(idx)}")
    b += f'<p class="fam">{f["note"]} تتبّعي كل شكل رمادي بالقلم وأنت تقولين موضعه، ثم اكتبيه مرة أخرى في الفراغ. ثم تتبّعي الكلمات وانقليها.</p>'
    def row(name, L, forms):
        cells = "".join(f'<div class="cell"><span class="lab">{lab}</span><div class="t">{s}&nbsp;&nbsp;{s}</div></div>' for lab, s in forms)
        cells += '<div class="cell"><span class="lab">أنتِ</span></div>'
        return f'<div class="letterrow{" two" if f.get("two") else ""}"><div class="nm">{name}<big>{L}</big></div><div class="forms">{cells}</div></div>'
    for name, L in f["letters"]:
        b += row(name, L, C.forms2(L) if f.get("two") else C.forms4(L))
    for name, forms in f.get("extra", []):
        b += row(name, forms[0][1], forms)
    b += '<div style="margin-top:6px">' + "".join(line(model=wd, trace=wd) for wd in f["words"]) + "</div>"
    return page(b, "مجموعة واحدة في الجلسة. الجسم أولًا، ثم النقاط، ثم الحركات.", "صفحات الكتابة")

def join_page(rows, idx, title, sub):
    b = hdr(title, f"صفحة الكتابة {ar(idx)}")
    b += f'<p class="instr">{sub}</p>'
    for letters, word in rows:
        b += f'<div class="joinrow"><div class="ar">{letters.replace(" ", " + ")}</div><div class="eq">=</div>{line()}</div>'
    return page(b, "قولي كل حرف مع حركته، ثم اكتبي الكلمة متصلة من اليمين إلى اليسار.", "صفحات الكتابة")

def split_page(idx):
    b = hdr("فَرِّقِي الْحُرُوفَ", f"صفحة الكتابة {ar(idx)}")
    b += '<p class="instr">اقرئي الكلمة، ثم اكتبي كل حرف وحده مع حركته في المربعات (من اليمين إلى اليسار). الكلمات ذات الحرفين لها مربعان.</p>'
    for wd in C.SPLIT:
        n = len([ch for ch in wd if "ء" <= ch <= "ي"])
        b += f'<div class="joinrow"><div class="ar">{wd}</div><div class="eq">=</div><div class="boxes">{"".join("<div class=box></div>" for _ in range(n))}</div></div>'
    return page(b, "هذه قراءة معكوسة: تجعل الاتصال تلقائيًا.", "صفحات الكتابة")

def madd_page(idx):
    b = hdr("أَيْنَ حَرْفُ الْمَدِّ؟", f"صفحة الكتابة {ar(idx)}")
    b += '<p class="instr">حوّطي حرف المد في كل كلمة (الألف أو الواو أو الياء التي لا حركة عليها)، ثم انقلي الكلمة في العمود المناسب. كلمتان ليس فيهما مد: اتركيهما.</p>'
    b += '<div class="wordbank">' + " · ".join(C.MADD_SORT + ["كَتَبَ", "لَعِبَ"]) + "</div>"
    b += '<div class="cols">' + "".join(f'<div class="col"><h4>{h}</h4>' + "".join(line() for _ in range(5)) + "</div>" for h in ["ـَا", "ـُو", "ـِي"]) + "</div>"
    return page(b, "الأسبوعان ٣ و٤.", "صفحات الكتابة")

def sukoon_page(idx):
    b = hdr("أَيْنَ السُّكُونُ؟", f"صفحة الكتابة {ar(idx)}")
    b += '<p class="instr">حوّطي كل سكون (ـْ). اقرئي الكلمة وألصقي الحرف الساكن بالذي قبله. ثم انقليها.</p>'
    b += "".join(line(model=wd) for wd in C.SUKOON_WORDS)
    return page(b, "الأسبوع ٥.", "صفحات الكتابة")

def tanween_page(idx):
    b = hdr("ثُلَاثِيَّاتُ التَّنْوِينِ", f"صفحة الكتابة {ar(idx)}")
    b += '<p class="instr">اكتبي كل كلمة ثلاث مرات: بتنوين الضم (ـٌ)، وتنوين الفتح (ـًا، لا تنسي الألف!)، وتنوين الكسر (ـٍ). السطر الأول مكتوب لك.</p>'
    b += '<div class="joinrow"><div class="ar" style="width:1.6in">كِتَاب</div><div class="boxes">' + "".join(f'<div class="box" style="height:auto;border:0"><div class="line"><div class="trace"><span>{x}</span></div></div></div>' for x in ["كِتَابٌ", "كِتَابًا", "كِتَابٍ"]) + "</div></div>"
    for st in C.TANWEEN_STEMS[1:]:
        b += f'<div class="joinrow"><div class="ar" style="width:1.6in">{st}</div><div class="boxes">' + "".join('<div class="box" style="height:auto;border:0">' + line() + "</div>" for _ in range(3)) + "</div></div>"
    return page(b, "الأسبوع ٦.", "صفحات الكتابة")

def shadda_page(idx):
    b = hdr("ضَاعِفِيهِ", f"صفحة الكتابة {ar(idx)}")
    b += '<p class="instr">حرفان (الأول ساكن) يصيران حرفًا واحدًا مشددًا. تتبّعي، ثم اكتبيه بنفسك. ثم انقلي كلمات الشدة.</p>'
    for a, s in C.SHADDA_PAIRS:
        b += f'<div class="joinrow"><div class="ar" style="width:1.4in">{a}</div><div class="eq">=</div><div class="ar" style="width:1in;color:#bdbdbd">{s}</div><div class="eq">←</div>{line()}</div>'
    b += '<div class="copy" style="margin-top:6px"><h3>اُكْتُبِي</h3>' + "".join(line(model=wd) for wd in C.SHADDA_WORDS[:6]) + "</div>"
    return page(b, "الأسبوع ٧.", "صفحات الكتابة")

def sunmoon_page(idx):
    b = hdr("قَمَرِيَّةٌ أَمْ شَمْسِيَّةٌ؟", f"صفحة الكتابة {ar(idx)}")
    b += '<p class="instr">اقرئي كل كلمة. إن نطقتِ اللام فهي تحت القمر. إن كانت اللام صامتة والحرف بعدها مشددًا فهي تحت الشمس. انقليها في عمودها.</p>'
    b += '<div class="wordbank">' + " · ".join(C.SUNMOON) + "</div>"
    b += '<div class="cols">' + "".join(f'<div class="col"><h4>{h}</h4>' + "".join(line() for _ in range(8)) + "</div>" for h in ["☾ قَمَرِيَّةٌ", "☀ شَمْسِيَّةٌ"]) + "</div>"
    return page(b, "الأسبوع ٨. القمرية: ا ب ج ح خ ع غ ف ق ك م ه و ي · الشمسية: ت ث د ذ ر ز س ش ص ض ط ظ ل ن", "صفحات الكتابة")

def endings_page(idx):
    b = hdr("ة أَمْ ه؟ ى أَمْ ي؟", f"صفحة الكتابة {ar(idx)}")
    b += '<p class="instr">قولي الكلمة بصوت عالٍ (ماما تقولها عند الحاجة). اختاري النهاية الصحيحة، ثم اكتبي الكلمة كاملة على السطر.</p>'
    for stem, a, bb in C.ENDINGS:
        b += f'<div class="joinrow"><div class="ar" style="width:1.6in">{stem}ـــ</div><div class="ar" style="width:1.1in;color:#555">{a} &nbsp;/&nbsp; {bb}</div><div class="eq">←</div>{line()}</div>'
    return page(b, "الأسبوع ٩. تلميح: ضمير الغائب في الآخر هاء (كِتَابُهُ)؛ أغلب الأسماء المؤنثة تنتهي بـ ة.", "صفحات الكتابة")

def ruled_page(idx, title="وَرَقَةُ إِمْلَاءٍ"):
    b = hdr(title, f"صفحة الكتابة {ar(idx)}")
    b += '<p class="instr">التاريخ: ____________ &nbsp;&nbsp; كلمات من صفحة القراءة رقم: ____ &nbsp;&nbsp; تكتب على السطر، ثم تراجع على الصفحة وتصحح بلون آخر.</p>'
    b += '<div class="ruled">' + "".join(line() for _ in range(12)) + "</div>"
    return page(b, "اطبعي منها ما تحتاجين.", "صفحات الكتابة")

def writing_html():
    pages = [forms_chart()]
    i = 2
    for f in C.FAMILIES:
        pages.append(family_page(f, i)); i += 1
    pages.append(join_page(C.JOIN1, i, "صِلِي الْحُرُوفَ (١)", "الأسبوعان ١ و٢. حروف بالحركات القصيرة فقط.")); i += 1
    pages.append(join_page(C.JOIN2, i, "صِلِي الْحُرُوفَ (٢)", "الأسابيع ٣ إلى ٩. فيها مد وسكون وتنوين وشدة و ة.")); i += 1
    for fn in (split_page, madd_page, sukoon_page, tanween_page, shadda_page, sunmoon_page, endings_page, ruled_page):
        pages.append(fn(i)); i += 1
    pages.append(ruled_page(i, "وَرَقَةُ إِمْلَاءٍ (نسخة ثانية)")); i += 1
    return "".join(pages)

# ---------------- ورقة القواعد ----------------
def box(title, inner):
    return f'<div class="box"><h3>{title}</h3>{inner}</div>'

def rules_html():
    p1 = hdr("قَوَاعِدُ الْقِرَاءَةِ فِي وَرَقَةٍ وَاحِدَةٍ", "ورقة القواعد ١ من ٢")
    g = ""
    g += box("الحركات (تعرفها)",
        '<table><tr><th>فتحة ـَ</th><th>كسرة ـِ</th><th>ضمة ـُ</th></tr><tr><td class="ar">بَ تَ جَ</td><td class="ar">بِ تِ جِ</td><td class="ar">بُ تُ جُ</td></tr></table>'
        '<p>تصفيقة واحدة لكل حركة. قوليها بترتيب عشوائي حتى تصبح فورية.</p>')
    g += box("الحروف تتماسك",
        '<div class="ex big">ب &nbsp; بـ &nbsp; ـبـ &nbsp; ـب</div><p>الجسم والنقاط يبقيان؛ الذيل يتغير. انقري كل حرف مع حركته ثم انزلقي: كَ – تَ – بَ ← كَتَبَ</p>'
        '<p><b>ستة حروف تترك اليد</b> (تتصل من اليمين فقط): <span class="ar" style="font-size:16pt">ا د ذ ر ز و</span> &nbsp; <span class="ar" style="font-size:16pt">دَرَسَ · وَلَد · زَرَعَ</span></p>')
    g += box("حروف المد: تصفيقتان",
        '<table><tr><th>ـَا</th><th>ـُو</th><th>ـِي</th></tr><tr><td class="ar">قَالَ نَامَ بَاب</td><td class="ar">يَقُولُ نُور</td><td class="ar">فِي كَبِير</td></tr></table>'
        '<p>حرف المد لا حركة له. قصير مقابل طويل: <span class="ar" style="font-size:16pt">جَمَل / جَمَال</span></p>')
    g += box("السكون: ألصقيه",
        '<div class="ex">مِنْ · هَلْ · يَكْتُبُ · يَلْعَبُ</div><p>لا حركة: صليه بالحرف الذي قبله. زوجان خاصان: فتحة + يْ = «أَيْ» <span class="ar" style="font-size:16pt">بَيْت</span>، فتحة + وْ = «أَوْ» <span class="ar" style="font-size:16pt">يَوْم</span></p>')
    g += box("التنوين: أضيفي نونًا",
        '<table><tr><th>ـٌ «أُنْ»</th><th>ـًا «أَنْ»</th><th>ـٍ «إِنْ»</th></tr><tr><td class="ar">كِتَابٌ</td><td class="ar">كِتَابًا</td><td class="ar">كِتَابٍ</td></tr></table>'
        '<p>في آخر الكلمة فقط. تنوين الفتح يركب ألفًا (إلا بعد ة: <span class="ar" style="font-size:16pt">مَدْرَسَةً</span>). النون تُسمع ولا تُكتب.</p>')
    g += box("الشدة: انطقيه مرتين",
        '<div class="ex">رَبّ = رَبْ + بَ &nbsp;·&nbsp; مُعَلِّم · سَيَّارَة · أُمٌّ</div><p>الأولى بالسكون، والثانية بحركته. تصفيقتان.</p>')
    page1 = page(p1 + f'<div class="grid">{g}</div>', "علّميها بهذا الترتيب، قاعدة كل أسبوع.", "ورقة القواعد")

    p2 = hdr("قَوَاعِدُ الْقِرَاءَةِ فِي وَرَقَةٍ وَاحِدَةٍ", "ورقة القواعد ٢ من ٢")
    g = ""
    g += box("«ال» مع الحروف القمرية: انطقي اللام",
        '<div class="ex big">ا ب ج ح خ ع غ ف ق ك م ه و ي</div><div class="ex">الْقَمَر · الْبَاب · الْكِتَاب · الْوَلَد</div><p>اللام عليها سكون. النشيد: <span class="ar" style="font-size:16pt">إِبْغِ حَجَّكَ وَخَفْ عَقِيمَهُ</span></p>')
    g += box("«ال» مع الحروف الشمسية: تجاوزي اللام",
        '<div class="ex big">ت ث د ذ ر ز س ش ص ض ط ظ ل ن</div><div class="ex">الشَّمْس · النَّهْر · الدَّرْس · السَّمَاء</div><p>اللام تُكتب ولا تُنطق؛ الحرف بعدها مشدد. انظري إلى اللام: لا شيء عليها ← لا تنطقيها.</p>')
    g += box("التاء المربوطة والألف المقصورة",
        '<div class="ex">مَدْرَسَة · شَجَرَة · فَاطِمَة &nbsp;|&nbsp; عَلَى · إِلَى · مُوسَى</div><p><b>ة</b> في الآخر فقط: «ت» عند الوصل، «هـ» عند الوقف. <b>ى</b> في الآخر فقط: تُقرأ ألفًا ممدودة. قارني <span class="ar" style="font-size:16pt">كِتَابُهُ</span> (هاء الضمير) و <span class="ar" style="font-size:16pt">فِي، عَلِي</span> (ياء بنقطتين).</p>')
    g += box("أشكال الهمزة الخمسة، صوت واحد",
        '<table><tr><th>أ</th><th>إ</th><th>ؤ</th><th>ئ</th><th>ء</th></tr><tr><td class="ar">أَحْمَد سَأَلَ</td><td class="ar">إِلَى إِنَّ</td><td class="ar">سُؤَال</td><td class="ar">بِئْر سَائِل</td><td class="ar">مَاء شَيْء</td></tr></table>'
        '<p>اقرئي الحركة التي عليها. أيّ كرسي تركب قاعدةُ إملاء تأتي لاحقًا. <span class="ar" style="font-size:16pt">آ</span> = همزة + ألف مد: <span class="ar" style="font-size:16pt">آدَم، قُرْآن</span></p>')
    g += box("قراءة الجمل",
        '<div class="ex">ذَهَبَ الْوَلَدُ إِلَى الْمَدْرَسَةِ.</div><p><b>الوقف</b> في الآخر: تسقط الحركة الأخيرة (ة ← «هـ»، تنوين الفتح ← ألف ممدودة: <span class="ar" style="font-size:16pt">قَلَمًا</span> = «قَلَمَا»).<br><b>«ال» بعد كلمة</b> تسقط همزتها: <span class="ar" style="font-size:16pt">فِي الْبَيْتِ</span> = «فِلْبَيْت».<br>ألف ساكتة بعد واو الجماعة: <span class="ar" style="font-size:16pt">كَتَبُوا</span>. الألف الصغيرة = مد: <span class="ar" style="font-size:16pt">هَٰذَا، لَٰكِنْ</span>.<br>الترقيم: ، ؟ . &nbsp; الأرقام: <span class="ar" style="font-size:16pt">٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩</span></p>')
    g += box("كلمات صغيرة ستراها في كل مكان",
        '<div class="ex">مِنْ · عَنْ · فِي · إِلَى · عَلَى · مَعَ · هَلْ · لَمْ · لَنْ · قَدْ · لَا · مَا · يَا<br>أَنَا · أَنْتَ · أَنْتِ · هُوَ · هِيَ · نَحْنُ · هُمْ · هَذَا · هَذِهِ<br>مَنْ · مَاذَا · أَيْنَ · كَيْفَ · مَتَى · كَمْ · نَعَمْ</div>')
    page2 = page(p2 + f'<div class="grid">{g}</div>', "الترتيب: الاتصال ← المد ← السكون ← التنوين ← الشدة ← «ال» ← النهايات ← الجمل.", "ورقة القواعد")
    return page1 + page2

# ---------------- الدليل (فصول ماركداون) ----------------
GUIDE_CSS = FONT_CSS + """
@page { size: Letter portrait; margin: 0.6in 0.65in; }
body { font-family: "Amiri", serif; color:#222; font-size: 12.5pt; line-height: 1.7; margin:0; direction: rtl; text-align: right; }
.chapter { page-break-before: always; }
.cover { height: 9.4in; display:flex; flex-direction:column; justify-content:center; text-align:center; page-break-after: always; }
.cover h1 { font-size: 32pt; margin: 0 0 10px; border: 0; }
.cover p { font-size: 14pt; color:#555; margin: 4px 0; }
.cover .toc { margin-top: 30px; text-align:right; display:inline-block; font-size: 13pt; line-height: 2; }
h1 { font-size: 22pt; border-bottom: 3px solid #222; padding-bottom: 4px; margin: 0 0 10px; }
h2 { font-size: 16pt; margin: 16px 0 6px; border-bottom: 1px solid #bbb; padding-bottom: 2px; page-break-after: avoid; }
h3 { font-size: 13.5pt; margin: 12px 0 4px; page-break-after: avoid; }
p { margin: 4px 0 6px; }
ul, ol { margin: 2px 0 6px; padding-right: 22px; padding-left: 0; }
li { margin-bottom: 2px; }
table { border-collapse: collapse; width: 100%; margin: 6px 0 10px; font-size: 11pt; }
th, td { border: 1px solid #999; padding: 3px 6px; vertical-align: top; text-align: right; }
th { background: #eee; }
tr { page-break-inside: avoid; }
code { font-family: "Amiri", serif; font-size: 11pt; background:#f2f2f2; padding: 0 3px; }
hr { border: 0; border-top: 1px solid #ccc; margin: 12px 0; }
a { color: #222; text-decoration: none; }
"""
CHAPTERS = ["README.md", "01-قواعد-القراءة.md", "02-طريقة-التعليم.md", "03-خطة-اثني-عشر-أسبوعا.md", "04-بنك-الأنشطة.md", "05-متابعة-التقدم.md"]

def md_to_html(path):
    text = pathlib.Path(path).read_text()
    text = re.sub(r'\[([^\]]+)\]\((?:\d\d-[^)]+\.md|README\.md|printables/[^)]+)\)', r'\1', text)
    text = text.replace("- [ ] ", "- ☐ ")
    return markdown.markdown(text, extensions=["tables", "sane_lists"])

def guide_html():
    cover = """<div class="cover"><h1>الْقِرَاءَةُ وَالْكِتَابَةُ بِالْعَرَبِيَّةِ فِي الْبَيْتِ</h1>
    <p>لطفلة تعرف الحروف بالتشكيل ومستعدة لقراءة الكلمات وكتابتها</p>
    <p>قاعدة واحدة في الأسبوع · ٢٥ دقيقة في اليوم · ١٢ أسبوعًا</p>
    <div class="toc">١. نظرة عامة والقواعد الذهبية<br>٢. قواعد القراءة بترتيب التعليم<br>٣. طريقة التعليم: القراءة، الكتابة، الإملاء<br>
    ٤. خطة الاثني عشر أسبوعًا<br>٥. بنك الأنشطة (٣٥ لعبة)<br>٦. متابعة التقدم<br><span style="color:#777">ثم: صفحات القراءة، صفحات الكتابة، ورقة القواعد</span></div></div>"""
    return cover + "".join(f'<div class="chapter">{md_to_html(ROOT / c)}</div>' for c in CHAPTERS)

def doc(body, css, title):
    return f"<!doctype html><html lang='ar' dir='rtl'><head><meta charset='utf-8'><title>{title}</title><style>{css}</style></head><body>{body}</body></html>"

if __name__ == "__main__":
    (HERE / "صفحات-القراءة.html").write_text(doc(reading_html(), PAGE_CSS, "صفحات القراءة"))
    (HERE / "صفحات-الكتابة.html").write_text(doc(writing_html(), PAGE_CSS, "صفحات الكتابة"))
    (HERE / "ورقة-القواعد.html").write_text(doc(rules_html(), PAGE_CSS, "ورقة القواعد"))
    if markdown:
        (HERE / "الدليل.html").write_text(doc(guide_html(), GUIDE_CSS, "الدليل"))
    else:
        print("حزمة markdown غير مثبتة: لم يُبنَ الدليل")
    print("تم إنشاء ملفات HTML")
