#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser

TARGET_URL = "http://172.20.10.2:8080/"
LISTEN_IP = "0.0.0.0"
LISTEN_PORT = 9000

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/open"):
            webbrowser.open_new_tab(TARGET_URL)  # open tab in default browser
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK\n")
            return

        self.send_response(404)
        self.end_headers()

    def log_message(self, fmt, *args):
        pass

HTTPServer((LISTEN_IP, LISTEN_PORT), Handler).serve_forever()
