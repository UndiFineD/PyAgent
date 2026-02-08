# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-NachoVPN\src\nachovpn\core\plugin_manager.py
import logging
import os
import traceback

from nachovpn.core.request_handler import VPNStreamRequestHandler
from nachovpn.plugins import VPNPlugin


class PluginManager:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin_class, **kwargs):
        """Register a plugin"""
        if plugin_class.__name__ in os.getenv("DISABLED_PLUGINS", "").split(","):
            logging.info(f"Skipping disabled plugin: {plugin_class.__name__}")
            return
        plugin = plugin_class(**kwargs)
        self.plugins.append(plugin)
        logging.info(f"Registered plugin: {plugin_class.__name__}")

    def handle_data(self, data, client_socket, client_ip):
        """Try each plugin to handle raw VPN data"""
        for plugin in self.plugins:
            try:
                if plugin.is_enabled() and plugin.can_handle_data(data, client_socket, client_ip):
                    return plugin.handle_data(data, client_socket, client_ip)
            except Exception as e:
                logging.error(f"Error in plugin {plugin.__class__.__name__}: {e}")
                logging.error(traceback.format_exc())
        return False

    def handle_http(self, handler):
        """Try each plugin to handle HTTP requests"""
        for plugin in self.plugins:
            try:
                if plugin.is_enabled() and plugin.can_handle_http(handler):
                    handler.plugin_name = plugin.__class__.__name__
                    return plugin.handle_http(handler)
            except Exception as e:
                logging.error(f"Error in plugin {plugin.__class__.__name__}: {e}")
                logging.error(traceback.format_exc())
        return False
