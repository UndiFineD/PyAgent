
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_whisperlivekit_py_eow_detection_a1ef278f61fd.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'load_cif'), 'missing load_cif'
assert hasattr(mod, 'resize'), 'missing resize'
assert hasattr(mod, 'fire_at_boundary'), 'missing fire_at_boundary'
