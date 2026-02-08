
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentuniverse_py_es_conversation_memory_storage_f088c3b4a550.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ElasticsearchMemoryStorage'), 'missing ElasticsearchMemoryStorage'
assert hasattr(mod, 'DefaultMemoryConverter'), 'missing DefaultMemoryConverter'
