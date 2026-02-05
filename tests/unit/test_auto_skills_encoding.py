
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\skills_encoding.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'base64_encode'), 'missing base64_encode'
assert hasattr(mod, 'base64_decode'), 'missing base64_decode'
assert hasattr(mod, 'hex_encode'), 'missing hex_encode'
assert hasattr(mod, 'hex_decode'), 'missing hex_decode'
assert hasattr(mod, 'url_encode'), 'missing url_encode'
assert hasattr(mod, 'url_decode'), 'missing url_decode'
