
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_various_intro_visuals_e6ca1f9a7a95.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'RandyFlipsAndStacks'), 'missing RandyFlipsAndStacks'
assert hasattr(mod, 'TwoDiceTableScene'), 'missing TwoDiceTableScene'
assert hasattr(mod, 'VisualCovariance'), 'missing VisualCovariance'
assert hasattr(mod, 'BinaryChoices'), 'missing BinaryChoices'
