#!/usr/bin/env python3
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

import asyncio
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Dict, List, Optional
import random
import string


class SSRFDetectorMixin:
    """
    Mixin providing SSRF detection capabilities using callback server pattern.

    Inspired by aem-hacker's detector server for SSRF vulnerability detection.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ssrf_token: str = self._generate_token()
        self._ssrf_data: Dict[str, List[str]] = {}
        self._server: Optional[HTTPServer] = None
        self._server_thread: Optional[threading.Thread] = None
        self._server_running: bool = False

    def _generate_token(self) -> str:
        """Generate random token for SSRF detection."""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

    class _DetectorHandler(BaseHTTPRequestHandler):
        """HTTP handler for SSRF detection callbacks."""

        def __init__(self, token: str, data_dict: Dict[str, List[str]], *args, **kwargs):
            self.token = token
            self.data_dict = data_dict
            super().__init__(*args, **kwargs)

        def log_message(self, format, *args):
            # Suppress default logging
            return

        def do_GET(self):
            self._handle_request()

        def do_POST(self):
            self._handle_request()

        def do_PUT(self):
            self._handle_request()

        def _handle_request(self):
            try:
                # Parse path: /token/key/value
                parts = self.path.strip('/').split('/')
                if len(parts) >= 3:
                    token, key, value = parts[0], parts[1], '/'.join(parts[2:])

                    if token == self.token:
                        if key in self.data_dict:
                            self.data_dict[key].append(value)
                        else:
                            self.data_dict[key] = [value]

                self.send_response(200)
                self.end_headers()

            except Exception:
                self.send_response(200)
                self.end_headers()

    def start_ssrf_detector(self, host: str = '0.0.0.0', port: int = 8080) -> bool:
        """
        Start the SSRF detection server.

        Args:
            host: Host to bind to
            port: Port to listen on

        Returns:
            True if started successfully
        """
        if self._server_running:
            return True

        try:
            # Create handler class with current token and data dict
            def handler_class(*args, **kwargs):
                return self._DetectorHandler(self._ssrf_token, self._ssrf_data, *args, **kwargs)

            self._server = HTTPServer((host, port), handler_class)
            self._server_thread = threading.Thread(target=self._server.serve_forever, daemon=True)
            self._server_thread.start()
            self._server_running = True

            return True

        except Exception as e:
            print(f"Failed to start SSRF detector: {e}")
            return False

    def stop_ssrf_detector(self) -> None:
        """Stop the SSRF detection server."""
        if self._server_running and self._server:
            self._server.shutdown()
            self._server.server_close()
            self._server_running = False
            self._server = None
            if self._server_thread:
                self._server_thread.join(timeout=5)
                self._server_thread = None

    def get_ssrf_callback_url(self, host: str, port: int) -> str:
        """
        Get the callback URL for SSRF detection.

        Args:
            host: External host for callbacks
            port: External port for callbacks

        Returns:
            Callback URL pattern
        """
        return f"http://{host}:{port}/{self._ssrf_token}"

    def check_ssrf_triggered(self, key: str, timeout: int = 10) -> List[str]:
        """
        Check if SSRF was triggered for a specific key.

        Args:
            key: The key to check
            timeout: Time to wait for callbacks

        Returns:
            List of values received for the key
        """
        if not self._server_running:
            return []

        # Wait for callbacks
        time.sleep(timeout)

        return self._ssrf_data.get(key, [])

    async def async_check_ssrf_triggered(self, key: str, timeout: int = 10) -> List[str]:
        """Async version of check_ssrf_triggered."""
        if not self._server_running:
            return []

        await asyncio.sleep(timeout)

        return self._ssrf_data.get(key, [])

    def clear_ssrf_data(self) -> None:
        """Clear collected SSRF data."""
        self._ssrf_data.clear()

    def reset_ssrf_token(self) -> str:
        """Generate new token and clear data."""
        self._ssrf_token = self._generate_token()
        self._ssrf_data.clear()
        return self._ssrf_token

    def is_detector_running(self) -> bool:
        """Check if detector server is running."""
        return self._server_running

    def get_ssrf_token(self) -> str:
        """Get current SSRF token."""
        return self._ssrf_token
