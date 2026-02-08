
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_voicecraft_py_sampling_a0b72adfd57d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'top_k_top_p_filtering'), 'missing top_k_top_p_filtering'
assert hasattr(mod, 'topk_sampling'), 'missing topk_sampling'
