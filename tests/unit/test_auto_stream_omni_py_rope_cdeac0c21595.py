
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_rope_cdeac0c21595.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'broadcat'), 'missing broadcat'
assert hasattr(mod, 'rotate_half'), 'missing rotate_half'
assert hasattr(mod, 'VisionRotaryEmbedding'), 'missing VisionRotaryEmbedding'
assert hasattr(mod, 'VisionRotaryEmbeddingFast'), 'missing VisionRotaryEmbeddingFast'
