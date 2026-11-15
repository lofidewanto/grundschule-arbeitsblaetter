import re, pathlib

HERE = pathlib.Path(__file__).parent
qr = (HERE / "qr.svg").read_text()
qr = re.sub(r'width="(\d+)" height="(\d+)"', lambda m: f'viewBox="0 0 {m[1]} {m[2]}" width="100%" height="100%"', qr, count=1)

VARIANTS = {
    "rechtshaender": dict(
        label="Rechtshänder",
        hand="linke",
        steps=[
            "Lege deine <b>linke Hand</b> flach auf das Blatt.",
            "Dein <b>Daumen zeigt nach rechts</b> &rarr;",
            "Genau in diese Richtung <b>schauen alle Zahlen</b>!",
        ],
        tmpl_hint="Für alle, die ihre Hand nicht auflegen mögen: Hand-Karte ausschneiden und neben das Heft legen.",
        tmpl_hand="linke Hand · Handfläche nach unten",
    ),
    "linkshaender": dict(
        label="Linkshänder",
        hand="rechte",
        steps=[
            "Lege deine <b>rechte Hand</b> mit dem <b>Handrücken</b> auf das Blatt.",
            "Dein <b>Daumen zeigt nach rechts</b> &rarr;",
            "Genau in diese Richtung <b>schauen alle Zahlen</b>!",
        ],
        tmpl_hint="Du magst deine Hand nicht umdrehen? Schneide die Hand-Schablone aus und lege sie auf dein Blatt.",
        tmpl_hand="rechte Hand · Handrücken nach unten",
    ),
}

def hand_svg(cls="hand", cut=False):
    stroke = 'stroke-dasharray="7 6"' if cut else ""
    return f"""
<svg class="{cls}" viewBox="0 0 220 230" aria-label="Hand, Daumen zeigt nach rechts">
  <g fill="var(--skin)" stroke="var(--ink)" stroke-width="3.5" stroke-linejoin="round" {stroke}>
    <path d="M40 120 L40 64 Q40 50 54 50 Q68 50 68 64 L68 110
             L68 30 Q68 16 82 16 Q96 16 96 30 L96 108
             L96 26 Q96 12 110 12 Q124 12 124 26 L124 110
             L124 44 Q124 30 138 30 Q152 30 152 44 L152 130
             L176 104 Q188 92 200 102 Q210 112 200 124 L160 182
             Q146 210 110 212 L80 212 Q40 210 40 168 Z"/>
  </g>
  <g fill="none" stroke="var(--ink)" stroke-width="2.5" stroke-linecap="round" opacity=".35">
    <path d="M68 110 L68 130"/><path d="M96 108 L96 128"/><path d="M124 110 L124 130"/>
  </g>
</svg>"""

DIGITS = "0123456789"
TASKS = [("3 + 4", 7), ("5 + 1", 6), ("2 + 7", 9), ("6 + 2", 8),
         ("9 − 4", 5), ("8 − 5", 3), ("7 − 5", 2), ("10 − 9", 1)]
# Zahlen-Detektiv: (Ziffer, gespiegelt?)
DETECTIVE = [("3", True), ("5", False), ("2", True), ("7", False), ("9", True),
             ("4", False), ("6", True), ("1", False), ("8", False), ("5", True), ("2", False), ("7", True)]

CSS = """
@page { size: A4; margin: 0; }
:root { --ink:#1f2937; --muted:#6b7280; --line:#cbd5e1; --accent:#2563eb; --accent-soft:#e8f0fe;
        --warm:#f59e0b; --warm-soft:#fff6e0; --ok:#16a34a; --skin:#fde7d4; --trace:#c7ced9; }
* { box-sizing: border-box; }
html, body { margin:0; background:#fff; color:var(--ink); font-family:'Andika', 'Comic Sans MS', sans-serif; }
.page { width:210mm; height:297mm; padding:9mm 13mm 8mm; position:relative; overflow:hidden; page-break-after:always; }
.page:last-child { page-break-after:auto; }
header.top { display:flex; justify-content:space-between; align-items:flex-end; gap:8mm; font-size:11pt; }
.field { flex:1; border-bottom:1.5px solid var(--ink); padding-bottom:1mm; }
.field span { color:var(--muted); }
.tag { font-size:9pt; font-weight:700; color:var(--accent); background:var(--accent-soft); border-radius:99px; padding:1mm 3.5mm; white-space:nowrap; }
h1 { font-size:21pt; margin:3.5mm 0 0.5mm; line-height:1.1; }
h1 small { display:block; font-size:11.5pt; font-weight:400; color:var(--muted); margin-top:1mm; }
.howto { display:grid; grid-template-columns: 28mm 1fr 27mm; gap:5mm; align-items:center;
         background:var(--warm-soft); border:2px solid var(--warm); border-radius:5mm; padding:3mm 5mm; margin-top:3mm; }
.howto .hand { width:24mm; height:auto; }
.handwrap { position:relative; }
.arrow { display:flex; align-items:center; gap:1.5mm; font-size:8.5pt; font-weight:700; color:var(--accent); margin-top:1mm; }
.arrow svg { width:20mm; height:5mm; }
.howto ol { margin:0; padding-left:6mm; font-size:12pt; line-height:1.45; }
.qr { text-align:center; font-size:8pt; color:var(--muted); line-height:1.25; }
.qr .code { width:22mm; height:22mm; margin:0 auto 1.5mm; background:#fff; padding:1.5mm; border-radius:2mm; }
h2 { font-size:12.5pt; margin:4mm 0 2mm; display:flex; align-items:center; gap:2.5mm; }
h2 .n { display:inline-grid; place-items:center; width:7mm; height:7mm; border-radius:50%; background:var(--accent); color:#fff; font-size:11pt; }
.trace { display:grid; grid-template-columns:1fr 1fr; gap:1.8mm 8mm; }
.trace .row { display:flex; gap:1.6mm; }
.box { width:11mm; height:11mm; border:1.5px solid var(--line); border-radius:1.5mm; display:grid; place-items:center;
       font-size:23pt; line-height:1; position:relative; }
.box::after { content:""; position:absolute; left:0; right:0; top:50%; border-top:1px dashed var(--line); }
.box.model { color:var(--trace); border-color:var(--trace); }
.box.model::before { content:"→"; position:absolute; top:-0.3mm; right:0.8mm; font-size:7pt; color:var(--accent); }
.tasks { display:grid; grid-template-columns:repeat(4, 1fr); gap:2mm 5mm; }
.task { display:flex; align-items:center; gap:2mm; font-size:14pt; }
.task .ans { width:10.5mm; height:10.5mm; border:1.5px solid var(--ink); border-radius:1.5mm; }
.task .chk { width:5.5mm; height:5.5mm; border:1.5px solid var(--ok); border-radius:50%; margin-left:auto; }
.detective { display:flex; justify-content:space-between; background:var(--accent-soft); border-radius:3mm; padding:1.5mm 4mm; }
.detective span { font-size:23pt; width:11mm; text-align:center; }
.detective .m { display:inline-block; transform:scaleX(-1); }
.code-strip { margin-top:4mm; border:2.5px solid var(--ok); border-radius:5mm; padding:3mm 5mm 3mm; }
.code-strip h3 { margin:0 0 2.5mm; font-size:13pt; color:var(--ok); }
.steps { display:grid; grid-template-columns:repeat(4, 1fr); gap:3mm; }
.step { text-align:center; font-size:9.5pt; line-height:1.3; position:relative; }
.step .ic { font-size:16pt; display:block; margin-bottom:1mm; }
.step:not(:last-child)::after { content:"➜"; position:absolute; right:-3mm; top:3mm; color:var(--ok); font-size:13pt; }
.step input { all:unset; }
.self { display:flex; gap:6mm; justify-content:center; margin-top:2.5mm; font-size:10.5pt; }
.self label { display:flex; align-items:center; gap:1.5mm; }
.self .c { width:5mm; height:5mm; border:1.5px solid var(--ink); border-radius:1mm; }
.solution { position:absolute; left:13mm; right:13mm; bottom:7mm; transform:rotate(180deg); font-size:8.5pt; color:var(--muted);
            text-align:center; border-top:1px dashed var(--line); padding-top:1.5mm; }
.footer { position:absolute; bottom:3mm; left:13mm; right:13mm; font-size:7pt; color:var(--muted); text-align:right; }
/* Seite 2 */
.tmpl h1 { margin-top:2mm; }
.cutcard { margin:6mm auto 0; width:150mm; border:2px dashed var(--muted); border-radius:6mm; padding:8mm; text-align:center; position:relative; }
.cutcard .scissor { position:absolute; top:-4.5mm; left:10mm; background:#fff; padding:0 2mm; font-size:14pt; }
.cutcard .hand { width:105mm; height:auto; }
.cutcard .big-arrow { display:flex; align-items:center; justify-content:center; gap:3mm; font-size:16pt; font-weight:700; color:var(--accent); margin-top:3mm; }
.cutcard .big-arrow svg { width:55mm; height:10mm; }
.cutcard .digits { font-size:24pt; letter-spacing:2.5mm; white-space:nowrap; margin-top:4mm; }
.cutcard .sub { color:var(--muted); font-size:10.5pt; margin-top:1mm; }
.tips { margin-top:8mm; font-size:11pt; line-height:1.55; background:var(--accent-soft); border-radius:4mm; padding:4mm 6mm; }
.tips h3 { margin:0 0 1.5mm; font-size:12pt; }
.tips ul { margin:0; padding-left:5mm; }
"""

ARROW = '<svg viewBox="0 0 100 20"><path d="M2 10 H88" stroke="currentColor" stroke-width="4" stroke-linecap="round"/><path d="M80 2 L96 10 L80 18" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def build(key, v):
    trace_rows = "".join(
        f'<div class="row"><div class="box model">{d}</div>' + '<div class="box"></div>' * 5 + "</div>"
        for d in "0516273849")  # links 0-4, rechts 5-9 (Grid füllt zeilenweise)
    tasks = "".join(f'<div class="task">{t} = <div class="ans"></div><div class="chk"></div></div>' for t, _ in TASKS)
    det = "".join(f'<span>{"<i class=m>" if m else ""}{d}{"</i>" if m else ""}</span>'.replace("<i class=m>", '<span class="m">').replace("</i>", "</span>")
                  for d, m in DETECTIVE)
    sol = "Lösungen Aufgabe 2: " + " · ".join(f"{t} = {r}" for t, r in TASKS) + \
          "  |  Aufgabe 3: falsch herum sind Nr. " + ", ".join(str(i + 1) for i, (_, m) in enumerate(DETECTIVE) if m)
    steps = "".join(f"<li>{s}</li>" for s in v["steps"])

    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>Daumen-Trick – {v['label']}</title>
<link href="https://fonts.googleapis.com/css2?family=Andika:wght@400;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>

<section class="page">
  <header class="top">
    <div class="field"><span>Name:</span></div>
    <div class="field" style="flex:.55"><span>Datum:</span></div>
    <div class="tag">✋ Version für {v['label']}</div>
  </header>
  <h1>Der Daumen-Trick 👍<small>So schreibe ich meine Zahlen richtig herum – und kontrolliere sie selbst.</small></h1>

  <div class="howto">
    <div class="handwrap">{hand_svg()}
      <div class="arrow">Daumen {ARROW}</div></div>
    <div><ol>{steps}</ol></div>
    <div class="qr"><div class="code">{qr}</div>Scannen &amp;<br>Video ansehen</div>
  </div>

  <h2><span class="n">1</span>Spure nach und schreibe die Zahl 5-mal.</h2>
  <div class="trace">{trace_rows}</div>

  <h2><span class="n">2</span>Rechne. Dann prüfe jede Zahl mit dem Daumen-Trick ✋ und male den Kreis grün.</h2>
  <div class="tasks">{tasks}</div>

  <h2><span class="n">3</span>Zahlen-Detektiv 🔍 Kreise alle Zahlen ein, die falsch herum stehen.</h2>
  <div class="detective">{det}</div>

  <div class="code-strip">
    <h3>✅ Mein Kontroll-Code – wenn ich fertig bin:</h3>
    <div class="steps">
      <div class="step"><span class="ic">✏️</span><b>1. Fertig</b><br>Alle Aufgaben geschrieben</div>
      <div class="step"><span class="ic">✋</span><b>2. Hand auflegen</b><br>{v['hand'].capitalize()} Hand aufs Blatt</div>
      <div class="step"><span class="ic">👉</span><b>3. Daumen prüfen</b><br>Schaut jede Zahl in Daumen-Richtung?</div>
      <div class="step"><span class="ic">🔁</span><b>4. Verbessern</b><br>Falsche Zahl durchstreichen, neu schreiben</div>
    </div>
    <div class="self"><label><span class="c"></span> Ich habe alle Zahlen geprüft.</label><label>So gut hat es geklappt: 😀 🙂 😐</label></div>
  </div>

  <div class="solution">{sol}</div>
  <div class="footer">Idee: Daumen-Trick nach @lernperspektive_ (Instagram)</div>
</section>

<section class="page tmpl">
  <header class="top"><div class="field"><span>Name:</span></div><div class="tag">✋ Version für {v['label']}</div></header>
  <h1>Meine Daumen-Karte ✂️<small>{v['tmpl_hint']}</small></h1>
  <div class="cutcard"><span class="scissor">✂</span>
    {hand_svg(cut=False)}
    <div class="big-arrow">Daumen {ARROW} Schreibrichtung</div>
    <div class="digits">0 1 2 3 4 5 6 7 8 9</div>
    <div class="sub">{v['tmpl_hand']} · so sehen die Zahlen richtig aus</div>
  </div>
  <div class="tips"><h3>Für Eltern &amp; Lehrkräfte</h3><ul>
    <li>Den Trick einmal gemeinsam mit dem Video (QR-Code auf Seite 1) anschauen.</li>
    <li>Das Kind kontrolliert nach jeder Aufgabe selbst – nicht verbessern, sondern fragen: „Was sagt dein Daumen?“</li>
    <li>Die Hilfe ist nur ein kurzer Anker: Meist prägt sich die Schreibrichtung schnell ein und die Karte wird bald nicht mehr gebraucht.</li>
    <li>Die Lösungen stehen auf dem Kopf unten auf Seite 1.</li>
  </ul></div>
  <div class="footer">Idee: Daumen-Trick nach @lernperspektive_ (Instagram)</div>
</section>
</body></html>"""

for key, v in VARIANTS.items():
    (HERE / f"AB_Daumen-Trick_{key}.html").write_text(build(key, v))
print("ok")
