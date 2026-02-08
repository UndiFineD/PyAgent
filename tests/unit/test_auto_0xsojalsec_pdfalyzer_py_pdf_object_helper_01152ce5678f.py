
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pdfalyzer_py_pdf_object_helper_01152ce5678f.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'pdf_object_id'), 'missing pdf_object_id'
assert hasattr(mod, 'does_list_have_any_references'), 'missing does_list_have_any_references'
assert hasattr(mod, '_sort_pdf_object_refs'), 'missing _sort_pdf_object_refs'
assert hasattr(mod, 'pypdf_class_name'), 'missing pypdf_class_name'
