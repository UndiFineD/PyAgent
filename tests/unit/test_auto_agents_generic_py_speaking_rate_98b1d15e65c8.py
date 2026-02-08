
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_speaking_rate_98b1d15e65c8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_SpeakingRateDetectionOptions'), 'missing _SpeakingRateDetectionOptions'
assert hasattr(mod, 'SpeakingRateEvent'), 'missing SpeakingRateEvent'
assert hasattr(mod, 'SpeakingRateDetector'), 'missing SpeakingRateDetector'
assert hasattr(mod, 'SpeakingRateStream'), 'missing SpeakingRateStream'
