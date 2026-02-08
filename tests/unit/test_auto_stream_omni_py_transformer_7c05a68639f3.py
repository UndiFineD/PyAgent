
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_transformer_7c05a68639f3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SnakeBeta'), 'missing SnakeBeta'
assert hasattr(mod, 'FeedForward'), 'missing FeedForward'
assert hasattr(mod, 'BasicTransformerBlock'), 'missing BasicTransformerBlock'
