
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_show_proportion_7051b2294d8a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ProbabilityRect'), 'missing ProbabilityRect'
assert hasattr(mod, 'ChangeProbability'), 'missing ChangeProbability'
assert hasattr(mod, 'ShowProbAsProportion'), 'missing ShowProbAsProportion'
