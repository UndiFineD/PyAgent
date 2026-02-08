
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_web_util_53cdd2819e3e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FlaskServerManager'), 'missing FlaskServerManager'
assert hasattr(mod, 'request_param'), 'missing request_param'
assert hasattr(mod, 'service_run_queue'), 'missing service_run_queue'
assert hasattr(mod, 'agent_run_queue'), 'missing agent_run_queue'
assert hasattr(mod, 'async_agent_run_queue'), 'missing async_agent_run_queue'
assert hasattr(mod, 'make_standard_response'), 'missing make_standard_response'
