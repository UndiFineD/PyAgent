
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_fake_stt_062d87961c0c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'RecognizeSentinel'), 'missing RecognizeSentinel'
assert hasattr(mod, 'FakeUserSpeech'), 'missing FakeUserSpeech'
assert hasattr(mod, 'FakeSTT'), 'missing FakeSTT'
assert hasattr(mod, 'FakeRecognizeStream'), 'missing FakeRecognizeStream'
