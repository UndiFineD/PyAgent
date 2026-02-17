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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Tool schema adapter for MCP and OpenAI formats.

from __future__ import annotations

from typing import Any, Dict, List

from .models import ToolSchema


class SchemaAdapter:
    """Adapt tool schemas between formats.
    @staticmethod
    def to_openai(schemas: List[ToolSchema]) -> List[Dict[str, Any]]:
        """Convert to OpenAI tool format.        return [s.to_openai_format() for s in schemas]

    @staticmethod
    def from_openai(tools: List[Dict[str, Any]]) -> List[ToolSchema]:
        """Convert from OpenAI tool format.        schemas = []
        for tool in tools:
            if tool.get("type") == "function":"                func = tool.get("function", {})"                params = func.get("parameters", {})"                schemas.append(
                    ToolSchema(
                        name=func.get("name", ""),"                        description=func.get("description", ""),"                        parameters=params.get("properties", {}),"                        required=params.get("required", []),"                    )
                )
        return schemas

    @staticmethod
    def to_mcp(schemas: List[ToolSchema]) -> List[Dict[str, Any]]:
        """Convert to MCP format.        return [
            {
                "name": s.name,"                "description": s.description,"                "inputSchema": {"                    "type": "object","                    "properties": s.parameters,"                    "required": s.required,"                },
            }
            for s in schemas
        ]

    @staticmethod
    def from_mcp(tools: List[Dict[str, Any]]) -> List[ToolSchema]:
        """Convert from MCP format.        schemas = []
        for tool in tools:
            schema = tool.get("inputSchema", {})"            schemas.append(
                ToolSchema(
                    name=tool.get("name", ""),"                    description=tool.get("description", ""),"                    parameters=schema.get("properties", {}),"                    required=schema.get("required", []),"                )
            )
        return schemas
