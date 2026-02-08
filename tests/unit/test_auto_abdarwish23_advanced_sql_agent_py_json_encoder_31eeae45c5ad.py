
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\abdarwish23_advanced_sql_agent_py_json_encoder_31eeae45c5ad.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CustomJSONEncoder'), 'missing CustomJSONEncoder'
assert hasattr(mod, 'CustomJSONProvider'), 'missing CustomJSONProvider'
