
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_history_components_02438869a061.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'history_dropdown_component'), 'missing history_dropdown_component'
assert hasattr(mod, 'format_label'), 'missing format_label'
