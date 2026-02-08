
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_embedding_d84ef1f1bacc.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PositionalEncoding'), 'missing PositionalEncoding'
assert hasattr(mod, 'RelPositionalEncoding'), 'missing RelPositionalEncoding'
assert hasattr(mod, 'WhisperPositionalEncoding'), 'missing WhisperPositionalEncoding'
assert hasattr(mod, 'LearnablePositionalEncoding'), 'missing LearnablePositionalEncoding'
assert hasattr(mod, 'NoPositionalEncoding'), 'missing NoPositionalEncoding'
assert hasattr(mod, 'EspnetRelPositionalEncoding'), 'missing EspnetRelPositionalEncoding'
