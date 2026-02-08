
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_malwoverview_py_colors_3eb7f63a98d0.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'mycolors'), 'missing mycolors'
assert hasattr(mod, 'printc'), 'missing printc'
assert hasattr(mod, 'printr'), 'missing printr'
