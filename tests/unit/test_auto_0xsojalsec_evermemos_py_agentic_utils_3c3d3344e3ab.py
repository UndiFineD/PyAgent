
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_evermemos_py_agentic_utils_3c3d3344e3ab.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'format_documents_for_llm'), 'missing format_documents_for_llm'
assert hasattr(mod, 'parse_json_response'), 'missing parse_json_response'
assert hasattr(mod, 'parse_refined_query'), 'missing parse_refined_query'
assert hasattr(mod, 'check_sufficiency'), 'missing check_sufficiency'
assert hasattr(mod, 'generate_refined_query'), 'missing generate_refined_query'
assert hasattr(mod, 'parse_multi_query_response'), 'missing parse_multi_query_response'
assert hasattr(mod, 'generate_multi_queries'), 'missing generate_multi_queries'
