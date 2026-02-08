
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_short_links_6ee55ce00bf2.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_vertical_screen'), 'missing get_vertical_screen'
assert hasattr(mod, 'CommentFlurry'), 'missing CommentFlurry'
assert hasattr(mod, 'CommentFlurryLinks'), 'missing CommentFlurryLinks'
assert hasattr(mod, 'CommentFlurryBlocks'), 'missing CommentFlurryBlocks'
assert hasattr(mod, 'CommentFlurryPrisms'), 'missing CommentFlurryPrisms'
assert hasattr(mod, 'CommentFlurryFourier'), 'missing CommentFlurryFourier'
assert hasattr(mod, 'CommentFlurryOtherQuestions'), 'missing CommentFlurryOtherQuestions'
assert hasattr(mod, 'PiLookingAtPhone'), 'missing PiLookingAtPhone'
assert hasattr(mod, 'ThisIsALink'), 'missing ThisIsALink'
assert hasattr(mod, 'LinkHighlightOverlay'), 'missing LinkHighlightOverlay'
