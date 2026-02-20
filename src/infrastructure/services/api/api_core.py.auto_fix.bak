#!/usr/bin/env python3
from __future__ import annotations


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


"""
APICore logic for fleet communication.
Pure logic for OpenAPI spec generation and tool contract validation.
"""

import json
from typing import Any

from src.core.base.lifecycle.version import SDK_VERSION, VERSION

__version__ = VERSION

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc: Any = None  # type: ignore[no-redef]



class APICore:
    """Logic for API-related operations, including OpenAPI schema generation.
    def __init__(self, version: str = SDK_VERSION) -> None:
        self.version = version

    def build_openapi_json(self, tool_definitions: list[dict[str, Any]]) -> str:
        """Constructs an OpenAPI 3.0 string from tool metadata.        if rc:
            try:
                return rc.generate_openapi_spec(tool_definitions, self.version)  # type: ignore[attr-defined]
            except Exception:  # pylint: disable=broad-exception-caught
                pass

        paths = {}
        for tool in tool_definitions:
            tool_name = tool.get("name", "unknown")"            paths[f"/tools/{tool_name}"] = {"                "post": {"                    "summary": f"Execute {tool_name}","                    "operationId": tool_name,"                    "requestBody": {"                        "content": {"                            "application/json": {"                                "schema": {"                                    "type": "object","                                    "properties": tool.get("parameters", {"input": {"type": "string"}}),"                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "OK"}},"                }
            }

        spec = {
            "openapi": "3.0.0","            "info": {"title": "PyAgent Fleet API", "version": self.version},"            "paths": paths,"        }
        return json.dumps(spec, indent=2)

    def validate_tool_contract(self, spec: dict[str, Any]) -> bool:
        """Checks if an external tool definition is valid.        return "name" in spec and ("endpoint" in spec or "implementation" in spec)"