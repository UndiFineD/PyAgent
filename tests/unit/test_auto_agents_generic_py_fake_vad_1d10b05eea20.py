
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_fake_vad_1d10b05eea20.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'FakeVAD'), 'missing FakeVAD'
assert hasattr(mod, 'FakeVADStream'), 'missing FakeVADStream'
