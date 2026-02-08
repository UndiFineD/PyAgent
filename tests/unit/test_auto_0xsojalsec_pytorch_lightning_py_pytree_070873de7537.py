
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_pytree_070873de7537.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_is_leaf_or_primitive_container'), 'missing _is_leaf_or_primitive_container'
assert hasattr(mod, '_tree_flatten'), 'missing _tree_flatten'
assert hasattr(mod, '_map_and_unflatten'), 'missing _map_and_unflatten'
