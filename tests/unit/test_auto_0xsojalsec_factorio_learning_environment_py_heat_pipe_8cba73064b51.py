
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_heat_pipe_8cba73064b51.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'render'), 'missing render'
assert hasattr(mod, 'render_shadow'), 'missing render_shadow'
assert hasattr(mod, 'get_key'), 'missing get_key'
assert hasattr(mod, 'get_around'), 'missing get_around'
assert hasattr(mod, 'is_heat_pipe'), 'missing is_heat_pipe'
assert hasattr(mod, 'is_entity'), 'missing is_entity'
assert hasattr(mod, 'is_entity_in_direction'), 'missing is_entity_in_direction'
assert hasattr(mod, 'get_size'), 'missing get_size'
