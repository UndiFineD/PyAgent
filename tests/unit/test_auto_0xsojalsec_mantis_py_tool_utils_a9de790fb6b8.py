
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_mantis_py_tool_utils_a9de790fb6b8.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'get_active_hosts'), 'missing get_active_hosts'
assert hasattr(mod, 'get_org_assets'), 'missing get_org_assets'
assert hasattr(mod, 'get_assets_grouped_by_type'), 'missing get_assets_grouped_by_type'
assert hasattr(mod, 'get_assets_with_empty_fields'), 'missing get_assets_with_empty_fields'
assert hasattr(mod, 'get_assets_with_non_empty_fields'), 'missing get_assets_with_non_empty_fields'
assert hasattr(mod, 'get_assets_by_field_value'), 'missing get_assets_by_field_value'
assert hasattr(mod, 'get_pipeline'), 'missing get_pipeline'
assert hasattr(mod, 'get_findings_by_asset'), 'missing get_findings_by_asset'
