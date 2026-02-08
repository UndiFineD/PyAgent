
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_pi_creature_scenes_464b0c94cf20.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'OnAnsweringTwice'), 'missing OnAnsweringTwice'
assert hasattr(mod, 'AskAboutEqualMassMomentumTransfer'), 'missing AskAboutEqualMassMomentumTransfer'
assert hasattr(mod, 'ComplainAboutRelevanceOfAnalogy'), 'missing ComplainAboutRelevanceOfAnalogy'
assert hasattr(mod, 'ReplaceOneTrickySceneWithAnother'), 'missing ReplaceOneTrickySceneWithAnother'
assert hasattr(mod, 'NowForTheGoodPart'), 'missing NowForTheGoodPart'
