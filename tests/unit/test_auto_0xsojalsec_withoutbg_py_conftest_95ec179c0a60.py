
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_withoutbg_py_conftest_95ec179c0a60.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'pytest_configure'), 'missing pytest_configure'
assert hasattr(mod, 'pytest_collection_modifyitems'), 'missing pytest_collection_modifyitems'
assert hasattr(mod, 'test_data_dir'), 'missing test_data_dir'
assert hasattr(mod, 'test_images_dir'), 'missing test_images_dir'
assert hasattr(mod, 'expected_outputs_dir'), 'missing expected_outputs_dir'
assert hasattr(mod, 'temp_dir'), 'missing temp_dir'
assert hasattr(mod, 'sample_test_image'), 'missing sample_test_image'
assert hasattr(mod, 'sample_test_images'), 'missing sample_test_images'
assert hasattr(mod, 'cleanup_temp_files'), 'missing cleanup_temp_files'
assert hasattr(mod, 'pytest_runtest_setup'), 'missing pytest_runtest_setup'
assert hasattr(mod, 'pytest_addoption'), 'missing pytest_addoption'
assert hasattr(mod, 'assert_image_properties'), 'missing assert_image_properties'
assert hasattr(mod, 'assert_processing_result'), 'missing assert_processing_result'
assert hasattr(mod, 'PerformanceTracker'), 'missing PerformanceTracker'
assert hasattr(mod, 'performance_tracker'), 'missing performance_tracker'
assert hasattr(mod, 'real_test_image_path'), 'missing real_test_image_path'
