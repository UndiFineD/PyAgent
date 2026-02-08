
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_base_f89801942765.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'VectorRecord'), 'missing VectorRecord'
assert hasattr(mod, 'VectorDBQuery'), 'missing VectorDBQuery'
assert hasattr(mod, 'VectorDBQueryResult'), 'missing VectorDBQueryResult'
assert hasattr(mod, 'VectorDBStatus'), 'missing VectorDBStatus'
assert hasattr(mod, 'BaseVectorStorage'), 'missing BaseVectorStorage'
