
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_sql_db_5214bf3c29d9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FakeTable'), 'missing FakeTable'
assert hasattr(mod, 'FakeDBInfo'), 'missing FakeDBInfo'
assert hasattr(mod, 'FakeSQLDatabase'), 'missing FakeSQLDatabase'
