
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xSojalSec_pdfalyzer_test_pdf_tree_node.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_pdf_node_address'), 'missing test_pdf_node_address'
assert hasattr(mod, 'test_address_of_this_node_in_other'), 'missing test_address_of_this_node_in_other'
assert hasattr(mod, 'test_referenced_by_keys'), 'missing test_referenced_by_keys'
