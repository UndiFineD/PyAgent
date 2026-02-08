
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\abdarwish23_advanced_sql_agent_py_sql_executor_service_8ffcb473ba08.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'execute_sql'), 'missing execute_sql'
assert hasattr(mod, 'execute_sql_reflection'), 'missing execute_sql_reflection'
assert hasattr(mod, 'execute_sql_corrected'), 'missing execute_sql_corrected'
