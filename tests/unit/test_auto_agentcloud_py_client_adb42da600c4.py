
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentcloud_py_client_adb42da600c4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'process'), 'missing process'
assert hasattr(mod, 'consume_tasks'), 'missing consume_tasks'
assert hasattr(mod, 'backoff'), 'missing backoff'
assert hasattr(mod, 'execute_task'), 'missing execute_task'
assert hasattr(mod, 'execute_chat_task'), 'missing execute_chat_task'
