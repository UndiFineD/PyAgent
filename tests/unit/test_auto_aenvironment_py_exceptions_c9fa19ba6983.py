
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\aenvironment_py_exceptions_c9fa19ba6983.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AEnvError'), 'missing AEnvError'
assert hasattr(mod, 'ToolError'), 'missing ToolError'
assert hasattr(mod, 'EnvironmentError'), 'missing EnvironmentError'
assert hasattr(mod, 'ToolTimeoutError'), 'missing ToolTimeoutError'
assert hasattr(mod, 'ToolServerError'), 'missing ToolServerError'
assert hasattr(mod, 'NetworkError'), 'missing NetworkError'
assert hasattr(mod, 'ValidationError'), 'missing ValidationError'
