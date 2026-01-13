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

"""
APICore logic for fleet communication.
Pure logic for OpenAPI spec generation and tool contract validation.
"""

from __future__ import annotations
from src.core.base.version import VERSION
import json
from typing import Dict, List, Any
from src.core.base.version import SDK_VERSION

__version__ = VERSION

class APICore:
    def __init__(self, version: str = SDK_VERSION) -> None:
        self.version = version

    def build_openapi_json(self, tool_definitions: list[dict[str, Any]]) -> str:
        """Constructs an OpenAPI 3.0 string from tool metadata."""
        paths = {}
        for tool in tool_definitions:
            tool_name = tool.get('name', 'unknown')
            paths[f"/tools/{tool_name}"] = {
                "post": {
                    "summary": f"Execute {tool_name}",
                    "operationId": tool_name,
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": tool.get('parameters', {"input": {"type": "string"}})
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {"description": "OK"}
                    }
                }
            }
            
        spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "PyAgent Fleet API",
                "version": self.version
            },
            "paths": paths
        }
        return json.dumps(spec, indent=2)

    def validate_tool_contract(self, spec: dict[str, Any]) -> bool:
        """Checks if an external tool definition is valid."""
        return "name" in spec and ("endpoint" in spec or "implementation" in spec)