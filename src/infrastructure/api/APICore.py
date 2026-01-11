#!/usr/bin/env python3

"""
APICore logic for fleet communication.
Pure logic for OpenAPI spec generation and tool contract validation.
"""

import json
from typing import Dict, List, Any

from src.core.base.version import SDK_VERSION

class APICore:
    def __init__(self, version: str = SDK_VERSION) -> None:
        self.version = version

    def build_openapi_json(self, tool_definitions: List[Dict[str, Any]]) -> str:
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

    def validate_tool_contract(self, spec: Dict[str, Any]) -> bool:
        """Checks if an external tool definition is valid."""
        return "name" in spec and ("endpoint" in spec or "implementation" in spec)
