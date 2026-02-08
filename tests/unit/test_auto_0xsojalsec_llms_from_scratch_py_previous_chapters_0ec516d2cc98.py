
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_llms_from_scratch_py_previous_chapters_0ec516d2cc98.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'GPTDatasetV1'), 'missing GPTDatasetV1'
assert hasattr(mod, 'create_dataloader_v1'), 'missing create_dataloader_v1'
assert hasattr(mod, 'MultiHeadAttention'), 'missing MultiHeadAttention'
