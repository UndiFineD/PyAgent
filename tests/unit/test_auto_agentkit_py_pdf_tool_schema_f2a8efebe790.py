
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_pdf_tool_schema_f2a8efebe790.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PdfAppendix'), 'missing PdfAppendix'
assert hasattr(mod, 'MarkdownMetadata'), 'missing MarkdownMetadata'
