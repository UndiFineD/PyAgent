
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_maltego_telegram_py_stickersettoowner_ccf33dacd1fe.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'fetch_sticker_set_owner'), 'missing fetch_sticker_set_owner'
assert hasattr(mod, 'StickerSetToOwner'), 'missing StickerSetToOwner'
