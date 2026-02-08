
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_test_evals_d48f4725bf68.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'KellyAgent'), 'missing KellyAgent'
assert hasattr(mod, 'EchoAgent'), 'missing EchoAgent'
assert hasattr(mod, 'test_function_call'), 'missing test_function_call'
assert hasattr(mod, 'RandomResult'), 'missing RandomResult'
assert hasattr(mod, 'InlineAgent'), 'missing InlineAgent'
assert hasattr(mod, 'AshAgent'), 'missing AshAgent'
assert hasattr(mod, 'test_inline_agent'), 'missing test_inline_agent'
