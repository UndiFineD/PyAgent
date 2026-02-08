
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_voicecraft_py_trainer_utils_f0f34941a084.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'StatefulDistributedSampler'), 'missing StatefulDistributedSampler'
assert hasattr(mod, 'StatefulSampler'), 'missing StatefulSampler'
assert hasattr(mod, 'AverageMeter'), 'missing AverageMeter'
assert hasattr(mod, 'print_model_info'), 'missing print_model_info'
assert hasattr(mod, 'DistributedDynamicBatchSampler'), 'missing DistributedDynamicBatchSampler'
