
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_models_b2033273c443.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SlackAuthProfile'), 'missing SlackAuthProfile'
assert hasattr(mod, 'SlackEventProfile'), 'missing SlackEventProfile'
assert hasattr(mod, 'SlackEventBody'), 'missing SlackEventBody'
assert hasattr(mod, 'SlackAppMentionEventProfile'), 'missing SlackAppMentionEventProfile'
assert hasattr(mod, 'SlackAppMentionEventBody'), 'missing SlackAppMentionEventBody'
