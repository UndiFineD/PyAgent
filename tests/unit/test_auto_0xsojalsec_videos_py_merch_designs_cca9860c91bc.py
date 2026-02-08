
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_merch_designs_cca9860c91bc.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ShowHilbertCurve'), 'missing ShowHilbertCurve'
assert hasattr(mod, 'ShowFlowSnake'), 'missing ShowFlowSnake'
assert hasattr(mod, 'FlippedSierpinski'), 'missing FlippedSierpinski'
assert hasattr(mod, 'ShowSierpinski'), 'missing ShowSierpinski'
assert hasattr(mod, 'SquareWave'), 'missing SquareWave'
assert hasattr(mod, 'PendulumPhaseSpace'), 'missing PendulumPhaseSpace'
