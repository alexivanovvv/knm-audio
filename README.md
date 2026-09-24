# Welkom in Nederland — Audioboek

Installeerbare webapp (PWA) die de KNM-samenvatting "Welkom in Nederland" als
audioboek afspeelt: 7 hoofdstukken, 36 taken. De interface toont Nederlandstalige
en Engelstalige labels naast elkaar, en Nederlandse kernbegrippen/eigennamen
worden apart uitgesproken van de Engelse tekst.

Momenteel gebruiken 11 van de 36 taken (hoofdstuk 1, hoofdstuk 2 en H5T5)
ElevenLabs Flash-stemmen; de overige 25 taken zijn nog gegenereerd met de
gratis neurale stemmen via [edge-tts](https://github.com/rany2/edge-tts)
(`nl-NL-MaartenNeural` voor Nederlandse termen, `en-US-GuyNeural` voor de
Engelse tekst). Zie `BACKLOG.md` (T-02) voor de status van het overzetten
van de resterende taken naar ElevenLabs.

## Gebruiken

Open `index.html` in de browser (lokaal of via GitHub Pages). Op iOS: open de
site in Safari, tik op **Deel → Zet op beginscherm** om de app als standalone
app te installeren.

## Functies

- Inhoudsopgave per hoofdstuk, klik op een taak om direct af te spelen
- Doorspelen naar de volgende taak (audioboek-modus)
- Voortgang wordt onthouden (localStorage) — "Verder luisteren"-kaart bij
  terugkeer
- Afspeelsnelheid (0.75× tot 2×), ±15s spoelen, toetsenbord-shortcuts
  (spatie/pijltjes)
- Service worker: audiofragmenten worden na eerste keer afspelen offline
  gecachet

## Structuur

```
index.html               — app shell + speler
manifest.webmanifest      — PWA-manifest (iconen, naam, kleuren)
sw.js                     — service worker (offline caching)
icons/                    — app-iconen (180/192/512, incl. maskable)
Audio/                    — 36 mp3's, één per Taak
```

## Herbouwen vanuit de bron

De audiofragmenten zijn gegenereerd met een Python-script dat de brontekst
("Welkom in Nederland — Summary with Key Terms (EN)") parseert: **vetgedrukte**
Nederlandse termen plus een lijst met bekende Nederlandse eigennamen
(provincies, steden, instanties) gaan naar de Nederlandse stem, de rest naar
de Engelse stem. Segmenten worden apart gesynthetiseerd met edge-tts en aan
elkaar geplakt met ffmpeg.
