
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_mm_utils_1962f63b55f9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'resize_and_center_crop'), 'missing resize_and_center_crop'
assert hasattr(mod, 'auto_pad_images'), 'missing auto_pad_images'
assert hasattr(mod, 'extract_patches'), 'missing extract_patches'
assert hasattr(mod, 'process_highres_image_crop_split'), 'missing process_highres_image_crop_split'
assert hasattr(mod, 'process_highres_image'), 'missing process_highres_image'
assert hasattr(mod, 'select_best_resolution'), 'missing select_best_resolution'
assert hasattr(mod, 'resize_and_pad_image'), 'missing resize_and_pad_image'
assert hasattr(mod, 'divide_to_patches'), 'missing divide_to_patches'
assert hasattr(mod, 'get_anyres_image_grid_shape'), 'missing get_anyres_image_grid_shape'
assert hasattr(mod, 'process_anyres_image'), 'missing process_anyres_image'
assert hasattr(mod, 'load_image_from_base64'), 'missing load_image_from_base64'
assert hasattr(mod, 'expand2square'), 'missing expand2square'
assert hasattr(mod, 'process_images'), 'missing process_images'
assert hasattr(mod, 'tokenizer_image_token'), 'missing tokenizer_image_token'
assert hasattr(mod, 'get_model_name_from_path'), 'missing get_model_name_from_path'
assert hasattr(mod, 'KeywordsStoppingCriteria'), 'missing KeywordsStoppingCriteria'
