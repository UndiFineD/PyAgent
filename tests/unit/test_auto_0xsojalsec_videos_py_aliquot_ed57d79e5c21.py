
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_aliquot_ed57d79e5c21.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_factors'), 'missing get_factors'
assert hasattr(mod, 'AmicableNumbers'), 'missing AmicableNumbers'
