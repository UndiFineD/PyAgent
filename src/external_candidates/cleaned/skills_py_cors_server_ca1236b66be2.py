# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\r00tid.py\token_alert.py\scripts.py\cors_server_ca1236b66be2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\r00tid\token-alert\scripts\cors-server.py

#!/usr/bin/env python3

"""CORS-enabled HTTP Server for Token Alert Dashboard"""

import sys

from http.server import HTTPServer, SimpleHTTPRequestHandler


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")

        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")

        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)

        self.end_headers()


if __name__ == "__main__":
    port = 8765

    server = HTTPServer(("localhost", port), CORSRequestHandler)

    print(f"✅ CORS-enabled server running on http://localhost:{port}")

    print(f"📊 Dashboard: http://localhost:{port}/dashboard-v3.html")

    server.serve_forever()
