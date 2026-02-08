
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_jacobian_animations_0345eba055a8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ExampleLinearTransformation'), 'missing ExampleLinearTransformation'
assert hasattr(mod, 'example_function'), 'missing example_function'
assert hasattr(mod, 'ExampleMultivariableFunction'), 'missing ExampleMultivariableFunction'
assert hasattr(mod, 'ExampleMultivariableFunctionWithZoom'), 'missing ExampleMultivariableFunctionWithZoom'
assert hasattr(mod, 'ExampleMultivariableFunctionWithMuchZoom'), 'missing ExampleMultivariableFunctionWithMuchZoom'
assert hasattr(mod, 'ExampleDeterminantAnimation'), 'missing ExampleDeterminantAnimation'
assert hasattr(mod, 'JacobianDeterminantAnimation'), 'missing JacobianDeterminantAnimation'
assert hasattr(mod, 'SmallJacobianDeterminant'), 'missing SmallJacobianDeterminant'
