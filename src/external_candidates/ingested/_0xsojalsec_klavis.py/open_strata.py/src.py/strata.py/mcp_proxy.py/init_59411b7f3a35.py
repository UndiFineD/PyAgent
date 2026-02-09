# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-klavis\open-strata\src\strata\mcp_proxy\__init__.py
"""MCP Proxy module for connecting to and interacting with MCP servers."""

from .auth_provider import create_oauth_provider
from .client import MCPClient
from .transport import HTTPTransport, StdioTransport, Transport

__all__ = [
    "MCPClient",
    "StdioTransport",
    "HTTPTransport",
    "Transport",
    "create_oauth_provider",
]
