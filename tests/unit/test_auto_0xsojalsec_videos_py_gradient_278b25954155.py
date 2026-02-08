
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_gradient_278b25954155.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'GradientDescentWrapper'), 'missing GradientDescentWrapper'
assert hasattr(mod, 'ShowSimpleMultivariableFunction'), 'missing ShowSimpleMultivariableFunction'
assert hasattr(mod, 'ShowGraphWithVectors'), 'missing ShowGraphWithVectors'
assert hasattr(mod, 'ShowFunction'), 'missing ShowFunction'
assert hasattr(mod, 'ShowExampleFunctionGraph'), 'missing ShowExampleFunctionGraph'
assert hasattr(mod, 'ShowGradient'), 'missing ShowGradient'
assert hasattr(mod, 'ExampleGraphHoldXConstant'), 'missing ExampleGraphHoldXConstant'
assert hasattr(mod, 'ExampleGraphHoldYConstant'), 'missing ExampleGraphHoldYConstant'
assert hasattr(mod, 'TakePartialDerivatives'), 'missing TakePartialDerivatives'
assert hasattr(mod, 'ShowDerivativeAtExamplePoint'), 'missing ShowDerivativeAtExamplePoint'
