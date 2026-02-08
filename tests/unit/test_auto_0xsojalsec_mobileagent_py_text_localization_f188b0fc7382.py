
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mobileagent_py_text_localization_f188b0fc7382.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'order_point'), 'missing order_point'
assert hasattr(mod, 'longest_common_substring_length'), 'missing longest_common_substring_length'
assert hasattr(mod, 'ocr'), 'missing ocr'
