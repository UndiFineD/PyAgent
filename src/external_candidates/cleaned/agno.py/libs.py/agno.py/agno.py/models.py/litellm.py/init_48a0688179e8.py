# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\models\litellm\__init__.py
from agno.models.litellm.chat import LiteLLM

try:
    from agno.models.litellm.litellm_openai import LiteLLMOpenAI
except ImportError:

    class LiteLLMOpenAI:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ImportError("`openai` not installed. Please install using `pip install openai`")


__all__ = [
    "LiteLLM",
]
