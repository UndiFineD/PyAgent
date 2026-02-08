
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\aenvironment_py_mcp_tool_1ac6171f282c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'register_tool'), 'missing register_tool'
assert hasattr(mod, '_generate_mcp_schema'), 'missing _generate_mcp_schema'
assert hasattr(mod, 'create_mcp_server'), 'missing create_mcp_server'
