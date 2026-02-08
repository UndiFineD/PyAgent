
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_tools_fdc665cec910.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_nested_classes'), 'missing get_nested_classes'
assert hasattr(mod, 'get_tools'), 'missing get_tools'
