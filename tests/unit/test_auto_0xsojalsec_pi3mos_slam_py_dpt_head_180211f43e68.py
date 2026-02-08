
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_dpt_head_180211f43e68.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'DPTHead'), 'missing DPTHead'
assert hasattr(mod, '_make_fusion_block'), 'missing _make_fusion_block'
assert hasattr(mod, '_make_scratch'), 'missing _make_scratch'
assert hasattr(mod, 'ResidualConvUnit'), 'missing ResidualConvUnit'
assert hasattr(mod, 'FeatureFusionBlock'), 'missing FeatureFusionBlock'
assert hasattr(mod, 'custom_interpolate'), 'missing custom_interpolate'
