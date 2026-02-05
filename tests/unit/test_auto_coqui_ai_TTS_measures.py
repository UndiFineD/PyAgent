
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\coqui_ai_TTS_measures.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'alignment_diagonal_score'), 'missing alignment_diagonal_score'
