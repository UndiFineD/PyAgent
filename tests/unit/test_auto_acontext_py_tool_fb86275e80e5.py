
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_tool_fb86275e80e5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FlagResponse'), 'missing FlagResponse'
assert hasattr(mod, 'InsertBlockResponse'), 'missing InsertBlockResponse'
assert hasattr(mod, 'ToolReferenceData'), 'missing ToolReferenceData'
assert hasattr(mod, 'ToolRenameItem'), 'missing ToolRenameItem'
