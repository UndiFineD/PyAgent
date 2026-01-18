# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Tool schema adapter for MCP and OpenAI formats.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .models import ToolSchema


class SchemaAdapter:
    """Adapt tool schemas between formats."""

    @staticmethod
    def to_openai(schemas: List[ToolSchema]) -> List[Dict[str, Any]]:
        """Convert to OpenAI tool format."""
        return [s.to_openai_format() for s in schemas]

    @staticmethod
    def from_openai(tools: List[Dict[str, Any]]) -> List[ToolSchema]:
        """Convert from OpenAI tool format."""
        schemas = []
        for tool in tools:
            if tool.get("type") == "function":
                func = tool.get("function", {})
                params = func.get("parameters", {})
                schemas.append(
                    ToolSchema(
                        name=func.get("name", ""),
                        description=func.get("description", ""),
                        parameters=params.get("properties", {}),
                        required=params.get("required", []),
                    )
                )
        return schemas

    @staticmethod
    def to_mcp(schemas: List[ToolSchema]) -> List[Dict[str, Any]]:
        """Convert to MCP format."""
        return [
            {
                "name": s.name,
                "description": s.description,
                "inputSchema": {
                    "type": "object",
                    "properties": s.parameters,
                    "required": s.required,
                },
            }
            for s in schemas
        ]

    @staticmethod
    def from_mcp(tools: List[Dict[str, Any]]) -> List[ToolSchema]:
        """Convert from MCP format."""
        schemas = []
        for tool in tools:
            schema = tool.get("inputSchema", {})
            schemas.append(
                ToolSchema(
                    name=tool.get("name", ""),
                    description=tool.get("description", ""),
                    parameters=schema.get("properties", {}),
                    required=schema.get("required", []),
                )
            )
        return schemas
