
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_wafer_py_utils_3049249129d6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'rndstr'), 'missing rndstr'
assert hasattr(mod, 'choice'), 'missing choice'
assert hasattr(mod, 'rndunicode'), 'missing rndunicode'
assert hasattr(mod, 'choice_percent'), 'missing choice_percent'
