
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_general_2ee7ac521833.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'LLMRenderBlock'), 'missing LLMRenderBlock'
assert hasattr(mod, 'LocatedContentBlock'), 'missing LocatedContentBlock'
assert hasattr(mod, 'GeneralBlockData'), 'missing GeneralBlockData'
