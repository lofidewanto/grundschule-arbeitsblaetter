#!/usr/bin/env python3
"""Erzeugt die Erzählstimme (edge-tts, Stimme de-DE-TanjaNeural) und die Zeitleiste
(timeline.js) für das Video „Wer braucht das Laub?“.

Aufruf:  python3 video_ton.py   (benötigt `edge-tts` und `ffmpeg`)
Ergebnis: ton/erzaehlung.wav und timeline.js
"""
import json, os, subprocess, wave

STIMME = "de-DE-TanjaNeural"
TEMPO = "-5%"           # etwas langsamer – für 7-Jährige
PAUSE_SATZ = 0.45       # Pause zwischen zwei Sätzen (s)
VOR = 0.5               # Pause am Szenenanfang (s)
NACH = 0.8              # Pause am Szenenende (s)

# (Szene, [Sätze]) – jeder Satz ist zugleich Untertitel
SKRIPT = [
 ("titel", ["Raschel, raschel! Wer braucht eigentlich das Laub im Wald?",
            "Komm mit auf einen Ausflug in den Herbstwald!"]),
 ("herbst", ["Im Herbst werden die Blätter an den Bäumen gelb, rot und braun.",
             "Dann fallen sie herunter.",
             "Bald liegt auf dem Waldboden eine dicke, bunte Laubdecke.",
             "Für viele Tiere ist dieses Laub ein richtiger Schatz!",
             "Schauen wir mal, wer es benutzt."]),
 ("igel1", ["Das ist der Igel.",
            "Im Herbst schnüffelt er mit seiner Nase im Laub.",
            "Darunter findet er Käfer, Würmer und Schnecken.",
            "So frisst er sich ein dickes Bäuchlein an."]),
 ("igel2", ["Dann sammelt der Igel viele Blätter und baut daraus ein Nest – unter einer Hecke oder in einem Laubhaufen.",
            "Darin rollt er sich zusammen und hält Winterschlaf, bis zum Frühling.",
            "Das Laub ist seine warme Bettdecke."]),
 ("maus1", ["Die Waldmaus ist klein und flink.",
            "Sie baut ihr Nest aus Laub, Moos und Gras – gut versteckt unter den Wurzeln.",
            "Das Laub hält sie schön warm, wenn es draußen kalt ist."]),
 ("maus2", ["Und das Laub schützt sie vor Feinden!",
            "Wenn die Eule oder der Fuchs kommt, huscht die Maus schnell unter die Blätter.",
            "Weg ist sie!"]),
 ("hoernchen1", ["Das Eichhörnchen sammelt im Herbst Nüsse und Eicheln.",
                 "Es vergräbt sie im Boden und deckt sie mit Laub zu.",
                 "So ist sein Wintervorrat gut versteckt.",
                 "Im Winter sucht es die Nüsse wieder.",
                 "Manche vergisst es – daraus wachsen dann neue Bäume!"]),
 ("hoernchen2", ["Oben im Baum baut das Eichhörnchen sein Nest.",
                 "Das heißt Kobel.",
                 "Innen polstert es den Kobel mit weichen Blättern, Moos und Gras.",
                 "Da ist es kuschelig warm."]),
 ("fuchs", ["Der Fuchs mag es gemütlich.",
            "An einem ruhigen Platz legt er sich gern auf trockenes Laub.",
            "Er rollt sich zusammen und deckt seine Nase mit dem buschigen Schwanz zu.",
            "Das trockene Laub ist wie eine weiche, warme Matratze."]),
 ("schwein1", ["Das Wildschwein hat eine starke Nase: den Rüssel.",
               "Damit wühlt es im Laub und in der Erde.",
               "Es findet Eicheln, Bucheckern, Würmer und Wurzeln.",
               "Lecker!"]),
 ("schwein2", ["Zum Schlafen scharrt das Wildschwein Laub und Zweige zu einem Haufen zusammen.",
               "So liegt es weich und nicht auf dem kalten Boden."]),
 ("dachs", ["Der Dachs wohnt in einem Bau unter der Erde.",
            "Er sammelt trockenes Laub, Gras und Moos.",
            "Das klemmt er zwischen Kinn und Vorderpfoten und schiebt es rückwärts in seinen Bau.",
            "Daraus macht er sich ein weiches Polster für seinen Schlafplatz.",
            "Im Winter schläft der Dachs dort ganz viel."]),
 ("rueckblick", ["Das haben wir gelernt:",
                 "Der Igel schläft im Laub.",
                 "Die Waldmaus versteckt sich darin.",
                 "Das Eichhörnchen versteckt sein Futter.",
                 "Der Fuchs ruht sich darauf aus.",
                 "Das Wildschwein sucht darin Futter.",
                 "Und der Dachs polstert damit seinen Bau."]),
 ("ende", ["Das Laub ist für die Tiere also ganz wichtig.",
           "Darum lassen wir das Laub im Wald liegen!",
           "Und vielleicht machst du im Garten einen Laubhaufen – für einen Igel.",
           "Tschüss und bis bald!"]),
]

HIER = os.path.dirname(os.path.abspath(__file__))
TON = os.path.join(HIER, "ton")
RATE = 24000


def tts(text, ziel):
    mp3 = ziel + ".mp3"
    if not os.path.exists(ziel):
        subprocess.run(["edge-tts", "-v", STIMME, f"--rate={TEMPO}", "-t", text, "--write-media", mp3], check=True)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp3, "-ac", "1", "-ar", str(RATE),
                        "-af", "silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                               "silenceremove=start_periods=1:start_threshold=-50dB,areverse", ziel], check=True)
        os.remove(mp3)
    with wave.open(ziel) as w:
        return w.readframes(w.getnframes()), w.getnframes() / RATE


def main():
    os.makedirs(TON, exist_ok=True)
    stille = lambda s: b"\x00\x00" * int(round(s * RATE))
    pcm, t, szenen = bytearray(), 0.0, []
    for sid, saetze in SKRIPT:
        start, lokal, info = t, VOR, []
        pcm += stille(VOR)
        for i, satz in enumerate(saetze):
            daten, d = tts(satz, os.path.join(TON, f"{sid}_{i}.wav"))
            info.append({"t": round(lokal, 3), "d": round(d, 3), "text": satz})
            pcm += daten
            lokal += d
            pause = PAUSE_SATZ if i < len(saetze) - 1 else NACH
            pcm += stille(pause)
            lokal += pause
        # Länge exakt aus den Samples, damit Bild und Ton nicht auseinanderlaufen
        t = len(pcm) / 2 / RATE
        szenen.append({"id": sid, "start": round(start, 3), "dur": round(t - start, 3), "sents": info})
    with wave.open(os.path.join(TON, "erzaehlung.wav"), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(RATE); w.writeframes(bytes(pcm))
    with open(os.path.join(HIER, "timeline.js"), "w", encoding="utf-8") as f:
        f.write("window.TL=" + json.dumps({"total": round(t, 3), "scenes": szenen}, ensure_ascii=False, indent=1) + ";\n")
    print(f"Gesamtlänge: {t:.1f} s ({t/60:.1f} min)")


if __name__ == "__main__":
    main()
