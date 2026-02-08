
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_builder_9724bc70ddd0.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'IdentityMap'), 'missing IdentityMap'
assert hasattr(mod, 'SimpleResBlock'), 'missing SimpleResBlock'
assert hasattr(mod, 'build_vision_projector'), 'missing build_vision_projector'
