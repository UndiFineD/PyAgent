
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentcloud_py_queries_b7e43709a62e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MongoClientConnection'), 'missing MongoClientConnection'
assert hasattr(mod, 'convert_id_to_ObjectId'), 'missing convert_id_to_ObjectId'
