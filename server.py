#!/usr/bin/env python
"""Espresso app server: static files + a tiny JSON sync API.

- Serves the app from this directory.
- GET  /api/state/<code>  -> the saved JSON blob for that sync code (or {}).
- POST /api/state/<code>  -> save the JSON blob for that code.
CORS is open so the GitHub Pages copy can sync to this server too.
Data is stored OUTSIDE the served folder, so it is never exposed as a static
file and never committed.

Run:  python server.py [port]        (port also from $PORT, default 8899)
"""
import json
import os
import re
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get("ESPRESSO_DATA_DIR") or (ROOT.parent / "espresso_data"))
DATA.mkdir(parents=True, exist_ok=True)
PORT = int(os.environ.get("PORT") or (sys.argv[1] if len(sys.argv) > 1 else 8899))
CODE_RE = re.compile(r"^[A-Za-z0-9_-]{3,40}$")
MAX_BODY = 512 * 1024  # 512 KB per blob is plenty


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)

    # --- helpers ---
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, status, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _code(self):
        m = re.match(r"^/api/state/([^/?]+)", self.path)
        return m.group(1) if m else None

    # --- routes ---
    def do_OPTIONS(self):
        self.send_response(204)
        if self.path.startswith("/api/"):
            self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith("/api/state/"):
            code = self._code()
            if not code or not CODE_RE.match(code):
                return self._json(400, {"error": "bad code"})
            f = DATA / (code + ".json")
            if f.exists():
                try:
                    return self._json(200, json.loads(f.read_text("utf-8")))
                except Exception:
                    return self._json(200, {})
            return self._json(200, {})
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/state/"):
            code = self._code()
            if not code or not CODE_RE.match(code):
                return self._json(400, {"error": "bad code"})
            n = int(self.headers.get("Content-Length") or 0)
            if n <= 0 or n > MAX_BODY:
                return self._json(413, {"error": "bad size"})
            try:
                obj = json.loads(self.rfile.read(n))
            except Exception:
                return self._json(400, {"error": "bad json"})
            (DATA / (code + ".json")).write_text(json.dumps(obj), "utf-8")
            return self._json(200, {"ok": True})
        self.send_response(404)
        self.end_headers()

    def log_message(self, *a):  # keep the journal quiet
        pass


if __name__ == "__main__":
    print(f"espresso server on :{PORT}  data={DATA}", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
