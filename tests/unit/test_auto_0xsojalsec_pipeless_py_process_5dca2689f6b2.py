
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pipeless_py_process_5dca2689f6b2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'hook'), 'missing hook'
assert hasattr(mod, 'detect_gaze'), 'missing detect_gaze'
