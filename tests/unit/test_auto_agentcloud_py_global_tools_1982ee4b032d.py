
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentcloud_py_global_tools_1982ee4b032d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'HumanInputParams'), 'missing HumanInputParams'
assert hasattr(mod, 'CustomHumanInput'), 'missing CustomHumanInput'
assert hasattr(mod, 'GlobalBaseTool'), 'missing GlobalBaseTool'
assert hasattr(mod, 'openapi_request'), 'missing openapi_request'
