
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentkit_py_test_pdf_tool_8095d110e458.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'mock_llm_call'), 'missing mock_llm_call'
assert hasattr(mod, 'pdf_pipeline'), 'missing pdf_pipeline'
assert hasattr(mod, 'fake_get_pdf_pipeline'), 'missing fake_get_pdf_pipeline'
assert hasattr(mod, 'pdf_tool'), 'missing pdf_tool'
assert hasattr(mod, 'test_doc_retrieval'), 'missing test_doc_retrieval'
assert hasattr(mod, 'test_qa_with_docs'), 'missing test_qa_with_docs'
assert hasattr(mod, 'test_qa_without_docs'), 'missing test_qa_without_docs'
assert hasattr(mod, 'test_pdf_tool_run'), 'missing test_pdf_tool_run'
