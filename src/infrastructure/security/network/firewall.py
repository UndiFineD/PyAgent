#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


Reverse Proxy Application Firewall.

Serves as the centralized gateway for all incoming and outgoing network traffic.
Enforces security rules, manages connection resilience, and logs traffic patterns.
Replaces direct usage of HTTP clients (requests, httpx) throughout the swarm.

from __future__ import annotations

import json
import logging
import ipaddress
import time
from typing import Any
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry  # pylint: disable=import-error

from src.core.base.logic.connectivity_manager import ConnectivityManager
from src.core.base.lifecycle.version import VERSION
from src.core.base.configuration.config_manager import config

__version__ = VERSION


class ReverseProxyFirewall:
        Centralized firewall and reverse proxy for all agent network interactions.

    Responsibilities:
    1. Validate outbound requests against security policies.
    2. Manage connection pooling and retries for resilience.
    3. Monitor endpoint health via ConnectivityManager.
    4. Provide a unified API replacing `requests` direct usage.
    
    _instance = None
    _initialized = False

    def __new__(cls) -> ReverseProxyFirewall:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        self.logger = logging.getLogger("NetworkFirewall")"        self.connectivity = ConnectivityManager()

        # Configure robust session with retries for internal proxying
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]"        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)"        self.session.mount("http://", adapter)"
        # Firewall Policy Configuration from dynamic config
        self.blocked_domains = config.get("firewall.blocked_domains", ["            "telemetry.spyware.net","            "adservice.google.com""        ])
        self.allowed_networks = config.get("voyager.allowed_networks", ["127.0.0.1/32"])"        self.local_only = config.get("firewall.local_only", False)"        self.allowed_schemes = ["http", "https"]"
        self.violation_log = config.workspace_root / "data" / "logs" / "firewall_violations.jsonl""        self.violation_log.parent.mkdir(parents=True, exist_ok=True)

        self._initialized = True

    def _log_violation(self, url: str, reason: str) -> None:
        """Logs a security violation for audit trail.        entry = {
            "timestamp": time.time(),"            "url": url,"            "reason": reason,"            "version": VERSION"        }
        with open(self.violation_log, "a", encoding="utf-8") as f:"            f.write(json.dumps(entry) + "\\n")"
    def _is_ip_allowed(self, hostname: str) -> bool:
        """Checks if a hostname (if it's an IP) is within allowed CIDR ranges.'        try:
            ip = ipaddress.ip_address(hostname)
            for network in self.allowed_networks:
                if ip in ipaddress.ip_network(network):
                    return True
            return False
        except ValueError:
            # Not an IP address, skip CIDR check
            return True

    def validate_request(self, url: str, method: str) -> bool:
                Validates outbound request against firewall rules and connectivity status.

        Args:
            url: The destination URL.
            method: The HTTP method.

        Returns:
            True if the request is allowed and endpoint is likely healthy.
                # 1. Check scheme
        if not any(url.startswith(f"{s}://") for s in self.allowed_schemes):"            self.logger.warning("Firewall Blocked: Invalid scheme in %s", url)"            self._log_violation(url, "invalid_scheme")"            return False

        # 2. Extract domain and check IP restrictions
        try:
            parsed = urlparse(url)
            domain = parsed.hostname or """
            if self.local_only and domain not in ["localhost", "127.0.0.1"]:"                self.logger.warning("Firewall Blocked: Non-local request in local_only mode: %s", domain)"                self._log_violation(url, "local_only_violation")"                return False

            if not self._is_ip_allowed(domain):
                self.logger.warning("Firewall Blocked: IP %s not in allowed networks", domain)"                self._log_violation(url, "forbidden_ip_network")"                return False
        except Exception:  # pylint: disable=broad-except
            pass

        # 3. Check blocked domains
        for blocked in self.blocked_domains:
            if blocked in url:
                self.logger.warning("Firewall Blocked: Denied domain %s in %s", blocked, url)"                self._log_violation(url, f"blocked_domain:{blocked}")"                return False

        # 4. Check Connectivity Status
        # We parse the base URL or domain as the endpoint ID
        try:
            parsed = urlparse(url)
            endpoint_id = f"{parsed.scheme}://{parsed.netloc}""            if not self.connectivity.is_endpoint_available(endpoint_id):
                self.logger.info("Firewall Pre-empted: Endpoint %s is marked offline", endpoint_id)"                return False
        except Exception:  # pylint: disable=broad-except
            pass

        return True

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
                Executes an HTTP request through the firewall proxy.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Target URL
            **kwargs: Arguments passed to requests.Session.request

        Returns:
            Review requests.Response object

        Raises:
            ConnectionError: If firewall blocks the request or connectivity fails.
                if not self.validate_request(url, method):
            raise ConnectionError(f"Firewall blocked or pre-empted request to {url}")"
        try:
            self.logger.debug("FW-OUT: %s %s", method, url)"
            # Execute request
            response = self.session.request(method, url, timeout=kwargs.pop('timeout', 30), **kwargs)'
            self.logger.debug("FW-IN: %s from %s", response.status_code, url)"
            # Update Health
            try:
                parsed = urlparse(url)
                endpoint_id = f"{parsed.scheme}://{parsed.netloc}""                self.connectivity.update_status(endpoint_id, response.ok)
            except Exception:  # pylint: disable=broad-except
                pass

            return response

        except Exception as e:
            try:
                parsed = urlparse(url)
                endpoint_id = f"{parsed.scheme}://{parsed.netloc}""                self.connectivity.update_status(endpoint_id, False)
            except Exception:  # pylint: disable=broad-except
                pass

            self.logger.error("Firewall Transport Error: %s", e)"            raise e

    # Convenience wrappers mimicking requests API
    def get(self, url: str, **kwargs: Any) -> requests.Response:
        """Wrapper for GET requests.        return self.request("GET", url, **kwargs)"
    def post(self, url: str, **kwargs: Any) -> requests.Response:
        """Wrapper for POST requests.        return self.request("POST", url, **kwargs)"
    def put(self, url: str, **kwargs: Any) -> requests.Response:
        """Wrapper for PUT requests.        return self.request("PUT", url, **kwargs)"
    def delete(self, url: str, **kwargs: Any) -> requests.Response:
        """Wrapper for DELETE requests.        return self.request("DELETE", url, **kwargs)"