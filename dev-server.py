#!/usr/bin/env python3
"""Local dev server: serves this folder + a POST /__deploy endpoint that
runs `netlify deploy --prod --dir=.` so the on-page Deploy button can
trigger a real production deploy on demand."""
import http.server
import json
import subprocess

PORT = 8765


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/__deploy":
            self.send_response(404)
            self.end_headers()
            return
        result = subprocess.run(
            ["netlify", "deploy", "--prod", "--dir=."],
            capture_output=True, text=True, timeout=300,
        )
        ok = result.returncode == 0
        body = json.dumps({
            "ok": ok,
            "stdout": result.stdout[-4000:],
            "stderr": result.stderr[-4000:],
        }).encode()
        self.send_response(200 if ok else 500)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


if __name__ == "__main__":
    with http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"http://localhost:{PORT}  (Deploy-knop in header post naar /__deploy)")
        httpd.serve_forever()
