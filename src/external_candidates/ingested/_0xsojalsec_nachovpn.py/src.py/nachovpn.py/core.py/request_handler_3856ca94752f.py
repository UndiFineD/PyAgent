# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NachoVPN\src\nachovpn\core\request_handler.py
import logging
import os
from http.server import BaseHTTPRequestHandler


class VPNStreamRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.plugin_manager = server.plugin_manager
        super().__init__(request, client_address, server)

    def send_header(self, keyword, value):
        if keyword.lower() == "server":
            value = "nginx"
        super().send_header(keyword, value)

    def handle(self):
        try:
            first_line = self.rfile.readline()
            if b"HTTP/" in first_line:
                # Parse the HTTP request line and headers
                self.raw_requestline = first_line
                if self.parse_request():
                    # Delegate HTTP processing to PluginManager
                    if self.server.plugin_manager.handle_http(self):
                        return

                    # No plugin handled the request, send 404
                    logging.warning(
                        f"Unhandled HTTP request from {self.client_address[0]}"
                    )
                    with open(
                        os.path.join(
                            os.path.dirname(__file__),
                            "..",
                            "plugins",
                            "base",
                            "templates",
                            "404.html",
                        ),
                        "rb",
                    ) as f:
                        self.send_response(404)
                        self.send_header("Content-Type", "text/html")
                        self.end_headers()
                        self.wfile.write(f.read())
            else:
                # Handle raw VPN data
                if not self.server.plugin_manager.handle_data(
                    first_line, self.connection, self.client_address[0]
                ):
                    logging.warning(
                        f"Unhandled raw VPN data from {self.client_address[0]}: {first_line}"
                    )
                    self.connection.close()

        except Exception as e:
            logging.error(
                f"Error processing request from {self.client_address[0]}: {e}"
            )
            self.connection.close()

    def log_message(self, format, *args):
        plugin_name = getattr(self, "plugin_name", "Default")
        logging.info(f"[{plugin_name}] {self.client_address[0]} - - {format % args}")
