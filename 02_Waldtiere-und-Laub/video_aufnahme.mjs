// Nimmt Video_Waldtiere-und-Laub_Quelle.html Bild für Bild mit Chrome auf und mischt die Erzählung dazu.
// Aufruf:  node video_aufnahme.mjs                → Video_Waldtiere-und-Laub.mp4
//          node video_aufnahme.mjs --stills 5 12.3 → Standbilder (Kontrolle) nach ./stills/
// Benötigt: puppeteer-core (npm i puppeteer-core), Google Chrome, ffmpeg
import puppeteer from 'puppeteer-core';
import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HIER = path.dirname(fileURLToPath(import.meta.url));
const FPS = 25;
const CHROME = process.env.CHROME || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const args = process.argv.slice(2);

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--hide-scrollbars'] });
const page = await browser.newPage();
await page.setViewport({ width: 1280, height: 720, deviceScaleFactor: 1 });
await page.goto('file://' + path.join(HIER, 'Video_Waldtiere-und-Laub_Quelle.html') + '?rec', { waitUntil: 'networkidle0' });
await page.waitForFunction('window.READY === true');
const total = await page.evaluate('window.TOTAL');

if (args[0] === '--stills') {
  mkdirSync(path.join(HIER, 'stills'), { recursive: true });
  for (const t of args.slice(1).map(Number)) {
    await page.evaluate(t => window.render(t), t);
    await page.screenshot({ path: path.join(HIER, 'stills', `t${t.toFixed(1).padStart(6, '0')}.jpg`), type: 'jpeg', quality: 80 });
  }
} else {
  const out = path.join(HIER, 'Video_Waldtiere-und-Laub.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-i', path.join(HIER, 'ton', 'erzaehlung.wav'),
    '-c:v', 'libx264', '-preset', 'slow', '-crf', '22', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11,aresample=44100', '-c:a', 'aac', '-b:a', '128k', '-shortest', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const n = Math.ceil(total * FPS);
  for (let i = 0; i < n; i++) {
    await page.evaluate(t => window.render(t), i / FPS);
    const buf = await page.screenshot({ type: 'jpeg', quality: 92 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 250 === 0) console.log(`${(i / FPS).toFixed(0)} / ${total.toFixed(0)} s`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log('fertig:', out);
}
await browser.close();
