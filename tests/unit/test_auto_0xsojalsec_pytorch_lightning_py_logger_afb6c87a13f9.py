
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pytorch_lightning_py_logger_afb6c87a13f9.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, '_convert_params'), 'missing _convert_params'
assert hasattr(mod, '_sanitize_callable_params'), 'missing _sanitize_callable_params'
assert hasattr(mod, '_flatten_dict'), 'missing _flatten_dict'
assert hasattr(mod, '_sanitize_params'), 'missing _sanitize_params'
assert hasattr(mod, '_convert_json_serializable'), 'missing _convert_json_serializable'
assert hasattr(mod, '_is_json_serializable'), 'missing _is_json_serializable'
assert hasattr(mod, '_add_prefix'), 'missing _add_prefix'
