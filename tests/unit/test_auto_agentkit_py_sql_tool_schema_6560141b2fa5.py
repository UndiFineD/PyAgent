
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_sql_tool_schema_6560141b2fa5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'TableInfo'), 'missing TableInfo'
assert hasattr(mod, 'DatabaseInfo'), 'missing DatabaseInfo'
assert hasattr(mod, 'ExecutionResult'), 'missing ExecutionResult'
