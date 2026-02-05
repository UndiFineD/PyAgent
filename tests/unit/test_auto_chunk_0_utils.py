
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\chunk_0_utils.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'extract_test_output_code'), 'missing extract_test_output_code'
assert hasattr(mod, 'extract_execution_code'), 'missing extract_execution_code'
