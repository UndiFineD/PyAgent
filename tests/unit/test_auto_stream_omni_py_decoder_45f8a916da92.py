
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_decoder_45f8a916da92.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SinusoidalPosEmb'), 'missing SinusoidalPosEmb'
assert hasattr(mod, 'Block1D'), 'missing Block1D'
assert hasattr(mod, 'ResnetBlock1D'), 'missing ResnetBlock1D'
assert hasattr(mod, 'Downsample1D'), 'missing Downsample1D'
assert hasattr(mod, 'TimestepEmbedding'), 'missing TimestepEmbedding'
assert hasattr(mod, 'Upsample1D'), 'missing Upsample1D'
assert hasattr(mod, 'ConformerWrapper'), 'missing ConformerWrapper'
assert hasattr(mod, 'Decoder'), 'missing Decoder'
