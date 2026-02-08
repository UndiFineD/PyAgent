
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_misc_5fffaf52ae27.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PhysicalIntuition'), 'missing PhysicalIntuition'
assert hasattr(mod, 'TimeLine'), 'missing TimeLine'
assert hasattr(mod, 'StayedUpAllNight'), 'missing StayedUpAllNight'
assert hasattr(mod, 'ThetaTGraph'), 'missing ThetaTGraph'
assert hasattr(mod, 'SolutionsToTheBrachistochrone'), 'missing SolutionsToTheBrachistochrone'
assert hasattr(mod, 'VideoLayout'), 'missing VideoLayout'
assert hasattr(mod, 'ShortestPathProblem'), 'missing ShortestPathProblem'
assert hasattr(mod, 'MathBetterThanTalking'), 'missing MathBetterThanTalking'
assert hasattr(mod, 'DetailsOfProofBox'), 'missing DetailsOfProofBox'
assert hasattr(mod, 'TalkedAboutSnellsLaw'), 'missing TalkedAboutSnellsLaw'
assert hasattr(mod, 'YetAnotherMarkLevi'), 'missing YetAnotherMarkLevi'
