
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\AD_Miner_logger.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'bcolors'), 'missing bcolors'
assert hasattr(mod, 'print_magenta'), 'missing print_magenta'
assert hasattr(mod, 'print_debug'), 'missing print_debug'
assert hasattr(mod, 'print_error'), 'missing print_error'
assert hasattr(mod, 'print_warning'), 'missing print_warning'
assert hasattr(mod, 'print_success'), 'missing print_success'
