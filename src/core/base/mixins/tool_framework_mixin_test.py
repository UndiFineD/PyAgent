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
Tests for Tool Framework Mixin.
Tests schema-based tool creation and management inspired by Adorable's tool system.
"""

import pytest
import asyncio
from src.core.base.mixins.tool_framework_mixin import (
    ToolFrameworkMixin,
    ToolExecutionError,
    ToolValidationError
)
from src.core.base.common.models.communication_models import CascadeContext

class MockToolFrameworkMixin(ToolFrameworkMixin):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

class TestToolFramework:
    @pytest.fixture
    def tool_framework(self):
        return MockToolFrameworkMixin()
    @pytest.fixture
    def cascade_context(self):
        return CascadeContext(task_id="test_task", agent_id="test_agent", workflow_id="test_workflow")
    def test_initialization(self, tool_framework):
        assert tool_framework.registered_tools == {}
        assert tool_framework.tool_usage_stats == {}
        assert tool_framework.enable_tool_validation
        assert tool_framework.max_tool_execution_time == 300
    def test_create_tool_decorator(self, tool_framework):
        @tool_framework.create_tool(tool_id="test_tool", description="A test tool", category="test")
        async def test_function(param1: str, param2: int = 42, cascade_context=None):
            return f"Result: {param1}, {param2}"
        assert "test_tool" in tool_framework.registered_tools
        tool_def = tool_framework.registered_tools["test_tool"]
        assert tool_def.id == "test_tool"
        assert tool_def.description == "A test tool"
        assert tool_def.category == "test"
        assert len(tool_def.parameters) == 2
        param1 = next(p for p in tool_def.parameters if p.name == "param1")
        assert param1.type == "string"
        assert param1.required
        param2 = next(p for p in tool_def.parameters if p.name == "param2")
        assert param2.type == "integer"
        assert not param2.required
        assert param2.default == 42
    @pytest.mark.asyncio
    async def test_execute_tool_success(self, tool_framework, cascade_context):
        @tool_framework.create_tool(tool_id="success_tool", description="A successful tool")
        async def success_function(value: str, cascade_context=None):
            return f"Processed: {value}"
        result = await tool_framework.execute_tool("success_tool", {"value": "test_input"}, cascade_context)
        assert result["success"]
        assert result["result"] == "Processed: test_input"
        assert result["tool_id"] == "success_tool"
        stats = tool_framework.tool_usage_stats["success_tool"]
        assert stats["calls"] == 1
        assert stats["successes"] == 1
        assert stats["failures"] == 0
    @pytest.mark.asyncio
    async def test_execute_tool_not_found(self, tool_framework, cascade_context):
        with pytest.raises(ToolExecutionError, match="Tool 'nonexistent' not found"):
            await tool_framework.execute_tool("nonexistent", {}, cascade_context)
    @pytest.mark.asyncio
    async def test_execute_tool_validation_error(self, tool_framework, cascade_context):
        @tool_framework.create_tool(tool_id="validation_tool", description="A tool with required params")
        async def validation_function(required_param: str, cascade_context=None):
            return f"Result: {required_param}"
        with pytest.raises(ToolValidationError, match="Missing required parameter"):
            await tool_framework.execute_tool("validation_tool", {}, cascade_context)
    @pytest.mark.asyncio
    async def test_execute_tool_execution_error(self, tool_framework, cascade_context):
        @tool_framework.create_tool(tool_id="error_tool", description="A tool that fails")
        async def error_function(cascade_context=None):
            raise ValueError("Tool execution failed")
        with pytest.raises(ToolExecutionError, match="Tool execution failed"):
            await tool_framework.execute_tool("error_tool", {}, cascade_context)
        stats = tool_framework.tool_usage_stats["error_tool"]
        assert stats["calls"] == 1
        assert stats["successes"] == 0
        assert stats["failures"] == 1
        assert "Tool execution failed" in stats["last_error"]
    @pytest.mark.asyncio
    async def test_execute_tool_timeout(self, tool_framework, cascade_context):
        tool_framework.max_tool_execution_time = 0.1
        @tool_framework.create_tool(tool_id="timeout_tool", description="A slow tool")
        async def slow_function(cascade_context=None):
            await asyncio.sleep(1)
            return "Should not reach here"
        with pytest.raises(ToolExecutionError, match="execution timed out"):
            await tool_framework.execute_tool("timeout_tool", {}, cascade_context)
    def test_get_tool_definitions(self, tool_framework):
        @tool_framework.create_tool(tool_id="tool1", description="First tool")
        async def tool1():
            pass
        @tool_framework.create_tool(tool_id="tool2", description="Second tool")
        async def tool2():
            pass
        definitions = tool_framework.get_tool_definitions()
        assert len(definitions) == 2
        assert "tool1" in definitions
        assert "tool2" in definitions
        assert definitions["tool1"]["description"] == "First tool"
    def test_get_tool_definition(self, tool_framework):
        @tool_framework.create_tool(tool_id="specific_tool", description="Specific tool")
        async def specific_tool():
            pass
        definition = tool_framework.get_tool_definition("specific_tool")
        assert definition is not None
        assert definition["id"] == "specific_tool"
        assert definition["description"] == "Specific tool"
        assert tool_framework.get_tool_definition("nonexistent") is None
    def test_unregister_tool(self, tool_framework):
        @tool_framework.create_tool(tool_id="removable_tool", description="Removable tool")
        async def removable_tool():
            pass
        assert "removable_tool" in tool_framework.registered_tools
        result = tool_framework.unregister_tool("removable_tool")
        assert result
        assert "removable_tool" not in tool_framework.registered_tools
        result = tool_framework.unregister_tool("nonexistent")
        assert not result
    def test_get_tool_stats(self, tool_framework):
        tool_framework.tool_usage_stats = {
            "tool1": {"calls": 5, "successes": 4, "failures": 1},
            "tool2": {"calls": 2, "successes": 2, "failures": 0}
        }
        stats = tool_framework.get_tool_stats()
        assert len(stats) == 2
        assert stats["tool1"]["calls"] == 5
        assert stats["tool2"]["successes"] == 2
    @pytest.mark.asyncio
    async def test_parameter_type_conversion(self, tool_framework):
        @tool_framework.create_tool(tool_id="type_conversion_tool", description="Tool for testing type conversion")
        async def type_conversion_tool(int_param: int, float_param: float, bool_param: bool, cascade_context=None):
            return {
                "int_param": int_param,
                "float_param": float_param,
                "bool_param": bool_param
            }
        result = asyncio.run(tool_framework.execute_tool(
            "type_conversion_tool",
            {
                "int_param": "42",
                "float_param": "3.14",
                "bool_param": "true"
            }
        ))
        assert result["success"]
        data = result["result"]
        assert data["int_param"] == 42
        assert data["float_param"] == 3.14
        assert data["bool_param"]
    @pytest.mark.asyncio
    async def test_validation_disabled(self, tool_framework):
        tool_framework.enable_tool_validation = False
        @tool_framework.create_tool(tool_id="no_validation_tool", description="Tool without validation")
        async def no_validation_tool(required_param: str, cascade_context=None):
            return f"Got: {required_param}"
        result = asyncio.run(tool_framework.execute_tool("no_validation_tool", {}))
        assert result["success"] == False
    def test_tool_definition_serialization(self, tool_framework):
        @tool_framework.create_tool(tool_id="serialization_tool", description="Tool for serialization test", category="test", version="2.0")
        async def serialization_tool():
            pass
        tool_def = tool_framework.registered_tools["serialization_tool"]
        data = tool_def.to_dict()
        assert data["id"] == "serialization_tool"
        assert data["description"] == "Tool for serialization test"
        assert data["category"] == "test"
        assert data["version"] == "2.0"
        assert "parameters" in data
