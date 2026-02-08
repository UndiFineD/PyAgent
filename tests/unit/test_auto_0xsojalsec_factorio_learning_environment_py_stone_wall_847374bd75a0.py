
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_stone_wall_847374bd75a0.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'render'), 'missing render'
assert hasattr(mod, 'render_shadow'), 'missing render_shadow'
assert hasattr(mod, 'get_name'), 'missing get_name'
assert hasattr(mod, 'get_key'), 'missing get_key'
assert hasattr(mod, 'get_around'), 'missing get_around'
assert hasattr(mod, 'is_stone_wall'), 'missing is_stone_wall'
assert hasattr(mod, 'is_gate'), 'missing is_gate'
assert hasattr(mod, 'get_size'), 'missing get_size'
