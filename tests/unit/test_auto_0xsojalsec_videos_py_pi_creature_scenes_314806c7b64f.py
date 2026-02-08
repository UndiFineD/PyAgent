
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_pi_creature_scenes_314806c7b64f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'WhyWouldYouCare'), 'missing WhyWouldYouCare'
assert hasattr(mod, 'SolveForWavesNothingElse'), 'missing SolveForWavesNothingElse'
assert hasattr(mod, 'HangOnThere'), 'missing HangOnThere'
assert hasattr(mod, 'YouSaidThisWasEasier'), 'missing YouSaidThisWasEasier'
assert hasattr(mod, 'LooseWithLanguage'), 'missing LooseWithLanguage'
assert hasattr(mod, 'FormulaOutOfContext'), 'missing FormulaOutOfContext'
