
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_intro_3e85b770ce34.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'TrigAnimation'), 'missing TrigAnimation'
assert hasattr(mod, 'Notation'), 'missing Notation'
assert hasattr(mod, 'ButDots'), 'missing ButDots'
assert hasattr(mod, 'ThreesomeOfNotation'), 'missing ThreesomeOfNotation'
assert hasattr(mod, 'TwoThreeEightExample'), 'missing TwoThreeEightExample'
assert hasattr(mod, 'WhatTheHell'), 'missing WhatTheHell'
assert hasattr(mod, 'Countermathematical'), 'missing Countermathematical'
assert hasattr(mod, 'PascalsCollision'), 'missing PascalsCollision'
assert hasattr(mod, 'LogarithmProperties'), 'missing LogarithmProperties'
assert hasattr(mod, 'HaveToShare'), 'missing HaveToShare'
