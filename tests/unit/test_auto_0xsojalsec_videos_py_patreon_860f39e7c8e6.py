
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_patreon_860f39e7c8e6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SideGigToFullTime'), 'missing SideGigToFullTime'
assert hasattr(mod, 'TakesTime'), 'missing TakesTime'
assert hasattr(mod, 'GrowingToDoList'), 'missing GrowingToDoList'
assert hasattr(mod, 'TwoTypesOfVideos'), 'missing TwoTypesOfVideos'
assert hasattr(mod, 'ClassWatching'), 'missing ClassWatching'
assert hasattr(mod, 'RandolphWatching'), 'missing RandolphWatching'
assert hasattr(mod, 'RandolphWatchingWithLaptop'), 'missing RandolphWatchingWithLaptop'
assert hasattr(mod, 'GrowRonaksSierpinski'), 'missing GrowRonaksSierpinski'
assert hasattr(mod, 'PatreonLogo'), 'missing PatreonLogo'
assert hasattr(mod, 'PatreonLogin'), 'missing PatreonLogin'
assert hasattr(mod, 'PythagoreanTransformation'), 'missing PythagoreanTransformation'
assert hasattr(mod, 'KindWordsOnEoLA'), 'missing KindWordsOnEoLA'
assert hasattr(mod, 'MakeALotOfPiCreaturesHappy'), 'missing MakeALotOfPiCreaturesHappy'
assert hasattr(mod, 'IntegrationByParts'), 'missing IntegrationByParts'
assert hasattr(mod, 'EndScreen'), 'missing EndScreen'
