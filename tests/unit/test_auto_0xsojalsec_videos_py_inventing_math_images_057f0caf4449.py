
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_inventing_math_images_057f0caf4449.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SimpleText'), 'missing SimpleText'
assert hasattr(mod, 'SimpleTex'), 'missing SimpleTex'
assert hasattr(mod, 'OneMinusOnePoem'), 'missing OneMinusOnePoem'
assert hasattr(mod, 'DivergentSum'), 'missing DivergentSum'
assert hasattr(mod, 'PowersOfTwoSmall'), 'missing PowersOfTwoSmall'
assert hasattr(mod, 'FinalSlide'), 'missing FinalSlide'
