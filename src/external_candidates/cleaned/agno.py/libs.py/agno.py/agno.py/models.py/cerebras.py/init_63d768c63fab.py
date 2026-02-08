# Extracted from: C:\DEV\PyAgent\.external\agno\libs\agno\agno\models\cerebras\__init__.py
from agno.models.cerebras.cerebras import Cerebras

try:
    from agno.models.cerebras.cerebras_openai import CerebrasOpenAI
except ImportError:

    class CerebrasOpenAI:  # type: ignore
        def __init__(self, *args, **kwargs):
            raise ImportError("`openai` not installed. Please install it via `pip install openai`")


__all__ = ["Cerebras", "CerebrasOpenAI"]
