
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_llms_from_scratch_py_ch03_0555a19ec4c3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CausalAttention'), 'missing CausalAttention'
assert hasattr(mod, 'MultiHeadAttentionWrapper'), 'missing MultiHeadAttentionWrapper'
assert hasattr(mod, 'MultiHeadAttention'), 'missing MultiHeadAttention'
