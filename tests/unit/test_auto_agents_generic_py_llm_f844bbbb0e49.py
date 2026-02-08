
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_llm_f844bbbb0e49.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_LLMOptions'), 'missing _LLMOptions'
assert hasattr(mod, 'LLM'), 'missing LLM'
assert hasattr(mod, 'LLMStream'), 'missing LLMStream'
