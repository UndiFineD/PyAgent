
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\chunk_0_debug.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'enable_debug_mode'), 'missing enable_debug_mode'
assert hasattr(mod, 'disable_debug_mode'), 'missing disable_debug_mode'
