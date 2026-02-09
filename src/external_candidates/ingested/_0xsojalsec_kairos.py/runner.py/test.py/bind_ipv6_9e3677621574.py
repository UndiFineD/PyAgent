# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Kairos\Runner\test\bind_ipv6.py
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler


class HTTPServerV6(HTTPServer):
    address_family = socket.AF_INET6


server = HTTPServerV6(("::", 8081), SimpleHTTPRequestHandler)
server.serve_forever()
