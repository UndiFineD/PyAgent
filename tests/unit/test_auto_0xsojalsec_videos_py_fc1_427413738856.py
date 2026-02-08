
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_fc1_427413738856.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CrossingOneMillion'), 'missing CrossingOneMillion'
assert hasattr(mod, 'ShareWithFriends'), 'missing ShareWithFriends'
assert hasattr(mod, 'AllFeaturedCreators'), 'missing AllFeaturedCreators'
assert hasattr(mod, 'GeneralWrapper'), 'missing GeneralWrapper'
assert hasattr(mod, 'ThinkTwiceWrapper'), 'missing ThinkTwiceWrapper'
assert hasattr(mod, 'LeiosOSWrapper'), 'missing LeiosOSWrapper'
assert hasattr(mod, 'WelchLabsWrapper'), 'missing WelchLabsWrapper'
assert hasattr(mod, 'InfinityPlusOneWrapper'), 'missing InfinityPlusOneWrapper'
assert hasattr(mod, 'EndScreen'), 'missing EndScreen'
