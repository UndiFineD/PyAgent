
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_agent_deps_f195bd795dd9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'set_global_tool_context'), 'missing set_global_tool_context'
assert hasattr(mod, 'get_meta_agent'), 'missing get_meta_agent'
