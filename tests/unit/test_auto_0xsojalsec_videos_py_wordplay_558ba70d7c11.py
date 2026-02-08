
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_wordplay_558ba70d7c11.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Intro'), 'missing Intro'
assert hasattr(mod, 'IntroduceSteve'), 'missing IntroduceSteve'
assert hasattr(mod, 'ShowTweets'), 'missing ShowTweets'
assert hasattr(mod, 'LetsBeHonest'), 'missing LetsBeHonest'
assert hasattr(mod, 'WhatIsTheBrachistochrone'), 'missing WhatIsTheBrachistochrone'
assert hasattr(mod, 'DisectBrachistochroneWord'), 'missing DisectBrachistochroneWord'
assert hasattr(mod, 'OneSolutionTwoInsights'), 'missing OneSolutionTwoInsights'
assert hasattr(mod, 'CircleOfIdeas'), 'missing CircleOfIdeas'
assert hasattr(mod, 'FermatsPrincipleStatement'), 'missing FermatsPrincipleStatement'
assert hasattr(mod, 'VideoProgression'), 'missing VideoProgression'
assert hasattr(mod, 'BalanceCompetingFactors'), 'missing BalanceCompetingFactors'
assert hasattr(mod, 'Challenge'), 'missing Challenge'
assert hasattr(mod, 'Section1'), 'missing Section1'
assert hasattr(mod, 'Section2'), 'missing Section2'
assert hasattr(mod, 'NarratorInterjection'), 'missing NarratorInterjection'
assert hasattr(mod, 'ThisCouldBeTheEnd'), 'missing ThisCouldBeTheEnd'
assert hasattr(mod, 'MyOwnChallenge'), 'missing MyOwnChallenge'
assert hasattr(mod, 'WarmupChallenge'), 'missing WarmupChallenge'
assert hasattr(mod, 'FindAnotherSolution'), 'missing FindAnotherSolution'
assert hasattr(mod, 'ProofOfSnellsLaw'), 'missing ProofOfSnellsLaw'
assert hasattr(mod, 'CondensedVersion'), 'missing CondensedVersion'
