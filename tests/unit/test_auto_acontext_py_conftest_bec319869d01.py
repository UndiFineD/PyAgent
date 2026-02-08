
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_conftest_bec319869d01.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'mock_block_get_embedding'), 'missing mock_block_get_embedding'
assert hasattr(mod, 'mock_block_search_get_embedding'), 'missing mock_block_search_get_embedding'
