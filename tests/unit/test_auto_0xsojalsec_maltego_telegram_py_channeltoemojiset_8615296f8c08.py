
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_maltego_telegram_py_channeltoemojiset_8615296f8c08.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'collect_available_reactions'), 'missing collect_available_reactions'
assert hasattr(mod, 'collect_emoji_ids'), 'missing collect_emoji_ids'
assert hasattr(mod, 'fetch_emoji_info'), 'missing fetch_emoji_info'
assert hasattr(mod, 'remove_duplicates'), 'missing remove_duplicates'
assert hasattr(mod, 'ChannelToEmojiSet'), 'missing ChannelToEmojiSet'
