
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_models_0388cdda5b8e.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'TaskResponse'), 'missing TaskResponse'
assert hasattr(mod, 'Response'), 'missing Response'
assert hasattr(mod, 'CompletionReason'), 'missing CompletionReason'
assert hasattr(mod, 'CompletionResult'), 'missing CompletionResult'
