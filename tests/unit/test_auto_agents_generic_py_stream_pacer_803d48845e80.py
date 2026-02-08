
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_stream_pacer_803d48845e80.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'StreamPacerOptions'), 'missing StreamPacerOptions'
assert hasattr(mod, 'SentenceStreamPacer'), 'missing SentenceStreamPacer'
assert hasattr(mod, 'StreamPacerWrapper'), 'missing StreamPacerWrapper'
