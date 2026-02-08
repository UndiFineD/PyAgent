
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_sudanese_band_a9a56d89d921.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'stereo_project_point'), 'missing stereo_project_point'
assert hasattr(mod, 'sudanese_band_func'), 'missing sudanese_band_func'
assert hasattr(mod, 'mobius_strip_func'), 'missing mobius_strip_func'
assert hasattr(mod, 'reversed_band'), 'missing reversed_band'
assert hasattr(mod, 'get_full_surface'), 'missing get_full_surface'
assert hasattr(mod, 'get_sudanese_band'), 'missing get_sudanese_band'
assert hasattr(mod, 'SudaneseBand'), 'missing SudaneseBand'
assert hasattr(mod, 'SudaneseBandToKleinBottle'), 'missing SudaneseBandToKleinBottle'
