
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_nested_meta_agent_tool_fe09374ddb7e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_chain'), 'missing get_chain'
assert hasattr(mod, 'ChainTool'), 'missing ChainTool'
