
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agents_generic_py_openai_df6d5d56b496.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'to_chat_ctx'), 'missing to_chat_ctx'
assert hasattr(mod, '_to_chat_item'), 'missing _to_chat_item'
assert hasattr(mod, '_to_image_content'), 'missing _to_image_content'
