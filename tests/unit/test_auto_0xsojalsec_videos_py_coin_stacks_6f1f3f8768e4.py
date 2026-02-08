
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_coin_stacks_6f1f3f8768e4.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'CoinStack'), 'missing CoinStack'
assert hasattr(mod, 'HeadsStack'), 'missing HeadsStack'
assert hasattr(mod, 'TailsStack'), 'missing TailsStack'
assert hasattr(mod, 'DecimalTally'), 'missing DecimalTally'
assert hasattr(mod, 'TallyStack'), 'missing TallyStack'
