
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_withoutbg_py_exceptions_033ffbd24ee1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'WithoutBGError'), 'missing WithoutBGError'
assert hasattr(mod, 'ModelNotFoundError'), 'missing ModelNotFoundError'
assert hasattr(mod, 'APIError'), 'missing APIError'
assert hasattr(mod, 'InvalidImageError'), 'missing InvalidImageError'
assert hasattr(mod, 'ConfigurationError'), 'missing ConfigurationError'
