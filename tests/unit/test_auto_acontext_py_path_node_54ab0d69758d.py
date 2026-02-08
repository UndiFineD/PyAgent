
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_path_node_54ab0d69758d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PathNode'), 'missing PathNode'
assert hasattr(mod, 'repr_path_tree'), 'missing repr_path_tree'
