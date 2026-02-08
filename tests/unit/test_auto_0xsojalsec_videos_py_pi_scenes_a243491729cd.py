
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_pi_scenes_a243491729cd.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ReactionsToInitialHeatEquation'), 'missing ReactionsToInitialHeatEquation'
assert hasattr(mod, 'ContrastPDEToODE'), 'missing ContrastPDEToODE'
assert hasattr(mod, 'AskAboutWhereEquationComesFrom'), 'missing AskAboutWhereEquationComesFrom'
assert hasattr(mod, 'AskWhyRewriteIt'), 'missing AskWhyRewriteIt'
assert hasattr(mod, 'ReferenceKhanVideo'), 'missing ReferenceKhanVideo'
