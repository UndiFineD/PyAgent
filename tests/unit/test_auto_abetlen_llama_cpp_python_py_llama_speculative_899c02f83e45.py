
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\abetlen_llama_cpp_python_py_llama_speculative_899c02f83e45.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LlamaDraftModel'), 'missing LlamaDraftModel'
assert hasattr(mod, 'LlamaPromptLookupDecoding'), 'missing LlamaPromptLookupDecoding'
