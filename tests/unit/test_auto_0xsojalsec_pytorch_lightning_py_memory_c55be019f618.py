
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_memory_c55be019f618.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'recursive_detach'), 'missing recursive_detach'
assert hasattr(mod, 'is_oom_error'), 'missing is_oom_error'
assert hasattr(mod, 'is_cuda_out_of_memory'), 'missing is_cuda_out_of_memory'
assert hasattr(mod, 'is_cudnn_snafu'), 'missing is_cudnn_snafu'
assert hasattr(mod, 'is_out_of_cpu_memory'), 'missing is_out_of_cpu_memory'
assert hasattr(mod, 'garbage_collection_cuda'), 'missing garbage_collection_cuda'
