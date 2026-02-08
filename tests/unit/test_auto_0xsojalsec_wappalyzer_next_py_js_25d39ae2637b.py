
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_wappalyzer_next_py_js_25d39ae2637b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'fix_keys'), 'missing fix_keys'
assert hasattr(mod, 'match_js'), 'missing match_js'
