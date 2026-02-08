
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_complex_functions_4fe36b35b727.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'GeneralizeToComplexFunctions'), 'missing GeneralizeToComplexFunctions'
assert hasattr(mod, 'ClarifyInputAndOutput'), 'missing ClarifyInputAndOutput'
assert hasattr(mod, 'GraphForFlattenedPi'), 'missing GraphForFlattenedPi'
assert hasattr(mod, 'SimpleComplexExponentExample'), 'missing SimpleComplexExponentExample'
assert hasattr(mod, 'TRangingFrom0To1'), 'missing TRangingFrom0To1'
