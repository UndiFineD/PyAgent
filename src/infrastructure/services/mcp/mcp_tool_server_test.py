# Auto-synced test for infrastructure/services/mcp/mcp_tool_server.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "mcp_tool_server.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "adapt_tool_schema"), "adapt_tool_schema missing"
    assert hasattr(mod, "create_mcp_session"), "create_mcp_session missing"
    assert hasattr(mod, "discover_mcp_servers"), "discover_mcp_servers missing"
    assert hasattr(mod, "MCPServerConfig"), "MCPServerConfig missing"
    assert hasattr(mod, "MCPServerType"), "MCPServerType missing"
    assert hasattr(mod, "ServerType"), "ServerType missing"
    assert hasattr(mod, "ToolStatus"), "ToolStatus missing"
    assert hasattr(mod, "SessionState"), "SessionState missing"
    assert hasattr(mod, "ToolSchema"), "ToolSchema missing"
    assert hasattr(mod, "ToolCall"), "ToolCall missing"
    assert hasattr(mod, "ToolResult"), "ToolResult missing"
    assert hasattr(mod, "MCPSession"), "MCPSession missing"
    assert hasattr(mod, "MCPToolServer"), "MCPToolServer missing"
    assert hasattr(mod, "SSEMCPServer"), "SSEMCPServer missing"
    assert hasattr(mod, "LocalMCPServer"), "LocalMCPServer missing"
    assert hasattr(mod, "SchemaAdapter"), "SchemaAdapter missing"
    assert hasattr(mod, "MCPServerRegistry"), "MCPServerRegistry missing"
    assert hasattr(mod, "SessionManager"), "SessionManager missing"

