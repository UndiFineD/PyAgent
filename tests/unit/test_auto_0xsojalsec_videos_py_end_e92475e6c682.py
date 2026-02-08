
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_end_e92475e6c682.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DontLearnFromSymbols'), 'missing DontLearnFromSymbols'
assert hasattr(mod, 'NotationReflectsMath'), 'missing NotationReflectsMath'
assert hasattr(mod, 'AsymmetriesInTheMath'), 'missing AsymmetriesInTheMath'
assert hasattr(mod, 'AddedVsOplussed'), 'missing AddedVsOplussed'
assert hasattr(mod, 'ReciprocalTop'), 'missing ReciprocalTop'
assert hasattr(mod, 'NotSymbolicPatterns'), 'missing NotSymbolicPatterns'
assert hasattr(mod, 'ChangeWeCanBelieveIn'), 'missing ChangeWeCanBelieveIn'
assert hasattr(mod, 'TriangleOfPowerIsBetter'), 'missing TriangleOfPowerIsBetter'
assert hasattr(mod, 'InYourOwnNotes'), 'missing InYourOwnNotes'
assert hasattr(mod, 'Qwerty'), 'missing Qwerty'
assert hasattr(mod, 'ShowLog'), 'missing ShowLog'
assert hasattr(mod, 'NoOneWillActuallyDoThis'), 'missing NoOneWillActuallyDoThis'
