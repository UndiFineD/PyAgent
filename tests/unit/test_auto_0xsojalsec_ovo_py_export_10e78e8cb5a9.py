
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_export_10e78e8cb5a9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'write_sheets'), 'missing write_sheets'
assert hasattr(mod, 'write_sheet'), 'missing write_sheet'
assert hasattr(mod, 'sanitize_excel_sheet_name'), 'missing sanitize_excel_sheet_name'
assert hasattr(mod, 'shorten_sheet_names'), 'missing shorten_sheet_names'
