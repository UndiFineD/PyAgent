# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NachoVPN\src\nachovpn\plugins\example\plugin.py
import logging

from flask import Flask, jsonify, request
from nachovpn.plugins import VPNPlugin


class ExamplePlugin(VPNPlugin):
    def _setup_routes(self):
        # Call the parent class's route setup
        super()._setup_routes()

        # Add additional routes specific to this plugin
        @self.flask_app.route("/api/v2/healthcheck", methods=["GET"])
        def healthcheck_v2():
            return jsonify({"message": "OK"})

    def can_handle_http(self, handler):
        return handler.path in ["/api/v2/healthcheck"]

    def can_handle_data(self, data, client_socket, client_ip):
        logging.info(
            f"ExamplePlugin::can_handle_data: Received data from {client_ip}: {data.hex()}"
        )
        return len(data) >= 4 and b"PING" in data[:4]

    def handle_data(self, data, client_socket, client_ip):
        logging.info(
            f"ExamplePlugin::handle_data: Received data from {client_ip}: {data.hex()}"
        )
        client_socket.sendall(b"PONG\n")
        return True
