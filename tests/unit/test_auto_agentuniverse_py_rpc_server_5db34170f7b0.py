
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_rpc_server_5db34170f7b0.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'service_run'), 'missing service_run'
assert hasattr(mod, 'service_run_async'), 'missing service_run_async'
assert hasattr(mod, 'service_run_result'), 'missing service_run_result'
