
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_prime_race_330e2c5dafc7.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PrimeRace'), 'missing PrimeRace'
assert hasattr(mod, 'RaceGraph'), 'missing RaceGraph'
assert hasattr(mod, 'LongRaceGraph'), 'missing LongRaceGraph'
