
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\acontext_py_space_construct_28417df6fb9d.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'build_space_ctx'), 'missing build_space_ctx'
assert hasattr(mod, 'pack_candidate_data_list'), 'missing pack_candidate_data_list'
assert hasattr(mod, 'space_construct_agent_curd'), 'missing space_construct_agent_curd'
