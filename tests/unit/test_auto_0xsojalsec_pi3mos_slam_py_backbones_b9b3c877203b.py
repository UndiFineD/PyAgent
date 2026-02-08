
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_backbones_b9b3c877203b.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'Weights'), 'missing Weights'
assert hasattr(mod, '_make_dinov2_model'), 'missing _make_dinov2_model'
assert hasattr(mod, 'dinov2_vits14'), 'missing dinov2_vits14'
assert hasattr(mod, 'dinov2_vitb14'), 'missing dinov2_vitb14'
assert hasattr(mod, 'dinov2_vitl14'), 'missing dinov2_vitl14'
assert hasattr(mod, 'dinov2_vitg14'), 'missing dinov2_vitg14'
assert hasattr(mod, 'dinov2_vits14_reg'), 'missing dinov2_vits14_reg'
assert hasattr(mod, 'dinov2_vitb14_reg'), 'missing dinov2_vitb14_reg'
assert hasattr(mod, 'dinov2_vitl14_reg'), 'missing dinov2_vitl14_reg'
assert hasattr(mod, 'dinov2_vitg14_reg'), 'missing dinov2_vitg14_reg'
