
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_upright_coins_6dca0a843999.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'UprightCoin'), 'missing UprightCoin'
assert hasattr(mod, 'UprightHeads'), 'missing UprightHeads'
assert hasattr(mod, 'UprightTails'), 'missing UprightTails'
assert hasattr(mod, 'CoinSequence'), 'missing CoinSequence'
assert hasattr(mod, 'FlatCoin'), 'missing FlatCoin'
assert hasattr(mod, 'FlatHeads'), 'missing FlatHeads'
assert hasattr(mod, 'FlatTails'), 'missing FlatTails'
