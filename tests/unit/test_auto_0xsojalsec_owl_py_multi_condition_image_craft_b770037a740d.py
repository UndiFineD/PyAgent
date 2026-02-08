
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_multi_condition_image_craft_b770037a740d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'MultiConditionImageCraftPromptTemplateDict'), 'missing MultiConditionImageCraftPromptTemplateDict'
