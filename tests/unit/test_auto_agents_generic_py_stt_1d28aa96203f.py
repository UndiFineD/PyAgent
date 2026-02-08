
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_stt_1d28aa96203f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'STTOptions'), 'missing STTOptions'
assert hasattr(mod, 'STT'), 'missing STT'
assert hasattr(mod, 'SpeechStream'), 'missing SpeechStream'
