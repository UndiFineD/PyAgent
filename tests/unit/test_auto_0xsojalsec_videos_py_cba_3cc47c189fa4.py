
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_cba_3cc47c189fa4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'EnumerableSaveScene'), 'missing EnumerableSaveScene'
assert hasattr(mod, 'LayersOfAbstraction'), 'missing LayersOfAbstraction'
assert hasattr(mod, 'DifferenceOfSquares'), 'missing DifferenceOfSquares'
assert hasattr(mod, 'Lightbulbs'), 'missing Lightbulbs'
assert hasattr(mod, 'LayersOfLightbulbs'), 'missing LayersOfLightbulbs'
assert hasattr(mod, 'Test'), 'missing Test'
