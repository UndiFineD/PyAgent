
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_praisonai_py_database_config_1a14940215c0.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'should_force_sqlite'), 'missing should_force_sqlite'
assert hasattr(mod, 'get_database_url_with_sqlite_override'), 'missing get_database_url_with_sqlite_override'
assert hasattr(mod, 'get_database_config_for_sqlalchemy'), 'missing get_database_config_for_sqlalchemy'
