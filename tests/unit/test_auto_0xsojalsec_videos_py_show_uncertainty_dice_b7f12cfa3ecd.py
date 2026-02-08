
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_show_uncertainty_dice_b7f12cfa3ecd.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ShowUncertaintyDice'), 'missing ShowUncertaintyDice'
assert hasattr(mod, 'IdealizedDieHistogram'), 'missing IdealizedDieHistogram'
