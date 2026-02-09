# Extracted from: C:\DEV\PyAgent\.external\code_puppy\code_puppy\command_line\mcp\__init__.py
"""
MCP Command Line Interface - Namespace package for MCP server management commands.

This package provides a modular command interface for managing MCP servers.
Each command is implemented in its own module for better maintainability.
"""

from .handler import MCPCommandHandler

__all__ = ["MCPCommandHandler"]
