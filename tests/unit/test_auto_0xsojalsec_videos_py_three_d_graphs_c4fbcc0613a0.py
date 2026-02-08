
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_three_d_graphs_c4fbcc0613a0.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ShowLinearity'), 'missing ShowLinearity'
assert hasattr(mod, 'CombineSeveralSolutions'), 'missing CombineSeveralSolutions'
assert hasattr(mod, 'CycleThroughManyLinearCombinations'), 'missing CycleThroughManyLinearCombinations'
