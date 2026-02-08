
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_utils_c5efd36f37b6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'wer'), 'missing wer'
assert hasattr(mod, 'EventCollector'), 'missing EventCollector'
assert hasattr(mod, 'read_audio_file'), 'missing read_audio_file'
assert hasattr(mod, 'fake_llm_stream'), 'missing fake_llm_stream'
