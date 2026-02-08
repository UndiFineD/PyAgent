
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pdfalyzer_py_test_node_colors_538ca002929a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'test_get_class_style'), 'missing test_get_class_style'
assert hasattr(mod, 'test_get_label_style'), 'missing test_get_label_style'
