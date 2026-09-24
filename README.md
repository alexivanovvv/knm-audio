# Welkom in Nederland — Audioboek

Installeerbare webapp (PWA) die de KNM-samenvatting "Welkom in Nederland" als
audioboek afspeelt: 7 hoofdstukken, 36 taken. De interface toont Nederlandstalige
en Engelstalige labels naast elkaar, en Nederlandse kernbegrippen/eigennamen
worden apart uitgesproken van de Engelse tekst.

Alle 36 taken gebruiken de ElevenLabs Flash-stem "George"
(`eleven_flash_v2_5`, voice-id `JBFqnCBsd6RMkjVDRZzb`). De Engelse tekst en de
Nederlandse kernbegrippen tussen `[haakjes]` worden apart gesynthetiseerd per
segment en met ffmpeg aan elkaar geplakt, zodat de stem en intonatie
consistent zijn door het hele boek heen. Eerder gebruikten 25 van de 36 taken
de gratis neurale stemmen via edge-tts — zie `BACKLOG.md` (T-02) voor de
geschiedenis van die overzetting.

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
- Ondertitels/lyrics-modus (CC-knop): meelezen met gesynchroniseerde
  regels, tik op een regel om te spoelen, `[NL termen]` gemarkeerd.
  23/36 taken hebben woord-nauwkeurige forced-alignment timing; de
  overige 13 gebruiken een schatting (proportioneel aan de tekstlengte)
  met een duidelijke melding in de drawer — zie `BACKLOG.md`, T-05.
- Service worker: audiofragmenten worden na eerste keer afspelen offline
  gecachet

## Structuur

```
index.html               — app shell + speler
manifest.webmanifest      — PWA-manifest (iconen, naam, kleuren)
sw.js                     — service worker (offline caching)
icons/                    — app-iconen (32/180/192/512, incl. maskable)
social/                   — og-image.png (1200×630, link previews) en
                            cover-1080.png (vierkant, algemeen gebruik)
Audio/                    — 36 mp3's, één per Taak
```

## Merk / iconografie

Het icoon combineert een sereif "NL"-wordmark met een geluidsgolf in de
Nederlandse driekleur — leest als "Nederlands, audio" op elk formaat, van
32px favicon tot 512px app-icoon. Dezelfde compositie komt terug in de
social-preview-afbeelding (`social/og-image.png`, gebruikt door
`og:image`/`twitter:image` in `index.html`) en in `social/cover-1080.png`
voor vierkant gebruik (bijv. delen in chats). Kleuren volgen het bestaande
oranje accent (`--accent`) uit de app zelf.

## Herbouwen vanuit de bron

De audiofragmenten zijn gegenereerd met een Python-script dat de brontekst
("Welkom in Nederland — Voiceover Script (EN-NL)") parseert: de tekst wordt
gesplitst op `[Nederlandse term]`-grenzen in afwisselende EN/NL-segmenten.
Elk segment wordt apart gesynthetiseerd via de ElevenLabs TTS-API (stem
George, `eleven_flash_v2_5`) en met ffmpeg aan elkaar geplakt tot één mp3 per
taak.
