
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_prettymapp_py_plotting_f79ea3790e9f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Plot'), 'missing Plot'
assert hasattr(mod, 'adjust_lightness'), 'missing adjust_lightness'
