
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\chunk_0_synthesis.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'inv_spectrogram'), 'missing inv_spectrogram'
assert hasattr(mod, 'apply_griffin_lim'), 'missing apply_griffin_lim'
