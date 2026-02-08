
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_llms_from_scratch_py_previous_chapters_68c7de9363b3.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'GPTDatasetV1'), 'missing GPTDatasetV1'
assert hasattr(mod, 'create_dataloader_v1'), 'missing create_dataloader_v1'
assert hasattr(mod, 'MultiHeadAttention'), 'missing MultiHeadAttention'
assert hasattr(mod, 'LayerNorm'), 'missing LayerNorm'
assert hasattr(mod, 'GELU'), 'missing GELU'
assert hasattr(mod, 'FeedForward'), 'missing FeedForward'
assert hasattr(mod, 'TransformerBlock'), 'missing TransformerBlock'
assert hasattr(mod, 'GPTModel'), 'missing GPTModel'
assert hasattr(mod, 'generate_text_simple'), 'missing generate_text_simple'
assert hasattr(mod, 'text_to_token_ids'), 'missing text_to_token_ids'
assert hasattr(mod, 'token_ids_to_text'), 'missing token_ids_to_text'
assert hasattr(mod, 'generate'), 'missing generate'
