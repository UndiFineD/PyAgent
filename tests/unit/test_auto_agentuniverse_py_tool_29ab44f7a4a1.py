
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_tool_29ab44f7a4a1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ToolInput'), 'missing ToolInput'
assert hasattr(mod, 'Tool'), 'missing Tool'
