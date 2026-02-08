
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_fractal_charm_a867cc89acee.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FractalCreation'), 'missing FractalCreation'
assert hasattr(mod, 'PentagonalFractalCreation'), 'missing PentagonalFractalCreation'
assert hasattr(mod, 'DiamondFractalCreation'), 'missing DiamondFractalCreation'
assert hasattr(mod, 'PiCreatureFractalCreation'), 'missing PiCreatureFractalCreation'
assert hasattr(mod, 'QuadraticKochFractalCreation'), 'missing QuadraticKochFractalCreation'
assert hasattr(mod, 'KochSnowFlakeFractalCreation'), 'missing KochSnowFlakeFractalCreation'
assert hasattr(mod, 'WonkyHexagonFractalCreation'), 'missing WonkyHexagonFractalCreation'
assert hasattr(mod, 'SierpinskiFractalCreation'), 'missing SierpinskiFractalCreation'
assert hasattr(mod, 'CircularFractalCreation'), 'missing CircularFractalCreation'
