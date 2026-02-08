
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_testing_7386ec4b3902.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'is_test_dialog_shown'), 'missing is_test_dialog_shown'
assert hasattr(mod, 'show_test_dialog'), 'missing show_test_dialog'
assert hasattr(mod, 'hide_test_dialog'), 'missing hide_test_dialog'
