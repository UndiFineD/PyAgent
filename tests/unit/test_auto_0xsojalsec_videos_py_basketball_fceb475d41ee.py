
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_basketball_fceb475d41ee.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'year_to_file_name'), 'missing year_to_file_name'
assert hasattr(mod, 'load_data'), 'missing load_data'
assert hasattr(mod, 'get_dots'), 'missing get_dots'
assert hasattr(mod, 'get_bars'), 'missing get_bars'
assert hasattr(mod, 'ShotHistory'), 'missing ShotHistory'
