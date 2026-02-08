
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\absadiki_whatsapp_msgstore_viewer_py_main_screen_1259bc8da7a1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Tab'), 'missing Tab'
assert hasattr(mod, 'MLabel'), 'missing MLabel'
assert hasattr(mod, 'ChatListItem'), 'missing ChatListItem'
assert hasattr(mod, 'CallListItem'), 'missing CallListItem'
assert hasattr(mod, 'MainScreenView'), 'missing MainScreenView'
