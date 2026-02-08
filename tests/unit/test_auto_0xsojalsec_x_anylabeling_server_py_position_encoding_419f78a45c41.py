
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_x_anylabeling_server_py_position_encoding_419f78a45c41.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'PositionEmbeddingSine'), 'missing PositionEmbeddingSine'
assert hasattr(mod, 'PositionEmbeddingRandom'), 'missing PositionEmbeddingRandom'
assert hasattr(mod, 'init_t_xy'), 'missing init_t_xy'
assert hasattr(mod, 'compute_axial_cis'), 'missing compute_axial_cis'
assert hasattr(mod, 'reshape_for_broadcast'), 'missing reshape_for_broadcast'
assert hasattr(mod, 'apply_rotary_enc'), 'missing apply_rotary_enc'
