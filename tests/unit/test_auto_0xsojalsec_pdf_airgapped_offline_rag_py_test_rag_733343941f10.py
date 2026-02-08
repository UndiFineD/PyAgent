
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_pdf_airgapped_offline_rag_py_test_rag_733343941f10.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'mock_config'), 'missing mock_config'
assert hasattr(mod, 'test_get_embedding_function'), 'missing test_get_embedding_function'
assert hasattr(mod, 'test_retrieve_context'), 'missing test_retrieve_context'
