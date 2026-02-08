
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_google_search_tool_v2_1b86f2dc2d31.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'GoogleSearchTool'), 'missing GoogleSearchTool'
assert hasattr(mod, 'GoogleScholarSearchTool'), 'missing GoogleScholarSearchTool'
