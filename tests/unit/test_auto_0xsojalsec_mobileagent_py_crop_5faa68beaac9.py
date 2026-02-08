
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mobileagent_py_crop_5faa68beaac9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'crop_image'), 'missing crop_image'
assert hasattr(mod, 'calculate_size'), 'missing calculate_size'
assert hasattr(mod, 'calculate_iou'), 'missing calculate_iou'
assert hasattr(mod, 'crop'), 'missing crop'
assert hasattr(mod, 'in_box'), 'missing in_box'
assert hasattr(mod, 'crop_for_clip'), 'missing crop_for_clip'
assert hasattr(mod, 'clip_for_icon'), 'missing clip_for_icon'
