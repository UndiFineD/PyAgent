
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_mask_aae5f1ce95f2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'subsequent_mask'), 'missing subsequent_mask'
assert hasattr(mod, 'subsequent_chunk_mask'), 'missing subsequent_chunk_mask'
assert hasattr(mod, 'add_optional_chunk_mask'), 'missing add_optional_chunk_mask'
assert hasattr(mod, 'make_pad_mask'), 'missing make_pad_mask'
