
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_wayback_google_analytics_py_codes_1a5fdbfa186c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_UA_code'), 'missing get_UA_code'
assert hasattr(mod, 'get_GA_code'), 'missing get_GA_code'
assert hasattr(mod, 'get_GTM_code'), 'missing get_GTM_code'
