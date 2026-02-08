
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_model_9929683c694c.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'ModelArgs'), 'missing ModelArgs'
assert hasattr(mod, 'precompute_freqs_cis'), 'missing precompute_freqs_cis'
assert hasattr(mod, 'reshape_for_broadcast'), 'missing reshape_for_broadcast'
assert hasattr(mod, 'apply_rotary_emb'), 'missing apply_rotary_emb'
assert hasattr(mod, 'repeat_kv'), 'missing repeat_kv'
assert hasattr(mod, 'RMSNorm'), 'missing RMSNorm'
assert hasattr(mod, 'Attention'), 'missing Attention'
assert hasattr(mod, 'FeedForward'), 'missing FeedForward'
assert hasattr(mod, 'TransformerBlock'), 'missing TransformerBlock'
assert hasattr(mod, 'Transformer'), 'missing Transformer'
