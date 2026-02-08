
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_ui_7353add73f71.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'extract_event_time_from_memory'), 'missing extract_event_time_from_memory'
assert hasattr(mod, 'ChatUI'), 'missing ChatUI'
