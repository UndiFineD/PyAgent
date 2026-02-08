
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_morph_brick_row_into_histogram_51c4b1da4a95.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'GenericMorphBrickRowIntoHistogram'), 'missing GenericMorphBrickRowIntoHistogram'
assert hasattr(mod, 'MorphBrickRowIntoHistogram3'), 'missing MorphBrickRowIntoHistogram3'
assert hasattr(mod, 'MorphBrickRowIntoHistogram20'), 'missing MorphBrickRowIntoHistogram20'
assert hasattr(mod, 'MorphBrickRowIntoHistogram100'), 'missing MorphBrickRowIntoHistogram100'
assert hasattr(mod, 'MorphBrickRowIntoHistogram500'), 'missing MorphBrickRowIntoHistogram500'
