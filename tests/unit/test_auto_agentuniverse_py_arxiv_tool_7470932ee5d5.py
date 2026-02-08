
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_arxiv_tool_7470932ee5d5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SearchMode'), 'missing SearchMode'
assert hasattr(mod, 'PaperSummary'), 'missing PaperSummary'
assert hasattr(mod, 'ArxivTool'), 'missing ArxivTool'
