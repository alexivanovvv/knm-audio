#!/usr/bin/env python3
"""Generate the short "Chapter X, task Y. <title>." clips played before a track
when "Announce chapter & task" is on (T-21). Same voice/model as the book itself:
ElevenLabs "George" (JBFqnCBsd6RMkjVDRZzb), eleven_flash_v2_5.

Titles are read from TASK_LABELS in index.html, so the clips always match the UI.
Output: Audio/announce/H{ch}T{t}.mp3. Existing clips are skipped (use --force).

    python3 tools/make_announcements.py [--force]
"""
import json, os, re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'Audio' / 'announce'
VOICE = 'JBFqnCBsd6RMkjVDRZzb'
MODEL = 'eleven_flash_v2_5'

def api_key():
    key = os.environ.get('ELEVENLABS_API_KEY')
    env = Path.home() / '.config/elevenlabs/.env'
    if not key and env.exists():
        m = re.search(r'^ELEVENLABS_API_KEY=(.+)$', env.read_text(), re.M)
        key = m and m.group(1).strip().strip('"\'')
    if not key: sys.exit('ELEVENLABS_API_KEY not set')
    return key

def labels():
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    block = html[html.index('const TASK_LABELS = {'):]
    block = block[:block.index('};')]
    return [(ch, t, a or b) for ch, t, a, b in
            re.findall(r"""H(\d+)T(\d+): (?:'((?:[^'\\]|\\.)*)'|"([^"]*)")""", block)]

def tts(text, key):
    req = urllib.request.Request(
        f'https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=mp3_44100_128',
        data=json.dumps({'text': text, 'model_id': MODEL}).encode(),
        headers={'xi-api-key': key, 'Content-Type': 'application/json', 'Accept': 'audio/mpeg'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def main():
    force = '--force' in sys.argv
    key = api_key()
    OUT.mkdir(parents=True, exist_ok=True)
    for ch, t, title in labels():
        dest = OUT / f'H{ch}T{t}.mp3'
        if dest.exists() and not force: continue
        title = title.replace(chr(92), '')
        text = f'Chapter {ch}, task {t}. {title}' + ('' if title[-1] in '.?!' else '.')
        dest.write_bytes(tts(text, key))
        print(dest.name, '—', text)

if __name__ == '__main__':
    main()
