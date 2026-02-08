
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_maltego_telegram_py_channeltoforwardedusers_6ffdafb28a00.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'find_forwarded_messages_from_users'), 'missing find_forwarded_messages_from_users'
assert hasattr(mod, 'get_unique_forward_users'), 'missing get_unique_forward_users'
assert hasattr(mod, 'ChannelToForwardedUsers'), 'missing ChannelToForwardedUsers'
