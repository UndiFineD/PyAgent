
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_name_animation_29e596ac1fb6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ComplexMorphingNames'), 'missing ComplexMorphingNames'
assert hasattr(mod, 'FlowNameAnimation'), 'missing FlowNameAnimation'
assert hasattr(mod, 'NameAnimationScene'), 'missing NameAnimationScene'
assert hasattr(mod, 'RotatingNameLetters'), 'missing RotatingNameLetters'
assert hasattr(mod, 'ModularMultiplicationNameAnimation'), 'missing ModularMultiplicationNameAnimation'
assert hasattr(mod, 'FourierNameAnimation'), 'missing FourierNameAnimation'
assert hasattr(mod, 'QuaternionNameAnimation'), 'missing QuaternionNameAnimation'
