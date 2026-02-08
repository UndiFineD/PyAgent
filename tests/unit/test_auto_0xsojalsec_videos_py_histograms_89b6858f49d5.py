
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_videos_py_histograms_89b6858f49d5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'text_range'), 'missing text_range'
assert hasattr(mod, 'Histogram'), 'missing Histogram'
assert hasattr(mod, 'BuildUpHistogram'), 'missing BuildUpHistogram'
assert hasattr(mod, 'FlashThroughHistogram'), 'missing FlashThroughHistogram'
assert hasattr(mod, 'OutlineableBars'), 'missing OutlineableBars'
