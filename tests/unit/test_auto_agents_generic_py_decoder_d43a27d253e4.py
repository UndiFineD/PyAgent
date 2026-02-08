
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_decoder_d43a27d253e4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_mime_to_av_format'), 'missing _mime_to_av_format'
assert hasattr(mod, 'StreamBuffer'), 'missing StreamBuffer'
assert hasattr(mod, 'AudioStreamDecoder'), 'missing AudioStreamDecoder'
