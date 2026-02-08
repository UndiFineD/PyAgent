
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mobileagent_py_merge_strategy_03436cd0af23.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'calculate_iou'), 'missing calculate_iou'
assert hasattr(mod, 'compute_iou'), 'missing compute_iou'
assert hasattr(mod, 'merge_boxes'), 'missing merge_boxes'
assert hasattr(mod, 'merge_boxes_and_texts'), 'missing merge_boxes_and_texts'
assert hasattr(mod, 'is_contained'), 'missing is_contained'
assert hasattr(mod, 'is_overlapping'), 'missing is_overlapping'
assert hasattr(mod, 'get_area'), 'missing get_area'
assert hasattr(mod, 'merge_all_icon_boxes'), 'missing merge_all_icon_boxes'
assert hasattr(mod, 'merge_all_icon_boxes_new'), 'missing merge_all_icon_boxes_new'
assert hasattr(mod, 'merge_bbox_groups'), 'missing merge_bbox_groups'
assert hasattr(mod, 'bbox_iou'), 'missing bbox_iou'
assert hasattr(mod, 'merge_boxes_and_texts_new'), 'missing merge_boxes_and_texts_new'
