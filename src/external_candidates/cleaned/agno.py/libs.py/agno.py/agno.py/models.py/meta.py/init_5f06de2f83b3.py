# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\models\meta\__init__.py
from agno.models.meta.llama import Llama

try:
    from agno.models.meta.llama_openai import LlamaOpenAI
except ImportError:

    class LlamaOpenAI:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ImportError("`openai` not installed. Please install it via `pip install openai`")


__all__ = ["Llama", "LlamaOpenAI"]
