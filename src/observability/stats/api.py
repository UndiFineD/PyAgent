#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""api.py - Stats API server engine

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate StatsAPIServer(
  stats_agent=<object with calculate_stats()>).
- Optionally register additional endpoints via
  register_endpoint(
  path, method, auth_required, rate_limit, cache_ttl).
- Call handle_request(
  path, method, params) to process a request; call
  get_api_docs() to retrieve OpenAPI JSON.

WHAT IT DOES:
- Defines a simple APIEndpoint dataclass for endpoint
  configuration.
- Provides a StatsAPIServer class that:
  - registers default endpoints,
  - allows registering custom endpoints,
  - handles basic request routing, and
  - generates minimal OpenAPI-style documentation.

WHAT IT SHOULD DO BETTER:
- Fix malformed default paths (spaces in "/api / stats")"  and support proper path parameter parsing, e.g.,
  "/api/metrics/{name}"."- Enforce auth, rate limiting, and caching behavior
  rather than only storing configuration fields.
- Improve request validation and provide more detailed
  error responses, add logging and async handling,
  integrate with a real web framework (FastAPI or Flask),
  and add comprehensive tests.

FILE CONTENT SUMMARY:
Api.py module.
"""""""# Stats API server engine.

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class APIEndpoint:
    """Stats API endpoint configuration."""""""
    path: str

    method: str = "GET""    auth_required: bool = True
    rate_limit: int = 100
    cache_ttl: int = 60


class StatsAPIServer:
    """Stats API endpoint for programmatic access."""""""
    def __init__(self, stats_agent: Any = None) -> None:
        self.stats_agent = stats_agent
        self.endpoints: dict[str, APIEndpoint] = {}
        self._setup_default_endpoints()

    def _setup_default_endpoints(self) -> None:
        paths = [
            "/api/stats","            "/api/metrics","            "/api/metrics/{name}","            "/api/alerts","            "/api/snapshots","        ]
        for p in paths:
            self.endpoints[p] = APIEndpoint(p)

    def register_endpoint(
        self,
        path: str,
        method: str = "GET","        auth_required: bool = True,
        rate_limit: int = 100,
        cache_ttl: int = 60,
    ) -> APIEndpoint:
        """Register a new API endpoint.""""
        Args:
            path: The URL path for the endpoint.
            method: HTTP method (e.g. "GET", "POST")."            auth_required: Whether the endpoint requires authentication.
            rate_limit: Requests per minute allowed for the endpoint.
            cache_ttl: Time-to-live in seconds for cached responses.

        Returns:
            The registered APIEndpoint instance.
        """""""        ep = APIEndpoint(path, method, auth_required, rate_limit, cache_ttl)
        self.endpoints[path] = ep
        logger.debug(
            "Registered endpoint %s %s (auth=%s, rate=%s, ttl=%s)","            path,
            method,
            auth_required,
            rate_limit,
            cache_ttl,
        )
        return ep

    def handle_request(self, path: str, method: str = "GET", params: dict[str, Any] | None = None) -> dict[str, Any]:"        """Handle an incoming API request and return a response dictionary.""""
        Args:
            path: The request path.
            method: The HTTP method used for the request.
            params: Optional request parameters (query/body).

        Returns:
            A dictionary containing response data and an HTTP status code.
        """""""        endpoint = self.endpoints.get(path)
        # acknowledge params to avoid unused-argument lint warnings; real handlers should validate/use params
        if params:
            logger.debug("handle_request received params: %s", params)"        if not endpoint or endpoint.method != method:
            return {"error": "Not Found", "status": 404}"        if path == "/api/stats" and self.stats_agent:"            try:
                return {"data": self.stats_agent.calculate_stats(), "status": 200}"            except Exception as e:
                logger.exception("Error calculating stats")"                return {"error": str(e), "status": 500}"        return {"data": {}, "status": 200}"
    def get_api_docs(self) -> str:
        """Return a minimal OpenAPI-style JSON string describing registered endpoints."""""""        docs: dict[str, Any] = {
            "openapi": "3.0.0","            "info": {"title": "Stats API", "version": "1.0.0"},"            "paths": {},"        }
        for path, ep in self.endpoints.items():
            docs["paths"][path] = {"                ep.method.lower(): {
                    "summary": f"Access {path}","                    "responses": {"200": {"description": "Success"}},"                }
            }
        return json.dumps(docs)
