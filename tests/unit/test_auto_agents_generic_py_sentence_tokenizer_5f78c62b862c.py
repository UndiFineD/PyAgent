
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_sentence_tokenizer_5f78c62b862c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_TokenizerOptions'), 'missing _TokenizerOptions'
assert hasattr(mod, 'SentenceTokenizer'), 'missing SentenceTokenizer'
