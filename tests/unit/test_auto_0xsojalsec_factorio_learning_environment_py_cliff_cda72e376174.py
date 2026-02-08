
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_cliff_cda72e376174.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'render'), 'missing render'
assert hasattr(mod, 'render_shadow'), 'missing render_shadow'
assert hasattr(mod, 'get_orientation'), 'missing get_orientation'
assert hasattr(mod, 'determine_cliff_type_from_orientation'), 'missing determine_cliff_type_from_orientation'
assert hasattr(mod, 'parse_orientation'), 'missing parse_orientation'
assert hasattr(mod, 'get_cliff_sprite_name'), 'missing get_cliff_sprite_name'
assert hasattr(mod, 'get_key'), 'missing get_key'
assert hasattr(mod, 'get_size'), 'missing get_size'
