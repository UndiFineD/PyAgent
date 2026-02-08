
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_wappalyzer_next_py_analyzer_5630e6eb9524.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DriverPool'), 'missing DriverPool'
assert hasattr(mod, 'cookie_to_cookies'), 'missing cookie_to_cookies'
assert hasattr(mod, 'process_url'), 'missing process_url'
assert hasattr(mod, 'merge_technologies'), 'missing merge_technologies'
