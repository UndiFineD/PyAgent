
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_fractal_porn_17dedcb8eeff.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Intro'), 'missing Intro'
assert hasattr(mod, 'BringInPeano'), 'missing BringInPeano'
assert hasattr(mod, 'FillOtherShapes'), 'missing FillOtherShapes'
assert hasattr(mod, 'SmallerFlowSnake'), 'missing SmallerFlowSnake'
assert hasattr(mod, 'MostDelightfulName'), 'missing MostDelightfulName'
assert hasattr(mod, 'SurpriseFractal'), 'missing SurpriseFractal'
assert hasattr(mod, 'IntroduceKoch'), 'missing IntroduceKoch'
assert hasattr(mod, 'StraightKoch'), 'missing StraightKoch'
assert hasattr(mod, 'SharperKoch'), 'missing SharperKoch'
assert hasattr(mod, 'DullerKoch'), 'missing DullerKoch'
assert hasattr(mod, 'SpaceFillingKoch'), 'missing SpaceFillingKoch'
assert hasattr(mod, 'FromKochToSpaceFilling'), 'missing FromKochToSpaceFilling'
