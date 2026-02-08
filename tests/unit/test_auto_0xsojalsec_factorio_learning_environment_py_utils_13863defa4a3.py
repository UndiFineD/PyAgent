
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_factorio_learning_environment_py_utils_13863defa4a3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'merge_contiguous_messages'), 'missing merge_contiguous_messages'
assert hasattr(mod, 'remove_whitespace_blocks'), 'missing remove_whitespace_blocks'
assert hasattr(mod, 'has_image_content'), 'missing has_image_content'
assert hasattr(mod, 'format_messages_for_anthropic'), 'missing format_messages_for_anthropic'
assert hasattr(mod, 'format_messages_for_openai'), 'missing format_messages_for_openai'
