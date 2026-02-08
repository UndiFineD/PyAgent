
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_maltego_telegram_py_channeltoauthors_9dbf9583d687.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'fetch_authors'), 'missing fetch_authors'
assert hasattr(mod, 'ChannelToAuthors'), 'missing ChannelToAuthors'
