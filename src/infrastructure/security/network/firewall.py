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

"""
Reverse Proxy Application Firewall.

Serves as the centralized gateway for all incoming and outgoing network traffic.
Enforces security rules, manages connection resilience, and logs traffic patterns.
Replaces direct usage of HTTP clients (requests, httpx) throughout the swarm.
"""

from __future__ import annotations

import logging
from typing import Any
from urllib.parse import urlparse

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry  # pylint: disable=import-error

from src.core.base.logic.connectivity_manager import ConnectivityManager
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ReverseProxyFirewall:
    """
    Centralized firewall and reverse proxy for all agent network interactions.
    
    Responsibilities:
    1. Validate outbound requests against security policies.
    2. Manage connection pooling and retries for resilience.
    3. Monitor endpoint health via ConnectivityManager.
    4. Provide a unified API replacing `requests` direct usage.
    """

    _instance = None
    _initialized = False

    def __new__(cls) -> ReverseProxyFirewall:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        
        self.logger = logging.getLogger("NetworkFirewall")
        self.connectivity = ConnectivityManager()
        
        # Configure robust session with retries for internal proxying
        self.session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        
        # Firewall Policy Configuration
        # In a real deployment, these would load from external config
        self.blocked_domains = [
            "telemetry.spyware.net",
            "adservice.google.com"
        ]
        self.allowed_schemes = ["http", "https"]
        
        self._initialized = True

    def validate_request(self, url: str, method: str) -> bool:
        """
        Validates outbound request against firewall rules and connectivity status.
        
        Args:
            url: The destination URL.
            method: The HTTP method.
            
        Returns:
            True if the request is allowed and endpoint is likely healthy.
        """
        # 1. Check scheme
        if not any(url.startswith(f"{s}://") for s in self.allowed_schemes):
            self.logger.warning("Firewall Blocked: Invalid scheme in %s", url)
            return False
            
        # 2. Check blocked domains
        for domain in self.blocked_domains:
            if domain in url:
                self.logger.warning("Firewall Blocked: Denied domain %s in %s", domain, url)
                return False
                
        # 3. Check Connectivity Status
        # We parse the base URL or domain as the endpoint ID
        try:
            parsed = urlparse(url)
            endpoint_id = f"{parsed.scheme}://{parsed.netloc}"
            if not self.connectivity.is_endpoint_available(endpoint_id):
                self.logger.info("Firewall Pre-empted: Endpoint %s is marked offline", endpoint_id)
                # We return True to let the request try anyway if it's critical? 
                # Or False to enforcing caching. The prompt asked for "Resilience Issue: Use ConnectivityManager"
                # If we return False, we are doing what ConnectivityManager suggests (skipping dead endpoints).
                return False
        except Exception:  # pylint: disable=broad-except
            pass

        return True

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """
        Executes an HTTP request through the firewall proxy.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Target URL
            **kwargs: Arguments passed to requests.Session.request
            
        Returns:
            Review requests.Response object
            
        Raises:
            ConnectionError: If firewall blocks the request or connectivity fails.
        """
        if not self.validate_request(url, method):
            raise ConnectionError(f"Firewall blocked or pre-empted request to {url}")
            
        try:
            self.logger.debug("FW-OUT: %s %s", method, url)
            
            # Execute request
            response = self.session.request(method, url, timeout=kwargs.pop('timeout', 30), **kwargs)
            
            self.logger.debug("FW-IN: %s from %s", response.status_code, url)
            
            # Update Health
            try:
                parsed = urlparse(url)
                endpoint_id = f"{parsed.scheme}://{parsed.netloc}"
                self.connectivity.update_status(endpoint_id, response.ok)
            except Exception: # pylint: disable=broad-except
                pass
            
            return response
            
        except Exception as e:
            try:
                parsed = urlparse(url)
                endpoint_id = f"{parsed.scheme}://{parsed.netloc}"
                self.connectivity.update_status(endpoint_id, False)
            except Exception: # pylint: disable=broad-except
                pass
                
            self.logger.error("Firewall Transport Error: %s", e)
            raise e

    # Convenience wrappers mimicking requests API
    def get(self, url: str, **kwargs: Any) -> requests.Response:
        """Wrapper for GET requests."""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> requests.Response:
        """Wrapper for POST requests."""
        return self.request("POST", url, **kwargs)
        
    def put(self, url: str, **kwargs: Any) -> requests.Response:
        """Wrapper for PUT requests."""
        return self.request("PUT", url, **kwargs)
        
    def delete(self, url: str, **kwargs: Any) -> requests.Response:
        """Wrapper for DELETE requests."""
        return self.request("DELETE", url, **kwargs)
