
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentcloud_py_build_task_helpers_a8255f0ad416.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_task_tools'), 'missing get_task_tools'
assert hasattr(mod, 'get_context_tasks'), 'missing get_context_tasks'
assert hasattr(mod, '_upload_task_output'), 'missing _upload_task_output'
assert hasattr(mod, '_assign_structured_output_fields_to_variables'), 'missing _assign_structured_output_fields_to_variables'
assert hasattr(mod, '_assign_output_to_variable_if_single_variable'), 'missing _assign_output_to_variable_if_single_variable'
assert hasattr(mod, '_update_variables_from_output'), 'missing _update_variables_from_output'
assert hasattr(mod, 'make_task_callback'), 'missing make_task_callback'
assert hasattr(mod, 'get_output_pydantic_model'), 'missing get_output_pydantic_model'
assert hasattr(mod, 'get_output_variables'), 'missing get_output_variables'
assert hasattr(mod, 'extract_matching_values'), 'missing extract_matching_values'
