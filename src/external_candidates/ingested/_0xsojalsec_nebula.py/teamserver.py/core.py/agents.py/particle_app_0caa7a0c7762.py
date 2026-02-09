# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Nebula\teamserver\core\Agents\particle_app.py
import http.server

from databases.db import initialize_db
from flask import Flask
from waitress import serve


def http_listener(host, port):
    httpd = http.server.HTTPServer((host, port), http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()


def main(database, host, port, c2_port):
    particle_app = Flask(__name__)
    particle_app.config["MONGODB_DB"] = database
    particle_app.config["MONGODB_HOST"] = host
    particle_app.config["MONGODB_PORT"] = port
    particle_app.config["MONGODB_CONNECT"] = False

    initialize_db(particle_app)
    particle_app.register_blueprint(listener_blueprint)

    serve(particle_app, host="0.0.0.0", port=c2_port)
