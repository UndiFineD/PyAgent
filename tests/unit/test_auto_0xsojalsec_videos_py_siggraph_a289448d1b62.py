
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_siggraph_a289448d1b62.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ThreePis'), 'missing ThreePis'
assert hasattr(mod, 'PendulumAxes'), 'missing PendulumAxes'
assert hasattr(mod, 'InterpolatingOrientations'), 'missing InterpolatingOrientations'
assert hasattr(mod, 'InterpolatingOrientationsWithQuaternions'), 'missing InterpolatingOrientationsWithQuaternions'
assert hasattr(mod, 'FirstStepIsToCare'), 'missing FirstStepIsToCare'
assert hasattr(mod, 'NeverNeeded'), 'missing NeverNeeded'
assert hasattr(mod, 'Thanks'), 'missing Thanks'
