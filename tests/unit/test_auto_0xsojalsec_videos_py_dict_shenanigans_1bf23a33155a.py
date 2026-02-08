
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_dict_shenanigans_1bf23a33155a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'filtered_locals'), 'missing filtered_locals'
assert hasattr(mod, 'digest_config'), 'missing digest_config'
assert hasattr(mod, 'digest_locals'), 'missing digest_locals'
assert hasattr(mod, 'DictAsObject'), 'missing DictAsObject'
assert hasattr(mod, 'get_all_descendent_classes'), 'missing get_all_descendent_classes'
