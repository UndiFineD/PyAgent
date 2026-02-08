
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_notion_toolkit_575d227554c3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_plain_text_from_rich_text'), 'missing get_plain_text_from_rich_text'
assert hasattr(mod, 'get_media_source_text'), 'missing get_media_source_text'
assert hasattr(mod, 'NotionToolkit'), 'missing NotionToolkit'
