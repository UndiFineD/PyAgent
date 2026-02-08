
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_footnote_80352d475e0e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'OpeningQuote'), 'missing OpeningQuote'
assert hasattr(mod, 'QuickFootnote'), 'missing QuickFootnote'
assert hasattr(mod, 'PeakOutsideFlatland'), 'missing PeakOutsideFlatland'
assert hasattr(mod, 'SymbolicThreeDTransform'), 'missing SymbolicThreeDTransform'
assert hasattr(mod, 'ThreeDLinearTransformExample'), 'missing ThreeDLinearTransformExample'
assert hasattr(mod, 'SingleVectorToOutput'), 'missing SingleVectorToOutput'
assert hasattr(mod, 'InputWordOutputWord'), 'missing InputWordOutputWord'
assert hasattr(mod, 'TransformOnlyBasisVectors'), 'missing TransformOnlyBasisVectors'
assert hasattr(mod, 'IHatJHatKHatWritten'), 'missing IHatJHatKHatWritten'
assert hasattr(mod, 'PutTogether3x3Matrix'), 'missing PutTogether3x3Matrix'
assert hasattr(mod, 'RotateSpaceAboutYAxis'), 'missing RotateSpaceAboutYAxis'
assert hasattr(mod, 'RotateOnlyBasisVectorsAboutYAxis'), 'missing RotateOnlyBasisVectorsAboutYAxis'
assert hasattr(mod, 'PutTogetherRotationMatrix'), 'missing PutTogetherRotationMatrix'
assert hasattr(mod, 'ScaleAndAddBeforeTransformation'), 'missing ScaleAndAddBeforeTransformation'
assert hasattr(mod, 'ShowVCoordinateMeaning'), 'missing ShowVCoordinateMeaning'
assert hasattr(mod, 'ScaleAndAddAfterTransformation'), 'missing ScaleAndAddAfterTransformation'
assert hasattr(mod, 'ShowVCoordinateMeaningAfterTransform'), 'missing ShowVCoordinateMeaningAfterTransform'
assert hasattr(mod, 'ShowMatrixVectorMultiplication'), 'missing ShowMatrixVectorMultiplication'
assert hasattr(mod, 'ShowMatrixMultiplication'), 'missing ShowMatrixMultiplication'
assert hasattr(mod, 'ApplyTwoSuccessiveTransforms'), 'missing ApplyTwoSuccessiveTransforms'
assert hasattr(mod, 'ComputerGraphicsAndRobotics'), 'missing ComputerGraphicsAndRobotics'
assert hasattr(mod, 'ThreeDRotation'), 'missing ThreeDRotation'
assert hasattr(mod, 'ThreeDRotationBrokenUp'), 'missing ThreeDRotationBrokenUp'
assert hasattr(mod, 'SymbolicTwoDToThreeDTransform'), 'missing SymbolicTwoDToThreeDTransform'
assert hasattr(mod, 'SymbolicThreeDToTwoDTransform'), 'missing SymbolicThreeDToTwoDTransform'
assert hasattr(mod, 'QuestionsToPonder'), 'missing QuestionsToPonder'
assert hasattr(mod, 'NextVideo'), 'missing NextVideo'
