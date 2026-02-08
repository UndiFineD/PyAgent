
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_device_parser_482695819641.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_determine_root_gpu_device'), 'missing _determine_root_gpu_device'
assert hasattr(mod, '_parse_gpu_ids'), 'missing _parse_gpu_ids'
assert hasattr(mod, '_normalize_parse_gpu_string_input'), 'missing _normalize_parse_gpu_string_input'
assert hasattr(mod, '_sanitize_gpu_ids'), 'missing _sanitize_gpu_ids'
assert hasattr(mod, '_normalize_parse_gpu_input_to_list'), 'missing _normalize_parse_gpu_input_to_list'
assert hasattr(mod, '_get_all_available_gpus'), 'missing _get_all_available_gpus'
assert hasattr(mod, '_check_unique'), 'missing _check_unique'
assert hasattr(mod, '_check_data_type'), 'missing _check_data_type'
assert hasattr(mod, '_select_auto_accelerator'), 'missing _select_auto_accelerator'
