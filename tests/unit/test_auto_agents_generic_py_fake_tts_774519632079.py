
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_fake_tts_774519632079.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FakeTTSResponse'), 'missing FakeTTSResponse'
assert hasattr(mod, 'FakeTTS'), 'missing FakeTTS'
assert hasattr(mod, 'FakeChunkedStream'), 'missing FakeChunkedStream'
assert hasattr(mod, 'FakeSynthesizeStream'), 'missing FakeSynthesizeStream'
