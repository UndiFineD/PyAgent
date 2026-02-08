
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_lumina_dimoo_py_prompt_utils_686c20ce886a.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'create_prompt_templates'), 'missing create_prompt_templates'
assert hasattr(mod, 'generate_text_to_image_prompt'), 'missing generate_text_to_image_prompt'
assert hasattr(mod, 'generate_image_to_image_prompt'), 'missing generate_image_to_image_prompt'
assert hasattr(mod, 'generate_multimodal_understanding_prompt'), 'missing generate_multimodal_understanding_prompt'
assert hasattr(mod, 'get_edit_type_specific_prompt'), 'missing get_edit_type_specific_prompt'
assert hasattr(mod, 'get_system_prompt_for_edit_type'), 'missing get_system_prompt_for_edit_type'
