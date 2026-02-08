
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_withoutbg_py_core_1feec2abbfcb.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'remove_background'), 'missing remove_background'
assert hasattr(mod, 'remove_background_batch'), 'missing remove_background_batch'
