
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_memory_utils_13e09bd29817.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ensure_mongo_beanie_ready'), 'missing ensure_mongo_beanie_ready'
assert hasattr(mod, 'query_all_groups_from_mongodb'), 'missing query_all_groups_from_mongodb'
assert hasattr(mod, 'query_memcells_by_group_and_time'), 'missing query_memcells_by_group_and_time'
assert hasattr(mod, 'serialize_datetime'), 'missing serialize_datetime'
