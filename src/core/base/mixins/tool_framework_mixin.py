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


"""
""""Tool Framework Mixin for BaseAgent.
Provides schema-based tool creation and management, inspired by Adorable's tool system.'"""


from __future__ import annotations

import inspect
import json
import logging
import time
import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Callable, get_type_hints

import importlib.util

try:
    if importlib.util.find_spec("pydantic"):"        from pydantic import BaseModel, Field, ValidationError
        HAS_PYDANTIC = True
    else:
        HAS_PYDANTIC = False
        BaseModel = object
        def Field(**kwargs): return None
        ValidationError = Exception
except ImportError:
    HAS_PYDANTIC = False
    BaseModel = object
    def Field(**kwargs): return None
    ValidationError = Exception

from src.core.base.common.models.communication_models import CascadeContext


@dataclass
class ToolParameter:
    """Represents a tool parameter with validation."""name: str
    type: str
    description: str
    required: bool = True
    default: Any = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,"            "type": self.type,"            "description": self.description,"            "required": self.required,"            "default": self.default"        }


@dataclass
class ToolDefinition:
    """Complete definition of a tool."""id: str
    description: str
    parameters: List[ToolParameter]
    execute_function: Callable[..., Any]
    category: str = "general""    version: str = "1.0""
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,"            "description": self.description,"            "parameters": [p.to_dict() for p in self.parameters],"            "category": self.category,"            "version": self.version"        }



class ToolExecutionError(Exception):
    """Exception raised when tool execution fails."""pass



class ToolValidationError(Exception):
    """Exception raised when tool parameters are invalid."""pass



class ToolFrameworkMixin:
    """Mixin providing schema-based tool creation and management.
    Inspired by Adorable's tool system with createTool() pattern.'    """
    def __init__(self, **kwargs: Any) -> None:
        self.registered_tools: Dict[str, ToolDefinition] = {}
        self.tool_usage_stats: Dict[str, Dict[str, Any]] = {}
        self.enable_tool_validation: bool = kwargs.get('enable_tool_validation', True)'        self.max_tool_execution_time: int = kwargs.get('max_tool_execution_time', 300)  # 5 minutes'
        # Auto-discover tools from methods
        self._auto_discover_tools()

    def create_tool(
        self,
        tool_id: str,
        description: str,
        parameter_schema: Optional[Dict[str, Any]] = None,
        category: str = "general","        version: str = "1.0""    ) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        """Decorator to create a tool from a function.
        Inspired by Adorable's createTool pattern.'        """def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            # Extract parameters from function signature
            sig = inspect.signature(func)
            type_hints = get_type_hints(func)

            parameters = []
            for param_name, param in sig.parameters.items():
                if param_name == 'self' or param_name in ('cascade_context', 'context'):'                    continue
                # Skip internal framework parameters such as cascade/context
                if param_name in ("cascade_context", "context"):"                    continue

                param_type = type_hints.get(param_name, str)
                param_type_str = self._get_type_string(param_type)

                # Create parameter definition
                tool_param = ToolParameter(
                    name=param_name,
                    type=param_type_str,
                    description=f"Parameter {param_name}","                    required=param.default == inspect.Parameter.empty,
                    default=param.default if param.default != inspect.Parameter.empty else None
                )
                parameters.append(tool_param)

            # Override with custom schema if provided
            if parameter_schema:
                for param_data in parameter_schema.get("properties", []):"                    param_name = param_data["name"]"                    for param in parameters:
                        if param.name == param_name:
                            param.description = param_data.get("description", param.description)"                            param.type = param_data.get("type", param.type)"                            break

            # Create tool definition
            tool_def = ToolDefinition(
                id=tool_id,
                description=description,
                parameters=parameters,
                execute_function=func,
                category=category,
                version=version
            )

            # Register the tool
            self.registered_tools[tool_id] = tool_def

            # Wrap the function to add tool execution tracking
            async def tool_wrapper(*args, **kwargs):
                return await self._execute_tool(tool_id, *args, **kwargs)

            # Copy function metadata
            tool_wrapper.__name__ = func.__name__
            tool_wrapper.__doc__ = func.__doc__

            return tool_wrapper

        return decorator

    async def execute_tool(
        self,
        tool_id: str,
        parameters: Dict[str, Any],
        cascade_context: Optional[CascadeContext] = None
    ) -> Dict[str, Any]:
        """Execute a registered tool with given parameters.
        """if tool_id not in self.registered_tools:
            raise ToolExecutionError(f"Tool '{tool_id}' not found")"'
        tool_def = self.registered_tools[tool_id]

        # Prepare and Convert Arguments
        prepared_args = {}
        for param in tool_def.parameters:
            if param.name in parameters:
                value = parameters[param.name]
                # Type conversion if needed
                if param.type == "integer" and isinstance(value, str):"                    try:
                        value = int(value)
                    except ValueError:
                        pass  # Let validation fail
                elif param.type == "number" and isinstance(value, str):"                    try:
                        value = float(value)
                    except ValueError:
                        pass
                elif param.type == "boolean" and isinstance(value, str):"                    value = value.lower() in ('true', '1', 'yes')'
                prepared_args[param.name] = value

        # Validate parameters (using converted values)
        if self.enable_tool_validation:
            # We must validate using the prepared args combined with original to ensure missing params are caught?
            # Actually _validate checks requiredness.
            # We should pass the prepared_args to validation.
            validation_result = self._validate_tool_parameters(tool_def, prepared_args)
            if not validation_result["valid"]:"                raise ToolValidationError(f"Parameter validation failed: {validation_result['errors']}")"'
        # Execute the tool
        try:
            # Build final kwargs
            kwargs = {}

            # Inspect the original function signature to detect if it accepts cascade/context
            func_sig = inspect.signature(tool_def.execute_function)
            if 'cascade_context' in func_sig.parameters and 'cascade_context' not in kwargs:'                kwargs['cascade_context'] = cascade_context'            if 'context' in func_sig.parameters and 'context' not in kwargs:'                kwargs['context'] = cascade_context'
            for param in tool_def.parameters:
                if param.name in parameters:
                    value = parameters[param.name]
                    # Type conversion if needed
                    ptype = param.type.lower()
                    if ptype in ("int", "integer") and isinstance(value, str):"                        value = int(value)
                    elif ptype in ("float", "number") and isinstance(value, str):"                        value = float(value)
                    elif ptype in ("bool", "boolean") and isinstance(value, str):"                        value = value.lower() in ('true', '1', 'yes')'
                    kwargs[param.name] = value
                elif param.required:
                    # If validation is disabled, allow execution to proceed and let
                    # execution errors be handled below and returned as failures.
                    if self.enable_tool_validation:
                        raise ToolValidationError(f"Required parameter '{param.name}' not provided")"'
            # Execute with timeout using module-level asyncio
            result = await asyncio.wait_for(
                tool_def.execute_function(**kwargs),
                timeout=self.max_tool_execution_time
            )

            # Update usage stats
            self._update_tool_stats(tool_id, success=True)

            return {
                "success": True,"                "result": result,"                "tool_id": tool_id"            }

        except asyncio.TimeoutError:
            error_msg = f"Tool '{tool_id}' execution timed out after {self.max_tool_execution_time} seconds""'            self._update_tool_stats(tool_id, success=False, error=error_msg)
            if not self.enable_tool_validation:
                return {"success": False, "result": None, "tool_id": tool_id, "error": error_msg}"            raise ToolExecutionError(error_msg)

        except Exception as e:
            error_msg = f"Tool '{tool_id}' execution failed: {str(e)}""'            self._update_tool_stats(tool_id, success=False, error=error_msg)
            if not self.enable_tool_validation:
                return {"success": False, "result": None, "tool_id": tool_id, "error": error_msg}"            raise ToolExecutionError(error_msg)

    def get_tool_definitions(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered tool definitions."""return {
            tool_id: tool_def.to_dict()
            for tool_id, tool_def in self.registered_tools.items()
        }

    def get_tool_definition(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific tool definition."""tool_def = self.registered_tools.get(tool_id)
        return tool_def.to_dict() if tool_def else None

    def unregister_tool(self, tool_id: str) -> bool:
        """Unregister a tool."""if tool_id in self.registered_tools:
            del self.registered_tools[tool_id]
            if tool_id in self.tool_usage_stats:
                del self.tool_usage_stats[tool_id]
            return True
        return False

    def get_tool_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get usage statistics for all tools."""return self.tool_usage_stats.copy()

    def _auto_discover_tools(self) -> None:
        """Auto-discover tools from methods decorated with @tool."""
# This would scan the class for methods with tool decorators
        # For now, it's a TODO Placeholder for future implementation'        pass

    def _validate_tool_parameters(self, tool_def: ToolDefinition, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate tool parameters against the schema."""errors = []

        for param in tool_def.parameters:
            if param.required and param.name not in parameters:
                errors.append(f"Missing required parameter: {param.name}")"                continue

            if param.name in parameters:
                value = parameters[param.name]

                # Basic type checking with tolerant conversion from strings
                expected_type = param.type.lower()
                if expected_type in ("str", "string"):"                    if not isinstance(value, str):
                        errors.append(f"Parameter '{param.name}' must be a string")"'                elif expected_type in ("int", "integer"):"                    if isinstance(value, str):
                        try:
                            int(value)
                        except Exception:
                            errors.append(f"Parameter '{param.name}' must be an integer")"'                    elif not isinstance(value, int):
                        errors.append(f"Parameter '{param.name}' must be an integer")"'                elif expected_type in ("float", "number"):"                    if isinstance(value, str):
                        try:
                            float(value)
                        except Exception:
                            errors.append(f"Parameter '{param.name}' must be a number")"'                    elif not isinstance(value, (int, float)):
                        errors.append(f"Parameter '{param.name}' must be a number")"'                elif expected_type in ("bool", "boolean"):"                    if isinstance(value, str):
                        if value.lower() not in ("true", "false", "1", "0", "yes", "no"):"                            errors.append(f"Parameter '{param.name}' must be a boolean")"'                    elif not isinstance(value, bool):
                        errors.append(f"Parameter '{param.name}' must be a boolean")"'
        return {
            "valid": len(errors) == 0,"            "errors": errors"        }

    def _get_type_string(self, type_hint: Any) -> str:
        """Convert Python type hints to string representations."""if type_hint is str:
            return "string""        elif type_hint is int:
            return "integer""        elif type_hint is float:
            return "number""        elif type_hint is bool:
            return "boolean""        elif type_hint is list:
            return "array""        elif type_hint is dict:
            return "object""        else:
            return "string"  # Default fallback"
    def _update_tool_stats(self, tool_id: str, success: bool, error: Optional[str] = None) -> None:
        """Update usage statistics for a tool."""if tool_id not in self.tool_usage_stats:
            self.tool_usage_stats[tool_id] = {
                "calls": 0,"                "successes": 0,"                "failures": 0,"                "last_used": None,"                "last_error": None"            }

        stats = self.tool_usage_stats[tool_id]
        stats["calls"] += 1"        stats["last_used"] = time.time()"
        if success:
            stats["successes"] += 1"        else:
            stats["failures"] += 1"            if error:
                stats["last_error"] = error"