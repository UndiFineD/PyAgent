
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_response_d0cca6c8bafc.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SearchResultBlockItem'), 'missing SearchResultBlockItem'
assert hasattr(mod, 'SpaceSearchResult'), 'missing SpaceSearchResult'
assert hasattr(mod, 'Flag'), 'missing Flag'
assert hasattr(mod, 'InsertBlockResponse'), 'missing InsertBlockResponse'
assert hasattr(mod, 'LearningStatusResponse'), 'missing LearningStatusResponse'
