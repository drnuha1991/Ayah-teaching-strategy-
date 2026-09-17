# Generates weekly-plans.html and checklists.html (one printable page per section).
# Convert to PDF with Chromium headless (see build.sh).

WEEKS = [
 dict(n=1, title="A B C T M", theme="First sounds, first words",
  letters=["A","B","C","T","M"],
  sounds="A = /a/ apple · B = /b/ · C = /k/ · T = /t/ · M = /mmm/",
  words=["at","am","cat","mat","bat","tab","cab","tam"],
  reading=["1 new letter a day: show the book page, say the sound, do the hand motion.",
           "Pure sounds, no 'uh' (say /mmm/ not 'muh').",
           "Day 4–5: build CAT with magnets, slide finger, 'c-a-t… cat!' She copies.",
           "Robot talk all week: 'pass the c-u-p.'"],
  writing=["Playdough squeeze, tweezers + pom-poms, chalk lines.",
           "Strokes: big line down, line across (salt tray, easel).",
           "HWT: first stroke pages, crayon only."],
  math=["Touch-and-count snacks to 5: 'so how many?'",
        "Dot cards 1–3: 'don't count, just look!'",
        "Preschool Math at Home: first 3–4 activities."],
  play="Sound treasure hunt: hide 5 things starting with /m/ or /t/. Find, name, say the sound."),
 dict(n=2, title="S I R P", theme="Nine letters, lots of words",
  letters=["S","I","R","P"],
  sounds="S = /sss/ · I = /i/ igloo · R = /rrr/ · P = /p/",
  words=["sit","sip","tip","pit","rip","rat","sat","bit","rib","tap","map","cap","pat","rim","Sam","Tim"],
  reading=["1 new letter a day, review all 9 in a 2-minute flash race.",
           "Blend 3–5 words a day on the cookie sheet. Swap one letter: sat→sit→sip→tip.",
           "Ear game: 'say *pig* like a robot' (p-i-g)."],
  writing=["Circles and crosses in shaving cream / salt tray.",
           "Capitals L, F, E: build with sticks → chalk → wet-dry-try → 1 HWT row.",
           "Short crayons only (snap them) for finger grip."],
  math=["Line up 10 toys, count touching each. 'So there are ___.'",
        "Count backward from 5 while jumping.",
        "PMAH next activities."],
  play="Robot dinner: every request at one meal is in robot talk. She guesses the word."),
 dict(n=3, title="E N D H", theme="Short e and lots of families",
  letters=["E","N","D","H"],
  sounds="E = /e/ egg · N = /nnn/ · D = /d/ · H = /h/ (quiet puff)",
  words=["hen","pen","ten","den","net","bed","red","pet","met","hat","ham","had","hid","him","hit","dip","did","nap","man","can","pan","dad","sad","mad"],
  reading=["1 letter a day; 13 letters now. Sound review as 'trick the puppet'.",
           "Word families: -en (hen pen ten den), -at (hat cat mat bat), -an (man can pan).",
           "Short-e is the hardest to hear: use the 'egg' hand motion every time.",
           "She reads 3 words to Teddy each day."],
  writing=["Capitals H, T, I (all straight lines).",
           "Air-write huge letters with the whole arm, eyes closed.",
           "Cutting practice: fringe on a paper strip."],
  math=["Dice grab: roll, grab that many blocks, 'don't count, just look' (1–4).",
        "Two piles of grapes: 'which has more? Line them up to check.'",
        "PMAH comparing activities."],
  play="Letter-sound hopscotch: chalk 6 letters in squares. Jump and say the sound. 'Jump to the one that says /h/!'"),
 dict(n=4, title="O G F L", theme="Short o + check-in",
  letters=["O","G","F","L"],
  sounds="O = /o/ octopus · G = /g/ · F = /fff/ · L = /lll/",
  words=["dog","log","fog","hot","hop","top","mop","pot","cot","dot","not","got","fan","fat","fit","fin","fed","leg","lap","lip","lid","big","dig","pig","bag"],
  reading=["1 letter a day; 17 letters. Check-in on Friday: flash all 17, put any wobbly ones on the 'practice pile'.",
           "Blend 5 words a day, mix vowels: dog, fan, pig, bed, sit.",
           "Word swat: 6 words on the wall, say one, she swats and reads it."],
  writing=["Capitals U, C, O (curves are ready now).",
           "Bath crayons on the tub wall.",
           "Name: model A-Y-A-H, she traces, then tries."],
  math=["Numeral cards 1–5 matched to dot cards and fingers.",
        "Number hunt: find a '3' on the clock, remote, a book page.",
        "Count to 15 on the stairs."],
  play="Sound sorting bins: two bins, two letters. Sort toys by first sound (pig, pen, pot → P; dog, doll → D)."),
 dict(n=5, title="U J W K", theme="Short u + all five vowels",
  letters=["U","J","W","K"],
  sounds="U = /u/ umbrella · J = /j/ · W = /w/ · K = /k/",
  words=["sun","run","fun","bun","nut","cut","cup","up","bug","hug","mug","rug","jug","jam","jet","job","jog","wet","web","wig","win","wag","kit","kid"],
  reading=["1 letter a day; 21 letters. All five vowels known: sing the vowel song with hand signs.",
           "Word-family flip book for -ug and -un.",
           "Start tiny 2-word phrases on the cookie sheet: BIG DOG, WET CAT."],
  writing=["Capitals Q, G, S (S in the salt tray many times first).",
           "Rainbow letters: trace one big letter in 5 colors.",
           "1 HWT row per letter, then stop."],
  math=["Fingers: 'show me 3, hide 1, how many now?' (bonds of 3 and 4).",
        "'You have 2 crackers, I give you 1 more. Now?'",
        "Domino match: find two sides with the same dots."],
  play="Word-family flip book: staple cards so the first letter flips: _UG → bug, hug, mug, rug, jug."),
 dict(n=6, title="V X Y Z Q", theme="All 26 done + first Bob Book",
  letters=["V","X","Y","Z","Q"],
  sounds="V = /vvv/ · X = /ks/ (end of box) · Y = /y/ · Z = /zzz/ · Qu = /kw/",
  words=["van","vet","box","fox","six","wax","mix","yes","yet","yak","yum","zip","zap","quit","quiz"],
  reading=["Finish the alphabet. Friday: big review of all 26 sounds (2 minutes, race the timer).",
           "Blend 5 mixed words a day from the book's review/challenge list.",
           "Friday: Bob Books Set 1, Book 1 'Mat'. Finger under each word. Celebrate!"],
  writing=["Capitals J, D, P (frog-jump letters: start at the top, jump back up).",
           "Write her name on a card for the fridge.",
           "Tweezers + muffin tin counting (hands + math)."],
  math=["Five-frame with pom-poms: 'how many? how many empty?'",
        "Numeral cards 6–10 with dot cards.",
        "Subitize to 5 with finger flash."],
  play="Blending ramp: 3 letter cards beside a cardboard ramp. Roll a car past them faster and faster until the word 'pops out'."),
 dict(n=7, title="Review words", theme="Bob Books 1–3 + heart words",
  letters=["all","26"],
  sounds="Review any letters on the practice pile. Heart words: THE, A (we just know these by heart).",
  words=["the","a","cat","sat","mat","sam","rag","cab","hot","dog","fun","pig","wet","jam","fox","six","zip","bed"],
  reading=["Daily: 5 mixed words on the cookie sheet, then one Bob Book (new or reread).",
           "Reread yesterday's book first: it's a warm-up, not a test.",
           "Build a sentence with magnets: THE CAT SAT. Point and slide."],
  writing=["Capitals B, R, N.",
           "Draw a cat, you write CAT lightly, she traces it.",
           "Wet-dry-try any wobbly letters."],
  math=["Count to 20 while walking / on a hundred chart.",
        "Shape hunt: find 3 circles, 3 rectangles. Build a triangle with sticks: 'how many sides?'",
        "PMAH shape activities."],
  play="Secret word treasure hunt: 5 cards (BED, MAT, CUP, TUB, BOX). Each word she reads leads to the next clue. Sticker at the end."),
 dict(n=8, title="Sentences", theme="Bob Books 4–6 + I, IS",
  letters=["I","IS"],
  sounds="Heart words: I, IS. Review THE, A.",
  words=["I","is","the","a","big","dog","can","sit","hop","run","the cat is big","I can hop","the dog is wet"],
  reading=["Bob Books 4–6 (one new, one reread, each day).",
           "Sentence strips: THE PIG CAN HOP. She reads and acts it out.",
           "Whisper-shout reading: same 5 words whispered, shouted, squeaky."],
  writing=["Capitals M, K, A.",
           "Numerals 1, 2, 3 ('1 is a big line down').",
           "Sticker dots along a letter's path."],
  math=["5 pom-poms, hide some under a cup: 'how many are hiding?' (bonds of 5).",
        "Roll and add: two dice, take that many blocks, count the tower.",
        "Snack math: '2 apple slices and 3 more, how many?'"],
  play="Sentence strips: write 5 silly sentences (THE CAT CAN HOP). She reads one, then acts it out."),
 dict(n=9, title="Stories about me", theme="Bob Books 7–9 + TO, AND",
  letters=["TO","AND"],
  sounds="Heart words: TO, AND. Review THE, A, I, IS.",
  words=["to","and","the cat and the dog","I run to the bed","Ayah can hop","Ayah is 4"],
  reading=["Bob Books 7–9.",
           "Story cards about her: 'AYAH CAN RUN. AYAH IS 4.' She reads and keeps them in a 'my books' envelope.",
           "Progressive Phonics free books: you read black words, she reads red."],
  writing=["Capitals V, W, X.",
           "Numerals 4, 5.",
           "Label her drawings: DOG, SUN, MOM."],
  math=["'5 crackers, eat 2, how many left?' (taking away within 5).",
        "Countdown rocket: 5-4-3-2-1 blast off with fingers.",
        "'One less' with toy cars driving away."],
  play="Reading picnic: blanket, snacks, a pile of Bob Books. Every stuffed animal gets one page read to it."),
 dict(n=10, title="Label the house", theme="Bob Books 10–12",
  letters=["Set","1"],
  sounds="Finish Bob Books Set 1. Optional: start Set 2.",
  words=["bed","cup","pan","mat","box","tub","fan","rug","lid","pot"],
  reading=["Bob Books 10–12. Let her read a familiar one alone to Teddy while you 'cook'.",
           "Sticky notes with words on the real objects; she reads them all week.",
           "She 'teaches' you one word a day."],
  writing=["Capitals Y, Z. All 26 done!",
           "Numerals 6, 7.",
           "Alphabet poster: she writes a few letters a day."],
  math=["Bead / sticker patterns: red-blue-red-blue, then red-red-blue. She continues yours, then makes one for you.",
        "Line up spoon, fork, crayon: shortest to longest.",
        "Clap-stomp body patterns."],
  play="Label the house: 10 sticky notes with CVC words stuck on the real things (BED, CUP, PAN, TUB, BOX)."),
 dict(n=11, title="Little letters", theme="Lowercase begins + board games",
  letters=["a","b","c","t","m"],
  sounds="Same sounds, small letters. Match each lowercase magnet to its capital: A-a, B-b, C-c, T-t, M-m.",
  words=["cat","mat","bat","tab","cab","at","am","sit","sip","rat"],
  reading=["Lowercase, same groups as the book, 5 letters this week. Match capital ↔ lowercase magnets.",
           "Read the Week 1–2 words again in lowercase.",
           "Reread favorite Bob Books; try Set 2 if she wants."],
  writing=["Review any wobbly capitals (circle the best one on each row).",
           "Numerals 8, 9, 10.",
           "Write one whole word alone: CAT."],
  math=["Show '3 + 2' on cards with pom-poms under each number; count all. Just looking, no writing.",
        "Hundred chart: point and count to 30. Cover a number: 'which one is hiding?'",
        "Board game every day this week."],
  play="Board-game week: Count Your Chickens or Hi Ho! Cherry-O every day instead of a math activity."),
 dict(n=12, title="Celebration", theme="Check-in week, no new content",
  letters=["★"],
  sounds="Use the checklists: tick what is solid, note what needs one more week.",
  words=["Reread favorites","Make a 'books I can read' list","Read to a grandparent on video"],
  reading=["No new letters or words. Reread, relax, show off.",
           "Read one Bob Book to someone on a video call.",
           "She picks the game every day."],
  writing=["Write a card: I LOVE YOU. AYAH.",
           "That's the whole writing goal this week."],
  math=["Play every math game she loved. Ask her to teach YOU the rules.",
        "Explaining is the deepest learning."],
  play="Certificate day: make a paper certificate, she signs it, take a photo with her stack of Bob Books."),
]

CSS = """
@page { size: Letter portrait; margin: 0.45in 0.5in; }
* { box-sizing: border-box; }
body { font-family: "DejaVu Sans", Arial, Helvetica, sans-serif; color: #222; margin: 0; font-size: 10.2pt; line-height: 1.28; }
.page { page-break-after: always; height: 10.1in; display: flex; flex-direction: column; }
.page:last-child { page-break-after: auto; }
h1 { font-size: 20pt; margin: 0; letter-spacing: .5px; }
.head { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 3px solid #222; padding-bottom: 4px; margin-bottom: 8px; }
.head .sub { font-size: 11pt; color: #555; }
.head .date { font-size: 9pt; color: #555; }
.letters { display: flex; gap: 8px; margin: 4px 0 6px; align-items: center; }
.letters .box { width: 0.72in; height: 0.72in; border: 2.5px solid #222; border-radius: 8px; font-size: 30pt; font-weight: bold; display: flex; align-items: center; justify-content: center; }
.letters .box.small { font-size: 18pt; }
.letters .sounds { font-size: 9.5pt; color: #333; margin-left: 6px; }
.letters .sounds .note { font-size: 8pt; color: #777; display:block; margin-top:3px; }
.words { border: 1.5px dashed #888; border-radius: 6px; padding: 5px 8px; margin-bottom: 8px; font-size: 12pt; letter-spacing: .3px; }
.words b { font-size: 9pt; color: #555; letter-spacing: 0; margin-right: 6px; text-transform: uppercase; }
.grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; margin-bottom: 8px; }
.card { border: 1.5px solid #222; border-radius: 8px; padding: 6px 8px; }
.card h2 { font-size: 10.5pt; margin: 0 0 3px; text-transform: uppercase; letter-spacing: .6px; border-bottom: 1px solid #ccc; padding-bottom: 2px; }
.card ul { margin: 0; padding-left: 14px; }
.card li { margin-bottom: 2px; }
.play { border: 2px solid #222; border-radius: 8px; padding: 6px 8px; background: #f3f3f3; margin-bottom: 8px; }
.play b { text-transform: uppercase; letter-spacing: .6px; font-size: 9.5pt; }
table.days { width: 100%; border-collapse: collapse; margin-top: auto; }
table.days th, table.days td { border: 1.2px solid #222; padding: 3px 5px; text-align: center; font-size: 9.5pt; }
table.days th { background: #e8e8e8; }
table.days td.row { text-align: left; font-weight: bold; width: 1.55in; }
table.days td.row small { font-weight: normal; color: #666; display:block; font-size: 8pt; }
table.days td .cb { display:inline-block; width: 0.26in; height: 0.26in; border: 1.5px solid #222; border-radius: 4px; }
.foot { display:flex; justify-content: space-between; font-size: 8.5pt; color: #555; margin-top: 5px; }
.rule { font-weight: bold; color: #222; }
/* checklists */
.chk h1 { font-size: 22pt; }
.groups { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }
.group { border: 1.5px solid #222; border-radius: 8px; padding: 6px 8px; }
.group h2 { margin: 0 0 4px; font-size: 10pt; color: #555; text-transform: uppercase; }
.lrow { display:flex; align-items:center; gap: 8px; margin: 4px 0; }
.lrow .L { width: 0.5in; font-size: 22pt; font-weight: bold; text-align:center; }
.lrow .cb { width: 0.26in; height: 0.26in; border: 1.5px solid #222; border-radius: 4px; display:inline-block; }
.lrow .lbl { font-size: 8pt; color: #666; width: 0.6in; }
.wordgrid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; }
.wordgrid .w { border: 1.5px solid #222; border-radius: 6px; padding: 5px 4px; display:flex; align-items:center; gap:6px; font-size: 13pt; font-weight: bold; }
.wordgrid .w .cb { width: 0.24in; height: 0.24in; border: 1.5px solid #222; border-radius: 4px; flex: none; }
.wordgrid .w.blank { border-style: dashed; color:#aaa; font-weight: normal; font-size: 9pt; }
.list li { margin-bottom: 6px; list-style: none; display:flex; align-items:center; gap:8px; font-size: 11pt; }
.list .cb { width: 0.28in; height: 0.28in; border: 1.5px solid #222; border-radius: 4px; display:inline-block; flex:none; }
.list { padding-left: 0; margin: 0; }
.two { display:grid; grid-template-columns: 1fr 1fr; gap: 14px; }
table.stick { width:100%; border-collapse: collapse; margin-top: 8px; }
table.stick th, table.stick td { border: 1.5px solid #222; text-align:center; }
table.stick th { background:#e8e8e8; padding: 6px; font-size: 11pt; }
table.stick td { height: 0.95in; font-size: 11pt; font-weight: bold; }
table.stick td.row { width: 1.2in; }
.big { font-size: 12pt; }
.caps { display:grid; grid-template-columns: repeat(7, 1fr); gap: 6px; }
.caps .c { border:1.5px solid #222; border-radius: 6px; height: 0.62in; display:flex; align-items:center; justify-content:space-between; padding: 0 6px; font-size: 20pt; font-weight:bold; }
.caps .c .cb { width:0.24in; height:0.24in; border:1.5px solid #222; border-radius:4px; }
.hint { color:#666; font-size: 9pt; margin: 2px 0 8px; }
"""

def cb(): return '<span class="cb"></span>'

def week_page(w):
    boxes = "".join(f'<div class="box{" small" if len(l)>1 else ""}">{l}</div>' for l in w["letters"])
    note = ""
    if 1 <= w["n"] <= 6:
        note = '<span class="note">Check against your ABC See, Hear, Do book. If its next group differs, use the book\'s letters and words.</span>'
    words = " &nbsp;·&nbsp; ".join(w["words"])
    lis = lambda items: "".join(f"<li>{i}</li>" for i in items)
    rows = [("Sounds &amp; words","10–15 min"),("Move!","5 min"),("Hands &amp; writing","10 min"),("Math game","10 min"),("Story time","15–20 min")]
    trs = "".join(f'<tr><td class="row">{r}<small>{m}</small></td>' + "".join(f"<td>{cb()}</td>" for _ in range(5)) + "</tr>" for r,m in rows)
    return f"""
<div class="page">
  <div class="head">
    <div><h1>Week {w["n"]}: {w["title"]}</h1><div class="sub">{w["theme"]}</div></div>
    <div class="date">Ayah's plan &nbsp;·&nbsp; week of ____________</div>
  </div>
  <div class="letters">{boxes}<div class="sounds">{w["sounds"]}{note}</div></div>
  <div class="words"><b>Words this week</b>{words}</div>
  <div class="grid">
    <div class="card"><h2>Sounds &amp; reading</h2><ul>{lis(w["reading"])}</ul></div>
    <div class="card"><h2>Hands &amp; writing</h2><ul>{lis(w["writing"])}</ul></div>
    <div class="card"><h2>Math</h2><ul>{lis(w["math"])}</ul></div>
  </div>
  <div class="play"><b>Play of the week:</b> {w["play"]}</div>
  <table class="days">
    <tr><th></th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th></tr>
    {trs}
  </table>
  <div class="foot"><span class="rule">Stop before she's done. Bored = switch the game, not the goal.</span><span>Sat + Sun: off. Just story time.</span></div>
</div>"""

def blank_week():
    rows = [("Sounds &amp; words","10–15 min"),("Move!","5 min"),("Hands &amp; writing","10 min"),("Math game","10 min"),("Story time","15–20 min")]
    trs = "".join(f'<tr><td class="row">{r}<small>{m}</small></td>' + "".join(f"<td>{cb()}</td>" for _ in range(5)) + "</tr>" for r,m in rows)
    boxes = "".join('<div class="box"></div>' for _ in range(5))
    return f"""
<div class="page">
  <div class="head">
    <div><h1>Week ____: ______________________</h1><div class="sub">Blank week (repeat a week, or plan your own)</div></div>
    <div class="date">Ayah's plan &nbsp;·&nbsp; week of ____________</div>
  </div>
  <div class="letters">{boxes}<div class="sounds">Sounds: _______________________________________<span class="note">Write the letters from the book's next group in the boxes.</span></div></div>
  <div class="words"><b>Words this week</b><br><br></div>
  <div class="grid">
    <div class="card" style="min-height:1.9in"><h2>Sounds &amp; reading</h2></div>
    <div class="card"><h2>Hands &amp; writing</h2></div>
    <div class="card"><h2>Math</h2></div>
  </div>
  <div class="play" style="min-height:0.6in"><b>Play of the week:</b></div>
  <table class="days">
    <tr><th></th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th></tr>
    {trs}
  </table>
  <div class="foot"><span class="rule">Stop before she's done. Bored = switch the game, not the goal.</span><span>Sat + Sun: off. Just story time.</span></div>
</div>"""

def checklists():
    groups = [("Week 1","ABCTM"),("Week 2","SIRP"),("Week 3","ENDH"),("Week 4","OGFL"),("Week 5","UJWK"),("Week 6","VXYZQ")]
    g = ""
    for name, letters in groups:
        rows = "".join(f'<div class="lrow"><div class="L">{L}</div>{cb()}<span class="lbl">says sound</span>{cb()}<span class="lbl">writes it</span></div>' for L in letters)
        g += f'<div class="group"><h2>{name}</h2>{rows}</div>'
    p1 = f"""<div class="page chk">
  <div class="head"><div><h1>Ayah's Letter Sounds</h1><div class="sub">Tick "says sound" when she says it fast, with no "uh". Tick "writes it" when she writes the capital.</div></div></div>
  <div class="groups">{g}</div>
  <div class="hint" style="margin-top:8px">Practice pile (letters that keep slipping): ______________________________________________</div>
</div>"""
    allwords = []
    for w in WEEKS[:7]:
        for x in w["words"]:
            if " " not in x and x not in allwords: allwords.append(x)
    cells = "".join(f'<div class="w">{cb()}{x}</div>' for x in allwords)
    cells += "".join('<div class="w blank">'+cb()+'my word</div>' for _ in range(6))
    p2 = f"""<div class="page chk">
  <div class="head"><div><h1>Words I Can Read</h1><div class="sub">Tick a word when Ayah reads it by herself. Reading it 3 times on 3 days = a star.</div></div></div>
  <div class="wordgrid">{cells}</div>
</div>"""
    bob = "".join(f'<li>{cb()} Bob Books Set 1, Book {i}</li>' for i in range(1,13))
    p3 = f"""<div class="page chk">
  <div class="head"><div><h1>Books I Can Read</h1><div class="sub">Tick when she reads the whole book (with a little help is fine). Star when she reads it alone.</div></div></div>
  <div class="two">
    <div><ul class="list">{bob}</ul></div>
    <div><ul class="list">
      <li>{cb()} Heart word: THE</li><li>{cb()} Heart word: A</li><li>{cb()} Heart word: I</li><li>{cb()} Heart word: IS</li><li>{cb()} Heart word: TO</li><li>{cb()} Heart word: AND</li>
      <li>{cb()} Read a story card about me</li>
      <li>{cb()} Read a book alone to Teddy</li>
      <li>{cb()} Read a sentence: THE CAT SAT</li>
      <li>{cb()} Read to someone on video</li>
      <li>{cb()} Bob Books Set 2, Book 1</li><li>{cb()} Bob Books Set 2, Book 2</li>
    </ul></div>
  </div>
  <div class="hint" style="margin-top:14px">Other books I read: ____________________________________________________________________<br><br>______________________________________________________________________________________</div>
</div>"""
    order = "LFEHTIUCOQGSJDPBRNMKAVWXYZ"
    caps = "".join(f'<div class="c"><span>{L}</span>{cb()}</div>' for L in order)
    nums = "".join(f'<div class="c"><span>{n}</span>{cb()}</div>' for n in range(1,11))
    p4 = f"""<div class="page chk">
  <div class="head"><div><h1>Ayah Can Write</h1><div class="sub">Capitals in the easy-to-hard order (Handwriting Without Tears). Tick when she writes it without a model.</div></div></div>
  <div class="hint">Get-ready strokes</div>
  <ul class="list two" style="margin-bottom:10px">
    <li>{cb()} line down |</li><li>{cb()} line across —</li><li>{cb()} circle O</li><li>{cb()} cross +</li><li>{cb()} square</li><li>{cb()} X and diagonals</li>
  </ul>
  <div class="hint">Capital letters</div>
  <div class="caps">{caps}</div>
  <div class="hint" style="margin-top:10px">Numbers</div>
  <div class="caps">{nums}</div>
  <ul class="list" style="margin-top:12px">
    <li>{cb()} Holds the crayon with fingers, not a fist</li>
    <li>{cb()} Writes her name: AYAH</li>
    <li>{cb()} Writes a word under a drawing (CAT)</li>
    <li>{cb()} Writes a card: I LOVE YOU</li>
  </ul>
</div>"""
    items = ["Counts 10 things, touching each one once","Says 'so there are ___' after counting","Counts out loud to 20","Counts out loud to 30",
             "Sees 1, 2, 3 without counting","Sees 4 and 5 without counting","Knows the numbers 1–5","Knows the numbers 6–10 and 0",
             "Matches a number to that many things","More, fewer, or the same?","One more / one less","Hidden pom-poms: how many under the cup? (5)",
             "Adds within 5 with toys or fingers","Takes away within 5 with toys","Names circle, square, triangle, rectangle","Copies and continues a pattern (red-blue-red-blue)",
             "Puts 3 things in order: short → long","Plays a board game to the end, taking turns"]
    half = (len(items)+1)//2
    col = lambda xs: "".join(f'<li>{cb()} {x}</li>' for x in xs)
    p5 = f"""<div class="page chk">
  <div class="head"><div><h1>Ayah's Math</h1><div class="sub">Tick when it's easy and she does it most of the time, not just once.</div></div></div>
  <div class="two"><ul class="list">{col(items[:half])}</ul><ul class="list">{col(items[half:])}</ul></div>
  <div class="hint" style="margin-top:14px">Favorite math games: ____________________________________________________________________</div>
</div>"""
    trs = "".join(f'<tr><td class="row">Week {i}</td>' + "".join("<td></td>" for _ in range(5)) + "</tr>" for i in range(1,5))
    p6 = f"""<div class="page chk">
  <div class="head"><div><h1>Our Learning Chart</h1><div class="sub big">Month ______ &nbsp;·&nbsp; One sticker for each day we played and learned. Any day with story time counts!</div></div></div>
  <table class="stick">
    <tr><th></th><th>Mon</th><th>Tue</th><th>Wed</th><th>Thu</th><th>Fri</th></tr>{trs}
  </table>
  <div class="hint big" style="margin-top:16px">When the chart is full we will: ________________________________________________________</div>
  <div class="hint big" style="margin-top:8px">Books we read together this month: _______________________________________________________<br><br>______________________________________________________________________________________</div>
</div>"""
    return p1+p2+p3+p4+p5+p6

html = lambda body, title: f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>"
open("weekly-plans.html","w").write(html("".join(week_page(w) for w in WEEKS) + blank_week(), "Ayah weekly plans"))
open("checklists.html","w").write(html(checklists(), "Ayah checklists"))
print("html written")
