
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentcloud_py_build_request_from_api_spec_778704d5caac.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'load_spec'), 'missing load_spec'
assert hasattr(mod, 'build_request'), 'missing build_request'
assert hasattr(mod, 'make_request'), 'missing make_request'
assert hasattr(mod, 'build_run_request'), 'missing build_run_request'
