
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pi3mos_slam_py_vision_transformer_157886bb1bdd.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'named_apply'), 'missing named_apply'
assert hasattr(mod, 'BlockChunk'), 'missing BlockChunk'
assert hasattr(mod, 'DinoVisionTransformer'), 'missing DinoVisionTransformer'
assert hasattr(mod, 'init_weights_vit_timm'), 'missing init_weights_vit_timm'
assert hasattr(mod, 'vit_small'), 'missing vit_small'
assert hasattr(mod, 'vit_base'), 'missing vit_base'
assert hasattr(mod, 'vit_large'), 'missing vit_large'
assert hasattr(mod, 'vit_giant2'), 'missing vit_giant2'
