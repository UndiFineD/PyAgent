
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_x_anylabeling_server_py_middleware_079a82353bee.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'APIKeyMiddleware'), 'missing APIKeyMiddleware'
assert hasattr(mod, 'RequestLoggingMiddleware'), 'missing RequestLoggingMiddleware'
assert hasattr(mod, 'setup_cors'), 'missing setup_cors'
