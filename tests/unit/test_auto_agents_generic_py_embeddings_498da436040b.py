
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_embeddings_498da436040b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'EmbeddingData'), 'missing EmbeddingData'
assert hasattr(mod, 'create_embeddings'), 'missing create_embeddings'
