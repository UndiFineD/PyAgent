
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_distributed_37f12f4a8ac5.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_find_tensors'), 'missing _find_tensors'
assert hasattr(mod, 'prepare_for_backward'), 'missing prepare_for_backward'
assert hasattr(mod, '_register_ddp_comm_hook'), 'missing _register_ddp_comm_hook'
assert hasattr(mod, '_sync_module_states'), 'missing _sync_module_states'
assert hasattr(mod, 'UnrepeatedDistributedSampler'), 'missing UnrepeatedDistributedSampler'
assert hasattr(mod, 'UnrepeatedDistributedSamplerWrapper'), 'missing UnrepeatedDistributedSamplerWrapper'
assert hasattr(mod, '_IndexBatchSamplerWrapper'), 'missing _IndexBatchSamplerWrapper'
