# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-roampal\ui-implementation\src-tauri\backend\modules\mcp\__init__.py
"""
MCP support modules for Roampal
Enables external LLMs to learn and contribute to memory like internal LLM
"""

from .client_detector import detect_mcp_client, get_auto_session_id
from .session_manager import MCPSessionManager

__all__ = ["MCPSessionManager", "detect_mcp_client", "get_auto_session_id"]
