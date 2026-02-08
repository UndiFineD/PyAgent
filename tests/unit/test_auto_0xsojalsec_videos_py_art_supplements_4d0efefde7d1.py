
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_art_supplements_4d0efefde7d1.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'AmbientPermutations'), 'missing AmbientPermutations'
assert hasattr(mod, 'WriteName'), 'missing WriteName'
assert hasattr(mod, 'TimelineTransition'), 'missing TimelineTransition'
assert hasattr(mod, 'OutpaintTransition'), 'missing OutpaintTransition'
assert hasattr(mod, 'NightSkyOutpaintingTransition'), 'missing NightSkyOutpaintingTransition'
assert hasattr(mod, 'LastWordsQuote'), 'missing LastWordsQuote'
assert hasattr(mod, 'InfamousCoquette'), 'missing InfamousCoquette'
assert hasattr(mod, 'NightBeforeQuote'), 'missing NightBeforeQuote'
assert hasattr(mod, 'CauchyFourierPoisson'), 'missing CauchyFourierPoisson'
