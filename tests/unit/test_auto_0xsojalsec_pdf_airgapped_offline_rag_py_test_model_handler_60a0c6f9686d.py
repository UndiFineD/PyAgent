
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pdf_airgapped_offline_rag_py_test_model_handler_60a0c6f9686d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'mock_config'), 'missing mock_config'
assert hasattr(mod, 'model_handler'), 'missing model_handler'
assert hasattr(mod, 'test_load_model'), 'missing test_load_model'
assert hasattr(mod, 'test_generate_stream'), 'missing test_generate_stream'
assert hasattr(mod, 'test_get_quantization_from_filename'), 'missing test_get_quantization_from_filename'
assert hasattr(mod, 'test_get_quantization_params'), 'missing test_get_quantization_params'
assert hasattr(mod, 'test_check_available_models'), 'missing test_check_available_models'
assert hasattr(mod, 'test_get_dynamic_max_tokens'), 'missing test_get_dynamic_max_tokens'
assert hasattr(mod, 'test_log_performance_metrics'), 'missing test_log_performance_metrics'
