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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Public API Engine for PyAgent.
Generates OpenAPI/Swagger specs and handles external tool integration.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import logging
from typing import Dict, Any
from .APICore import APICore

__version__ = VERSION

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