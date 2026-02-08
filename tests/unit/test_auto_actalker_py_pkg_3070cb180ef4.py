
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\actalker_py_pkg_3070cb180ef4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_obj_from_str'), 'missing get_obj_from_str'
assert hasattr(mod, 'instantiate_from_config'), 'missing instantiate_from_config'
