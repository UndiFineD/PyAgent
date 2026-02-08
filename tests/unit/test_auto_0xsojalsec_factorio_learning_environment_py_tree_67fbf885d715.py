
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_tree_67fbf885d715.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'render'), 'missing render'
assert hasattr(mod, 'render_shadow'), 'missing render_shadow'
assert hasattr(mod, 'get_key'), 'missing get_key'
assert hasattr(mod, 'get_size'), 'missing get_size'
assert hasattr(mod, 'get_tree_variant'), 'missing get_tree_variant'
assert hasattr(mod, 'is_tree_entity'), 'missing is_tree_entity'
assert hasattr(mod, 'build_available_trees_index'), 'missing build_available_trees_index'
