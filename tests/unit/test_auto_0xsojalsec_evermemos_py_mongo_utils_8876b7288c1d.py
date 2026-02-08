
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_mongo_utils_8876b7288c1d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'generate_object_id'), 'missing generate_object_id'
assert hasattr(mod, 'generate_object_id_str'), 'missing generate_object_id_str'
