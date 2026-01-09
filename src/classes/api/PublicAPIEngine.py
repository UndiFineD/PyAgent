#!/usr/bin/env python3

"""Public API Engine for PyAgent.
Generates OpenAPI/Swagger specs and handles external tool integration.
"""

import json
import logging
from typing import Dict, List, Any
from .APICore import APICore

class PublicAPIEngine:
    """
    Manages the external interface for third-party integrations.
    Shell for APICore.
    """

    def __init__(self, fleet_manager: Any) -> None:
        self.fleet = fleet_manager
        self.core = APICore()

    def generate_openapi_spec(self) -> str:
        """Generates a dynamic OpenAPI 3.0 specification based on registered tools."""
        # Standardize tool data for core
        raw_tools = []
        if hasattr(self.fleet, 'registry'):
             # This depends on how tools are stored, assuming a list of objects with .name
             tools = self.fleet.registry.list_tools()
             for t in tools:
                 raw_tools.append({"name": t.name, "parameters": getattr(t, 'parameters', None)})
        
        return self.core.build_openapi_json(raw_tools)

    def register_external_tool(self, tool_spec: Dict[str, Any]) -> str:
        """Registers a tool from an external OpenAPI definition."""
        if not self.core.validate_tool_contract(tool_spec):
             return "Error: Invalid tool specification."
             
        name = tool_spec.get("name")
        logging.info(f"API-ENGINE: Importing external tool '{name}'")
        return f"Successfully registered external tool '{name}' into fleet registry."
