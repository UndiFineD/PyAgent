
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_simple_math_tool_75d3043a2838.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AddTool'), 'missing AddTool'
assert hasattr(mod, 'SubtractTool'), 'missing SubtractTool'
assert hasattr(mod, 'MultiplyTool'), 'missing MultiplyTool'
assert hasattr(mod, 'DivideTool'), 'missing DivideTool'
