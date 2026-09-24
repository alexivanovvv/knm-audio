#!/usr/bin/env python3
"""Local dev server: serves this folder + a POST /__deploy endpoint that
runs `netlify deploy --prod --dir=.` so the on-page Deploy button can
trigger a real production deploy on demand.

Also emulates the /api/progress Netlify Function (T-10, PIN sync) with a
local JSON-file store under .local-blobs/, so PIN sync can be tested on
localhost before a real deploy. The real backend (netlify/functions/progress.js)
uses Netlify Blobs instead — same key/value shape, different storage."""
import http.server
import json
import re
import subprocess
import urllib.parse
from pathlib import Path

PORT = 8765
BLOBS_DIR = Path(__file__).parent / ".local-blobs"
KEY_RE = re.compile(r"^[a-f0-9]{16,128}$")


class Handler(http.server.SimpleHTTPRequestHandler):
    def _json(self, status, obj):
        body = json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/progress":
            key = urllib.parse.parse_qs(parsed.query).get("key", [""])[0]
            if not KEY_RE.match(key):
                self._json(400, {"error": "invalid key"})
                return
            f = BLOBS_DIR / f"{key}.json"
            if not f.exists():
                self.send_response(404)
                self.end_headers()
                return
            self._json(200, json.loads(f.read_text()))
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/progress":
            length = int(self.headers.get("Content-Length", 0))
            try:
                body = json.loads(self.rfile.read(length))
            except (ValueError, TypeError):
                self._json(400, {"error": "invalid json"})
                return
            key = body.get("key", "")
            payload = body.get("payload")
            if not KEY_RE.match(key) or payload is None:
                self._json(400, {"error": "missing key/payload"})
                return
            BLOBS_DIR.mkdir(exist_ok=True)
            (BLOBS_DIR / f"{key}.json").write_text(json.dumps(payload))
            self._json(200, {"ok": True})
            return
        if self.path != "/__deploy":
            self.send_response(404)
            self.end_headers()
            return
        result = subprocess.run(
            ["netlify", "deploy", "--prod", "--dir=."],
            capture_output=True, text=True, timeout=300,
        )
        ok = result.returncode == 0
        self._json(200 if ok else 500, {
            "ok": ok,
            "stdout": result.stdout[-4000:],
            "stderr": result.stderr[-4000:],
        })

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"http://localhost:{PORT}  (Deploy-knop in header post naar /__deploy)")
        httpd.serve_forever()
