
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\whatsapp_msgstore_viewer_py_chat_screen_b3642d5d513b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'RV'), 'missing RV'
assert hasattr(mod, 'Attachment'), 'missing Attachment'
assert hasattr(mod, 'Quote'), 'missing Quote'
assert hasattr(mod, 'ChatMessage'), 'missing ChatMessage'
assert hasattr(mod, 'ChatScreenView'), 'missing ChatScreenView'
