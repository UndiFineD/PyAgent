
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_transport_belt_9c8d0054517c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'render'), 'missing render'
assert hasattr(mod, 'render_shadow'), 'missing render_shadow'
assert hasattr(mod, 'render_inventory'), 'missing render_inventory'
assert hasattr(mod, 'render_inventory2'), 'missing render_inventory2'
assert hasattr(mod, 'get_key'), 'missing get_key'
assert hasattr(mod, 'get_around'), 'missing get_around'
assert hasattr(mod, 'is_transport_belt'), 'missing is_transport_belt'
assert hasattr(mod, 'is_splitter'), 'missing is_splitter'
assert hasattr(mod, 'get_size'), 'missing get_size'
