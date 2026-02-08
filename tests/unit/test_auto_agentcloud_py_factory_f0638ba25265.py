
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\agentcloud_py_factory_f0638ba25265.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'model_factory'), 'missing model_factory'
assert hasattr(mod, '_build_ollama_model'), 'missing _build_ollama_model'
assert hasattr(mod, '_build_openai_model'), 'missing _build_openai_model'
assert hasattr(mod, '_build_azure_model'), 'missing _build_azure_model'
assert hasattr(mod, '_build_fastembed_model'), 'missing _build_fastembed_model'
assert hasattr(mod, '_fastembed_standard_doc_name_swap'), 'missing _fastembed_standard_doc_name_swap'
assert hasattr(mod, '_build_google_vertex_ai_model'), 'missing _build_google_vertex_ai_model'
assert hasattr(mod, '_build_google_ai_model'), 'missing _build_google_ai_model'
assert hasattr(mod, '_build_cohere_model'), 'missing _build_cohere_model'
assert hasattr(mod, '_build_anthropic_model'), 'missing _build_anthropic_model'
assert hasattr(mod, '_build_groq_model'), 'missing _build_groq_model'
