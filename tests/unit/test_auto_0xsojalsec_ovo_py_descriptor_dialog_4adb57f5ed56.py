
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_descriptor_dialog_4adb57f5ed56.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'on_dismiss_dialog'), 'missing on_dismiss_dialog'
assert hasattr(mod, 'detail_descriptor_dialog'), 'missing detail_descriptor_dialog'
assert hasattr(mod, 'detail_button'), 'missing detail_button'
assert hasattr(mod, 'detail_table'), 'missing detail_table'
assert hasattr(mod, 'detail_design'), 'missing detail_design'
