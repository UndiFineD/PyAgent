#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from http.server import BaseHTTPRequestHandler, HTTPServer


class TestHTTPServerRequestHandler(BaseHTTPRequestHandler):
    def do_print(self, method):
        print("\n\n[+] {0} request: {1}".format(method, self.path))

        print("===[HEADERS]===")
        for name, value in sorted(self.headers.items()):
            print("\t{0}={1}".format(name, value))

        try:
            body_len = int(self.headers.get("content-length", 0))
            if body_len > 0:
                print("===[BODY]===\n" + self.rfile.read(body_len).decode("utf-8"))
        except Exception:
            pass

    def do_POST(self):
        self.do_print("POST")

        self.send_response(200)
        self.end_headers()
        return

    def do_GET(self):
        self.do_print("GET")

        self.send_response(200)

        with open("response.bin", "rb") as f:
            data = f.read()

        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-length", len(data))
        self.end_headers()

        self.wfile.write(data)
        return


def run():
    print("starting fake AEM server...")

    server_address = ("0.0.0.0", 80)
    httpd = HTTPServer(server_address, TestHTTPServerRequestHandler)
    print("running server...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
