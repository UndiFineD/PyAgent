
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\stream_omni_py_siglip_encoder_842aa67b0927.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'SigLipImageProcessor'), 'missing SigLipImageProcessor'
assert hasattr(mod, 'SigLipVisionConfig'), 'missing SigLipVisionConfig'
assert hasattr(mod, 'SigLipVisionModelOutput'), 'missing SigLipVisionModelOutput'
assert hasattr(mod, 'SigLipVisionEmbeddings'), 'missing SigLipVisionEmbeddings'
assert hasattr(mod, 'SigLipAttention'), 'missing SigLipAttention'
assert hasattr(mod, 'SigLipMLP'), 'missing SigLipMLP'
assert hasattr(mod, 'SigLipEncoderLayer'), 'missing SigLipEncoderLayer'
assert hasattr(mod, 'SigLipPreTrainedModel'), 'missing SigLipPreTrainedModel'
assert hasattr(mod, 'SigLipEncoder'), 'missing SigLipEncoder'
assert hasattr(mod, 'SigLipVisionTransformer'), 'missing SigLipVisionTransformer'
assert hasattr(mod, 'SigLipMultiheadAttentionPoolingHead'), 'missing SigLipMultiheadAttentionPoolingHead'
assert hasattr(mod, 'SigLipVisionModel'), 'missing SigLipVisionModel'
assert hasattr(mod, 'SigLipVisionTower'), 'missing SigLipVisionTower'
