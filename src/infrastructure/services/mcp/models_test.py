# Auto-synced test for infrastructure/services/mcp/models.py
import importlib.util
import pathlib


def _load_module():
    p = pathlib.Path(__file__).parent / "models.py"
    spec = importlib.util.spec_from_file_location("_mod_under_test", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_imports_and_symbols():
    mod = _load_module()
    assert hasattr(mod, "MCPServerType"), "MCPServerType missing"
    assert hasattr(mod, "ToolStatus"), "ToolStatus missing"
    assert hasattr(mod, "SessionState"), "SessionState missing"
    assert hasattr(mod, "MCPServerConfig"), "MCPServerConfig missing"
    assert hasattr(mod, "ToolSchema"), "ToolSchema missing"
    assert hasattr(mod, "ToolCall"), "ToolCall missing"
    assert hasattr(mod, "ToolResult"), "ToolResult missing"
    assert hasattr(mod, "MCPSession"), "MCPSession missing"

