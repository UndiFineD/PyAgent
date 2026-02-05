
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xSojalSec_klavis_errors.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ToolExecutionError'), 'missing ToolExecutionError'
assert hasattr(mod, 'RetryableToolError'), 'missing RetryableToolError'
assert hasattr(mod, 'AuthenticationError'), 'missing AuthenticationError'
assert hasattr(mod, 'TokenExpiredError'), 'missing TokenExpiredError'
assert hasattr(mod, 'InvalidTokenError'), 'missing InvalidTokenError'
