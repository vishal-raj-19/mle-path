#!/usr/bin/env python3
"""MLE Path local server.

Serves the planner on http://127.0.0.1:8765 and saves your progress to
progress.json in this folder (with a daily backup in backups/).
Standard library only — no installs needed. Stop with Ctrl+C.
"""
import datetime
import http.server
import json
import os
import shutil
import socketserver
import sys
import threading
import webbrowser

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "progress.json")
BACKUPS = os.path.join(ROOT, "backups")
PORT = int(os.environ.get("MLE_PATH_PORT", "8765"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def _send_json(self, code, body: bytes):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/state":
            body = b"{}"
            if os.path.exists(DATA):
                with open(DATA, "rb") as f:
                    body = f.read() or b"{}"
            return self._send_json(200, body)
        return super().do_GET()

    def do_POST(self):
        if self.path.split("?")[0] != "/api/state":
            return self._send_json(404, b'{"error":"not found"}')
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            json.loads(raw)
        except ValueError:
            return self._send_json(400, b'{"error":"invalid json"}')
        tmp = DATA + ".tmp"
        with open(tmp, "wb") as f:
            f.write(raw)
        os.replace(tmp, DATA)
        # one backup per day
        os.makedirs(BACKUPS, exist_ok=True)
        daily = os.path.join(BACKUPS, f"progress-{datetime.date.today().isoformat()}.json")
        shutil.copyfile(DATA, daily)
        return self._send_json(200, b'{"ok":true}')

    def log_message(self, *args):
        pass


def main():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        print(f"Port {PORT} is busy. Set MLE_PATH_PORT=8766 (or another port) and run again.")
        sys.exit(1)
    url = f"http://127.0.0.1:{PORT}/"
    print(f"MLE Path running at {url}")
    print(f"Progress file: {DATA}")
    print("Leave this window open while you use the planner. Ctrl+C to stop.")
    if "--no-browser" not in sys.argv:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
