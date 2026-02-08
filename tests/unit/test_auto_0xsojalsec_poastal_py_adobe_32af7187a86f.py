
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_poastal_py_adobe_32af7187a86f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'adobe_email'), 'missing adobe_email'
assert hasattr(mod, 'adobe_facebook_email'), 'missing adobe_facebook_email'
