
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_prompting_py_objects_025669e07d1b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Object'), 'missing Object'
assert hasattr(mod, 'Player'), 'missing Player'
assert hasattr(mod, 'Cow'), 'missing Cow'
assert hasattr(mod, 'Zombie'), 'missing Zombie'
assert hasattr(mod, 'Skeleton'), 'missing Skeleton'
assert hasattr(mod, 'Arrow'), 'missing Arrow'
assert hasattr(mod, 'Plant'), 'missing Plant'
assert hasattr(mod, 'Fence'), 'missing Fence'
