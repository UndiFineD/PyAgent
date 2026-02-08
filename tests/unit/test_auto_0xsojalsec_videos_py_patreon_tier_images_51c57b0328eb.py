
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_patreon_tier_images_51c57b0328eb.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CircleDivisionImage'), 'missing CircleDivisionImage'
assert hasattr(mod, 'PatronImage1'), 'missing PatronImage1'
assert hasattr(mod, 'PatronImage2'), 'missing PatronImage2'
assert hasattr(mod, 'PatronImage4'), 'missing PatronImage4'
assert hasattr(mod, 'PatronImage8'), 'missing PatronImage8'
assert hasattr(mod, 'PatronImage16'), 'missing PatronImage16'
assert hasattr(mod, 'PatronImage31'), 'missing PatronImage31'
assert hasattr(mod, 'PatronImage57'), 'missing PatronImage57'
assert hasattr(mod, 'PatronImage99'), 'missing PatronImage99'
assert hasattr(mod, 'PatronImage163'), 'missing PatronImage163'
assert hasattr(mod, 'PatronImage256'), 'missing PatronImage256'
