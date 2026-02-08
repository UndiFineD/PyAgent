
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_utils_0a168bcb3e4b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'group_tool_calls'), 'missing group_tool_calls'
assert hasattr(mod, '_ChatItemGroup'), 'missing _ChatItemGroup'
