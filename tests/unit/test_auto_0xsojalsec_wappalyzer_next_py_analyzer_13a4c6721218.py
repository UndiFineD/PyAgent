
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_wappalyzer_next_py_analyzer_13a4c6721218.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'process_scripts'), 'missing process_scripts'
assert hasattr(mod, 'analyze_from_response'), 'missing analyze_from_response'
assert hasattr(mod, 'http_scan'), 'missing http_scan'
