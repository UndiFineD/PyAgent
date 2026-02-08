
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_ovo_py_test_excel_export_851a25e42afe.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'create_test_data'), 'missing create_test_data'
assert hasattr(mod, 'test_export_proteinqc_excel'), 'missing test_export_proteinqc_excel'
