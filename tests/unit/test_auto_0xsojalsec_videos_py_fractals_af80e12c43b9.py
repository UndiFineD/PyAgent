
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_fractals_af80e12c43b9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'rotate'), 'missing rotate'
assert hasattr(mod, 'fractalify'), 'missing fractalify'
assert hasattr(mod, 'fractalification_iteration'), 'missing fractalification_iteration'
assert hasattr(mod, 'SelfSimilarFractal'), 'missing SelfSimilarFractal'
assert hasattr(mod, 'Sierpinski'), 'missing Sierpinski'
assert hasattr(mod, 'DiamondFractal'), 'missing DiamondFractal'
assert hasattr(mod, 'PentagonalFractal'), 'missing PentagonalFractal'
assert hasattr(mod, 'PentagonalPiCreatureFractal'), 'missing PentagonalPiCreatureFractal'
assert hasattr(mod, 'PiCreatureFractal'), 'missing PiCreatureFractal'
assert hasattr(mod, 'WonkyHexagonFractal'), 'missing WonkyHexagonFractal'
assert hasattr(mod, 'CircularFractal'), 'missing CircularFractal'
assert hasattr(mod, 'JaggedCurvePiece'), 'missing JaggedCurvePiece'
assert hasattr(mod, 'FractalCurve'), 'missing FractalCurve'
assert hasattr(mod, 'LindenmayerCurve'), 'missing LindenmayerCurve'
assert hasattr(mod, 'SelfSimilarSpaceFillingCurve'), 'missing SelfSimilarSpaceFillingCurve'
assert hasattr(mod, 'HilbertCurve'), 'missing HilbertCurve'
assert hasattr(mod, 'HilbertCurve3D'), 'missing HilbertCurve3D'
assert hasattr(mod, 'PeanoCurve'), 'missing PeanoCurve'
assert hasattr(mod, 'TriangleFillingCurve'), 'missing TriangleFillingCurve'
assert hasattr(mod, 'HexagonFillingCurve'), 'missing HexagonFillingCurve'
assert hasattr(mod, 'UtahFillingCurve'), 'missing UtahFillingCurve'
assert hasattr(mod, 'FlowSnake'), 'missing FlowSnake'
assert hasattr(mod, 'SierpinskiCurve'), 'missing SierpinskiCurve'
assert hasattr(mod, 'KochSnowFlake'), 'missing KochSnowFlake'
assert hasattr(mod, 'KochCurve'), 'missing KochCurve'
assert hasattr(mod, 'QuadraticKoch'), 'missing QuadraticKoch'
assert hasattr(mod, 'QuadraticKochIsland'), 'missing QuadraticKochIsland'
assert hasattr(mod, 'StellarCurve'), 'missing StellarCurve'
assert hasattr(mod, 'SnakeCurve'), 'missing SnakeCurve'
