
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_wappalyzer_next_py_matcher_aa6056cc8d37.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'group_or_literal'), 'missing group_or_literal'
assert hasattr(mod, 'get_version'), 'missing get_version'
assert hasattr(mod, 'parse_pattern'), 'missing parse_pattern'
assert hasattr(mod, 'single_match'), 'missing single_match'
assert hasattr(mod, 'match'), 'missing match'
assert hasattr(mod, 'match_dict'), 'missing match_dict'
