
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_base_io_8da6a55254c4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'File'), 'missing File'
assert hasattr(mod, 'strip_consecutive_newlines'), 'missing strip_consecutive_newlines'
assert hasattr(mod, 'DocxFile'), 'missing DocxFile'
assert hasattr(mod, 'PdfFile'), 'missing PdfFile'
assert hasattr(mod, 'TxtFile'), 'missing TxtFile'
assert hasattr(mod, 'JsonFile'), 'missing JsonFile'
assert hasattr(mod, 'HtmlFile'), 'missing HtmlFile'
