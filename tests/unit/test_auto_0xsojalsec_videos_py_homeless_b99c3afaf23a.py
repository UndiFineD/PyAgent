
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_homeless_b99c3afaf23a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Cycloidify'), 'missing Cycloidify'
assert hasattr(mod, 'PythagoreanTransformation'), 'missing PythagoreanTransformation'
assert hasattr(mod, 'PullCurveStraight'), 'missing PullCurveStraight'
assert hasattr(mod, 'StraghtenCircle'), 'missing StraghtenCircle'
assert hasattr(mod, 'SingleVariableFunc'), 'missing SingleVariableFunc'
assert hasattr(mod, 'MultivariableFunc'), 'missing MultivariableFunc'
assert hasattr(mod, 'prime_factors'), 'missing prime_factors'
assert hasattr(mod, 'ShowSumOfSquaresPattern'), 'missing ShowSumOfSquaresPattern'
