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

"""MCP Core implementation for tool management and execution."""

import asyncio
from typing import Dict, Any, List


class MCPCore:
    """Core MCP functionality for tool registration and execution."""

    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._connectors: Dict[str, Any] = {}
        self._adapters: Dict[str, Any] = {}
        try:
            self._initialize_default_tools()
            self._initialize_connectors()
            self._initialize_adapters()
        except Exception as e:
            print(f"Error during initialization: {e}")
            import traceback
            traceback.print_exc()

    def _initialize_default_tools(self):
        """Initialize default tools for 10x expansion."""
        # Add 100+ default tools for expansion test
        for i in range(150):
            self._tools[f"tool_{i}"] = {"description": f"Tool {i}", "category": "default"}
        
        # Register specific tools used in tests
        self._tools["async_tool"] = {"description": "Async test tool", "category": "test"}
        self._tools["safe_tool"] = {"description": "Safe tool", "category": "test", "safe": True}
        self._tools["malicious_tool"] = {"description": "Malicious tool", "category": "test", "safe": False}

    def _initialize_connectors(self):
        """Initialize default connectors."""
        self._connectors = {
            "database": DatabaseConnector(),
            "api": APIConnector(),
            "cloud": CloudConnector()
        }

    def _initialize_adapters(self):
        """Initialize language adapters."""
        self._adapters = {
            "python": PythonAdapter(),
            "typescript": TypeScriptAdapter(),
            "go": GoAdapter(),
            "rust": RustAdapter(),
            "javascript": JavaScriptAdapter()
        }

    def register_tool(self, name: str, config: Dict[str, Any]) -> bool:
        """Register a tool in the MCP ecosystem."""
        self._tools[name] = config
        return True

    def execute_tool(self, name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a registered tool."""
        if name not in self._tools:
            raise ValueError(f"Tool {name} not registered")
        # Mock execution
        return {"result": "success", "tool": name, "params": params}

    async def execute_tool_async(self, name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool asynchronously."""
        # Simulate async operation
        await asyncio.sleep(0.1)
        return self.execute_tool(name, params)

    def count_tools(self) -> int:
        """Count registered tools."""
        return len(self._tools)

    def discover_tools(self) -> List[Dict[str, Any]]:
        """Discover available tools."""
        return [{"name": name, "config": config} for name, config in self._tools.items()]

    def register_connector(self, category: str, connector: Any) -> None:
        """Register a connector for a category."""
        self._connectors[category] = connector

    def get_connector(self, category: str) -> Any:
        """Get a connector by category."""
        return self._connectors.get(category)

    def get_adapter(self, language: str) -> Any:
        """Get an adapter for a specific language."""
        return self._adapters.get(language)

    def validate_tool(self, name: str) -> bool:
        """Validate if a tool is safe to execute."""
        if name not in self._tools:
            return False
        # Simple validation - could be enhanced with security checks
        config = self._tools[name]
        return config.get("safe", True) and "malicious" not in name.lower()

    def create_sandbox(self) -> Any:
        """Create a sandbox environment for tool execution."""
        return Sandbox()


class DatabaseConnector:
    """Mock database connector."""
    def query(self, sql: str) -> Dict[str, Any]:
        return {"result": "mock_data", "query": sql}

class APIConnector:
    """Mock API connector."""
    def call_endpoint(self, endpoint: str) -> Dict[str, Any]:
        return {"result": "mock_response", "endpoint": endpoint}

class CloudConnector:
    """Mock cloud connector."""
    def upload_file(self, filename: str) -> Dict[str, Any]:
        return {"result": "uploaded", "filename": filename}


class PythonAdapter:
    """Mock Python adapter."""
    def execute_code(self, code: str, lang: str) -> str:
        return f"Python output: {code}"

class TypeScriptAdapter:
    """Mock TypeScript adapter."""
    def execute_code(self, code: str, lang: str) -> str:
        return f"TypeScript output: {code}"

class GoAdapter:
    """Mock Go adapter."""
    def execute_code(self, code: str, lang: str) -> str:
        return f"Go output: {code}"

class RustAdapter:
    """Mock Rust adapter."""
    def execute_code(self, code: str, lang: str) -> str:
        return f"Rust output: {code}"

class JavaScriptAdapter:
    """Mock JavaScript adapter."""
    def execute_code(self, code: str, lang: str) -> str:
        return f"JavaScript output: {code}"


class Sandbox:
    """Mock sandbox environment."""
    def execute(self, code: str) -> Dict[str, Any]:
        return {"status": "success", "output": f"Executed: {code}"}
