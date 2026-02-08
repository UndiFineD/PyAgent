
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_custom_elements_4d6e3e75aa73.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'heading_with_value'), 'missing heading_with_value'
assert hasattr(mod, 'subheading_with_value'), 'missing subheading_with_value'
assert hasattr(mod, 'iter_progress'), 'missing iter_progress'
assert hasattr(mod, 'get_approx_screen_width'), 'missing get_approx_screen_width'
assert hasattr(mod, 'approx_max_width'), 'missing approx_max_width'
assert hasattr(mod, 'wrapped_columns'), 'missing wrapped_columns'
assert hasattr(mod, 'confirm_download_button'), 'missing confirm_download_button'
