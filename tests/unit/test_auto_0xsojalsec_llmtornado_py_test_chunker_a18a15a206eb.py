
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_llmtornado_py_test_chunker_a18a15a206eb.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'chunker'), 'missing chunker'
assert hasattr(mod, 'test_chunk_simple_text'), 'missing test_chunk_simple_text'
assert hasattr(mod, 'test_chunk_empty_text'), 'missing test_chunk_empty_text'
assert hasattr(mod, 'test_chunk_with_newlines'), 'missing test_chunk_with_newlines'
assert hasattr(mod, 'test_chunk_overlap'), 'missing test_chunk_overlap'
