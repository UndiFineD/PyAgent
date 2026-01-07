#!/usr/bin/env python3

"""Auto-extracted class from agent_stats.py"""

from __future__ import annotations

from .APIEndpoint import APIEndpoint
from .StatsAgent import StatsAgent

from typing import Any, Dict, Optional
import json

class StatsAPIServer:
    """Stats API endpoint for programmatic access.

    Provides RESTful API endpoints for accessing stats
    programmatically.

    Attributes:
        endpoints: Registered API endpoints.
        stats_agent: The stats agent to serve data from.
    """

    def __init__(self, stats_agent: Optional[StatsAgent] = None) -> None:
        """Initialize API server.

        Args:
            stats_agent: Optional stats agent instance.
        """
        self.stats_agent = stats_agent
        self.endpoints: Dict[str, APIEndpoint] = {}
        self._request_count: Dict[str, int] = {}
        self._setup_default_endpoints()

    def _setup_default_endpoints(self) -> None:
        """Setup default API endpoints."""
        defaults = [
            APIEndpoint("/api / stats", "GET", True, 100, 60),
            APIEndpoint("/api / metrics", "GET", True, 100, 30),
            APIEndpoint("/api / metrics/{name}", "GET", True, 100, 30),
            APIEndpoint("/api / alerts", "GET", True, 50, 10),
            APIEndpoint("/api / snapshots", "GET", True, 50, 60),
        ]
        for endpoint in defaults:
            self.endpoints[endpoint.path] = endpoint
            self._request_count[endpoint.path] = 0

    def register_endpoint(
        self,
        path: str,
        method: str = "GET",
        auth_required: bool = True,
        rate_limit: int = 100,
        cache_ttl: int = 60
    ) -> APIEndpoint:
        """Register a custom API endpoint.

        Args:
            path: The endpoint path.
            method: HTTP method.
            auth_required: Whether authentication is required.
            rate_limit: Requests per minute limit.
            cache_ttl: Cache time - to - live in seconds.

        Returns:
            The registered endpoint.
        """
        endpoint = APIEndpoint(
            path=path,
            method=method,
            auth_required=auth_required,
            rate_limit=rate_limit,
            cache_ttl=cache_ttl
        )
        self.endpoints[path] = endpoint
        self._request_count[path] = 0
        return endpoint

    def handle_request(
        self,
        path: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Handle an API request.

        Args:
            path: The request path.
            method: The HTTP method.
            params: Request parameters.

        Returns:
            Response data.
        """
        endpoint = self.endpoints.get(path)
        if not endpoint:
            return {"error": "Endpoint not found", "status": 404}

        if endpoint.method != method:
            return {"error": "Method not allowed", "status": 405}

        self._request_count[path] += 1

        # Route to appropriate handler
        if path == "/api / stats" and self.stats_agent:
            return {"data": self.stats_agent.calculate_stats(), "status": 200}
        elif path == "/api / alerts" and self.stats_agent:
            alerts = self.stats_agent.get_alerts()
            return {"data": [{"id": a.id, "message": a.message} for a in alerts], "status": 200}
        else:
            return {"data": {}, "status": 200}

    def get_api_docs(self) -> str:
        """Generate API documentation.

        Returns:
            OpenAPI - style documentation.
        """
        docs: Dict[str, Any] = {
            "openapi": "3.0.0",
            "info": {"title": "Stats API", "version": "1.0.0"},
            "paths": {}
        }

        for path, endpoint in self.endpoints.items():
            docs["paths"][path] = {
                endpoint.method.lower(): {
                    "summary": f"Access {path}",
                    "security": [{"bearerAuth": []}] if endpoint.auth_required else [],
                    "responses": {"200": {"description": "Success"}}
                }
            }

        return json.dumps(docs, indent=2)
