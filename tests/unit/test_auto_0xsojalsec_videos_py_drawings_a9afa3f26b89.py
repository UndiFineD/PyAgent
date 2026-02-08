
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_drawings_a9afa3f26b89.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Car'), 'missing Car'
assert hasattr(mod, 'MoveCar'), 'missing MoveCar'
assert hasattr(mod, 'PartyHat'), 'missing PartyHat'
assert hasattr(mod, 'SunGlasses'), 'missing SunGlasses'
assert hasattr(mod, 'Headphones'), 'missing Headphones'
assert hasattr(mod, 'Guitar'), 'missing Guitar'
assert hasattr(mod, 'DeckOfCards'), 'missing DeckOfCards'
assert hasattr(mod, 'PlayingCard'), 'missing PlayingCard'
assert hasattr(mod, 'SuitSymbol'), 'missing SuitSymbol'
assert hasattr(mod, 'AoPSLogo'), 'missing AoPSLogo'
assert hasattr(mod, 'BitcoinLogo'), 'missing BitcoinLogo'
