
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_wafer_py_language_utils_f080bbf20ecd.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'gen_text'), 'missing gen_text'
assert hasattr(mod, 'gen_boolean'), 'missing gen_boolean'
assert hasattr(mod, 'gen_number'), 'missing gen_number'
assert hasattr(mod, 'gen_color'), 'missing gen_color'
assert hasattr(mod, 'gen_javascript'), 'missing gen_javascript'
assert hasattr(mod, 'gen_style'), 'missing gen_style'
assert hasattr(mod, 'gen_url'), 'missing gen_url'
assert hasattr(mod, 'gen_email'), 'missing gen_email'
assert hasattr(mod, 'gen_date'), 'missing gen_date'
assert hasattr(mod, 'gen_target'), 'missing gen_target'
assert hasattr(mod, 'gen_name'), 'missing gen_name'
assert hasattr(mod, 'gen_flag'), 'missing gen_flag'
assert hasattr(mod, 'gen_drop'), 'missing gen_drop'
assert hasattr(mod, 'gen_dir'), 'missing gen_dir'
assert hasattr(mod, 'gen_wtarget'), 'missing gen_wtarget'
assert hasattr(mod, 'gen_access_key'), 'missing gen_access_key'
assert hasattr(mod, 'gen_duration'), 'missing gen_duration'
