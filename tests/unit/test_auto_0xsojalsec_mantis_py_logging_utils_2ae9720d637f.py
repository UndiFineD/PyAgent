
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mantis_py_logging_utils_2ae9720d637f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CustomFormatter'), 'missing CustomFormatter'
assert hasattr(mod, 'LoggingConfig'), 'missing LoggingConfig'
