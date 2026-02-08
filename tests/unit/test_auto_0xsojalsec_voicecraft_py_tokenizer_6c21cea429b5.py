
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_voicecraft_py_tokenizer_6c21cea429b5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'TextTokenizer'), 'missing TextTokenizer'
assert hasattr(mod, 'tokenize_text'), 'missing tokenize_text'
assert hasattr(mod, 'convert_audio'), 'missing convert_audio'
assert hasattr(mod, 'AudioTokenizer'), 'missing AudioTokenizer'
assert hasattr(mod, 'tokenize_audio'), 'missing tokenize_audio'
