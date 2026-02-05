
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\chunk_0_xhs_diy_encode.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'triplet_to_base64'), 'missing triplet_to_base64'
assert hasattr(mod, 'encode_chunk'), 'missing encode_chunk'
assert hasattr(mod, 'b64_encode'), 'missing b64_encode'
assert hasattr(mod, 'encode_utf8'), 'missing encode_utf8'
