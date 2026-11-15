# Grundschul-Arbeitsblätter ✏️

Arbeitsblätter zum Ausdrucken und Erklärvideos für die Grundschule.

🌐 **Webseite:** https://lofidewanto.github.io/grundschule-arbeitsblaetter/

## Inhalt

### 01 · Der Daumen-Trick 👍

Kinder lernen, Zahlen richtig herum zu schreiben, und kontrollieren sie selbst: Legt man die Hand so auf das Blatt, dass der Daumen nach rechts zeigt, „schauen“ alle Zahlen in diese Richtung.

| Datei | Beschreibung |
|---|---|
| [AB_Daumen-Trick_rechtshaender.pdf](01_Daumen-Trick/AB_Daumen-Trick_rechtshaender.pdf) | Arbeitsblatt für Rechtshänder (2 Seiten, inkl. Daumen-Karte zum Ausschneiden) |
| [AB_Daumen-Trick_linkshaender.pdf](01_Daumen-Trick/AB_Daumen-Trick_linkshaender.pdf) | Arbeitsblatt für Linkshänder (2 Seiten, inkl. Daumen-Karte zum Ausschneiden) |
| [Erklaerung_Daumen-Trick_Bildergeschichte.pdf](01_Daumen-Trick/Erklaerung_Daumen-Trick_Bildergeschichte.pdf) | Erklärung als Bildergeschichte |
| [Video_Daumen-Trick_Comic.mp4](01_Daumen-Trick/Video_Daumen-Trick_Comic.mp4) | Comic-Erklärvideo |

🎬 **Video online ansehen:** https://lofidewanto.github.io/grundschule-arbeitsblaetter/daumen-trick/
Der QR-Code auf den Arbeitsblättern führt direkt zu dieser Seite.

## Arbeitsblätter neu erzeugen

Die Arbeitsblätter werden aus [`01_Daumen-Trick/build.py`](01_Daumen-Trick/build.py) als HTML erzeugt und mit Chrome als PDF gedruckt. Der QR-Code liegt in `01_Daumen-Trick/qr.svg`.

```bash
cd 01_Daumen-Trick
python3 build.py
for v in rechtshaender linkshaender; do
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
    --no-pdf-header-footer --virtual-time-budget=8000 \
    --print-to-pdf="$PWD/AB_Daumen-Trick_$v.pdf" "file://$PWD/AB_Daumen-Trick_$v.html"
done
```

QR-Code neu erzeugen (z. B. mit [segno](https://pypi.org/project/segno/)):

```bash
python3 -c "import segno; segno.make('https://lofidewanto.github.io/grundschule-arbeitsblaetter/daumen-trick/', error='m').save('qr.svg', border=0, dark='#1f2937', xmldecl=False)"
```

## Danksagung

Idee: Daumen-Trick nach [@lernperspektive_](https://www.instagram.com/lernperspektive_/) (Instagram).
