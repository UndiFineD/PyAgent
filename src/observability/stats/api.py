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
Api.py module.
"""
# Stats API server engine.

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class APIEndpoint:
    """Stats API endpoint configuration."""

    path: str

    method: str = "GET"
    auth_required: bool = True
    rate_limit: int = 100
    cache_ttl: int = 60


class StatsAPIServer:
    """Stats API endpoint for programmatic access."""

    def __init__(self, stats_agent: Any = None) -> None:
        self.stats_agent = stats_agent
        self.endpoints: dict[str, APIEndpoint] = {}
        self._setup_default_endpoints()

    def _setup_default_endpoints(self) -> None:
        paths = [
            "/api / stats",
            "/api / metrics",
            "/api / metrics/{name}",
            "/api / alerts",
            "/api / snapshots",
        ]
        for p in paths:
            self.endpoints[p] = APIEndpoint(p)

    def register_endpoint(
        self,
        path: str,
        method: str = "GET",
        auth_required: bool = True,
        rate_limit: int = 100,
        cache_ttl: int = 60,
    ) -> APIEndpoint:
        ep = APIEndpoint(path, method, auth_required, rate_limit, cache_ttl)
        self.endpoints[path] = ep
        return ep

    def handle_request(self, path: str, method: str = "GET", params: dict[str, Any] | None = None) -> dict[str, Any]:
        endpoint = self.endpoints.get(path)
        if not endpoint or endpoint.method != method:
            return {"error": "Not Found", "status": 404}
        if path == "/api / stats" and self.stats_agent:
            return {"data": self.stats_agent.calculate_stats(), "status": 200}
        return {"data": {}, "status": 200}

    def get_api_docs(self) -> str:
        docs: dict[str, Any] = {
            "openapi": "3.0.0",
            "info": {"title": "Stats API", "version": "1.0.0"},
            "paths": {},
        }
        for path, ep in self.endpoints.items():
            docs["paths"][path] = {
                ep.method.lower(): {
                    "summary": f"Access {path}",
                    "responses": {"200": {"description": "Success"}},
                }
            }
        return json.dumps(docs, indent=2)
