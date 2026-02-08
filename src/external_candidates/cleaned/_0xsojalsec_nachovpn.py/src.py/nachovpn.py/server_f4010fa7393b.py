# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NachoVPN\src\nachovpn\server.py
import inspect
import logging
import os
import socket
import socketserver
import sys
import uuid

import nachovpn.plugins
from nachovpn.core.cert_manager import CertManager
from nachovpn.core.db_manager import DBManager
from nachovpn.core.plugin_manager import PluginManager
from nachovpn.core.request_handler import VPNStreamRequestHandler
from nachovpn.plugins import VPNPlugin

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(module)s.%(funcName)s]",
)


class ThreadedVPNServer(socketserver.ThreadingTCPServer):
    def __init__(self, server_address, RequestHandlerClass, cert_manager, plugin_manager):
        self.cert_manager = cert_manager
        self.plugin_manager = plugin_manager
        super().__init__(server_address, RequestHandlerClass)
        self.socket = cert_manager.ssl_context.wrap_socket(self.socket, server_side=True)


class VPNServer:
    def __init__(self, host="0.0.0.0", port=443, cert_dir=os.path.join(os.getcwd(), "certs")):
        self.host = host
        self.port = port

        # Setup certificates
        self.cert_manager = CertManager(cert_dir)
        self.cert_manager.setup()

        # Initialize database
        self.db_manager = DBManager()

        # Setup plugin manager with cert hash
        self.plugin_manager = PluginManager()

        # Common plugin kwargs
        plugin_kwargs = {
            "write_pcap": os.getenv("WRITE_PCAP", False),
            "cert_manager": self.cert_manager,
            "external_ip": os.getenv("EXTERNAL_IP", socket.gethostbyname(socket.gethostname())),
            "dns_name": os.getenv("SERVER_FQDN", socket.gethostname()),
            "db_manager": self.db_manager,
        }

        # Register plugins
        for name, plugin in inspect.getmembers(nachovpn.plugins, inspect.isclass):
            if issubclass(plugin, VPNPlugin) and plugin != VPNPlugin:
                self.plugin_manager.register_plugin(plugin, **plugin_kwargs)

        # Allow reuse of the address
        socketserver.ThreadingTCPServer.allow_reuse_address = True

    def run(self):
        with ThreadedVPNServer(
            (self.host, self.port),
            VPNStreamRequestHandler,
            self.cert_manager,
            self.plugin_manager,
        ) as server:
            logging.info(f"Server listening on {self.host}:{self.port}")
            server.serve_forever()


def main():
    log_level = logging.INFO

    if "-d" in sys.argv or "--debug" in sys.argv:
        log_level = logging.DEBUG
    elif "-q" in sys.argv or "--quiet" in sys.argv:
        log_level = logging.WARNING

    logging.getLogger().setLevel(log_level)

    server = VPNServer()
    try:
        server.run()
    except KeyboardInterrupt:
        logging.info("\nShutting down...")


if __name__ == "__main__":
    main()
