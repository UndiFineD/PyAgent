
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_model_summary_deepspeed_7876e08c7fdc.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'deepspeed_param_size'), 'missing deepspeed_param_size'
assert hasattr(mod, 'DeepSpeedLayerSummary'), 'missing DeepSpeedLayerSummary'
assert hasattr(mod, 'DeepSpeedSummary'), 'missing DeepSpeedSummary'
