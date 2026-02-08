
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_footnote2_c6675a93d91b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'OpeningQuote'), 'missing OpeningQuote'
assert hasattr(mod, 'AnotherFootnote'), 'missing AnotherFootnote'
assert hasattr(mod, 'ColumnsRepresentBasisVectors'), 'missing ColumnsRepresentBasisVectors'
assert hasattr(mod, 'Symbolic2To3DTransform'), 'missing Symbolic2To3DTransform'
assert hasattr(mod, 'PlaneStartState'), 'missing PlaneStartState'
assert hasattr(mod, 'OutputIn3dWords'), 'missing OutputIn3dWords'
assert hasattr(mod, 'OutputIn3d'), 'missing OutputIn3d'
assert hasattr(mod, 'ShowSideBySide2dTo3d'), 'missing ShowSideBySide2dTo3d'
assert hasattr(mod, 'AnimationLaziness'), 'missing AnimationLaziness'
assert hasattr(mod, 'DescribeColumnsInSpecificTransformation'), 'missing DescribeColumnsInSpecificTransformation'
assert hasattr(mod, 'CountRowsAndColumns'), 'missing CountRowsAndColumns'
assert hasattr(mod, 'WriteColumnSpaceDefinition'), 'missing WriteColumnSpaceDefinition'
assert hasattr(mod, 'MatrixInTheWild'), 'missing MatrixInTheWild'
assert hasattr(mod, 'ThreeDToTwoDInput'), 'missing ThreeDToTwoDInput'
assert hasattr(mod, 'ThreeDToTwoDInputWords'), 'missing ThreeDToTwoDInputWords'
assert hasattr(mod, 'ThreeDToTwoDOutput'), 'missing ThreeDToTwoDOutput'
assert hasattr(mod, 'ThreeDToTwoDSideBySide'), 'missing ThreeDToTwoDSideBySide'
assert hasattr(mod, 'Symbolic2To1DTransform'), 'missing Symbolic2To1DTransform'
assert hasattr(mod, 'TwoDTo1DTransform'), 'missing TwoDTo1DTransform'
assert hasattr(mod, 'TwoDTo1DTransformWithDots'), 'missing TwoDTo1DTransformWithDots'
assert hasattr(mod, 'NextVideo'), 'missing NextVideo'
assert hasattr(mod, 'DotProductPreview'), 'missing DotProductPreview'
