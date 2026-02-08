
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_test_sop_customization_a5387f50c276.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'TestSOPPromptCustomization'), 'missing TestSOPPromptCustomization'
assert hasattr(mod, 'TestTaskSOPPromptWithCustomization'), 'missing TestTaskSOPPromptWithCustomization'
assert hasattr(mod, 'TestProjectConfigIntegration'), 'missing TestProjectConfigIntegration'
