
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_context_archive_utils_4f7aea64203f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_current_context_archive'), 'missing get_current_context_archive'
assert hasattr(mod, 'update_context_archive'), 'missing update_context_archive'
