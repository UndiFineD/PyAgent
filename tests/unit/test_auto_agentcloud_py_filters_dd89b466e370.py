
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentcloud_py_filters_dd89b466e370.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'create_pinecone_filters'), 'missing create_pinecone_filters'
assert hasattr(mod, 'create_qdrant_filters'), 'missing create_qdrant_filters'
