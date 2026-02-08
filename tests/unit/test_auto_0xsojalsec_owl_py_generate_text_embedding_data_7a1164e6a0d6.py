
import importlib.util
from pathlib import Path

p = Path(r"C:\DEV\PyAgent\src\external_candidates\auto\0xsojalsec_owl_py_generate_text_embedding_data_7a1164e6a0d6.py")
spec = importlib.util.spec_from_file_location('mod_under_test', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

assert hasattr(mod, 'GenerateTextEmbeddingDataPromptTemplateDict'), 'missing GenerateTextEmbeddingDataPromptTemplateDict'
