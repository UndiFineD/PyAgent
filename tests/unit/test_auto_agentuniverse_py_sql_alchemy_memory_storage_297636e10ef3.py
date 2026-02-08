
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_sql_alchemy_memory_storage_297636e10ef3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'BaseMemoryConverter'), 'missing BaseMemoryConverter'
assert hasattr(mod, 'create_memory_model'), 'missing create_memory_model'
assert hasattr(mod, 'DefaultMemoryConverter'), 'missing DefaultMemoryConverter'
assert hasattr(mod, 'SqlAlchemyMemoryStorage'), 'missing SqlAlchemyMemoryStorage'
