# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\core.py\component.py\llm.py\llm_adapter.py\llm_backend_adapter_26c6c7936b25.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\component\llm\llm_adapter\llm_backend_adapter.py

from abc import ABC, abstractmethod

from typing import AsyncGenerator, List, Union

from core.component.llm.llm_adapter.completion import (

    ChatCompletionRequest,

    ChatCompletionResponse,

)

class LLMBackendAdapter(ABC):

    """Abstract base class for LLM backend adapter"""

    @abstractmethod

    async def chat_completion(

        self, request: ChatCompletionRequest

    ) -> Union[ChatCompletionResponse, AsyncGenerator[str, None]]:

        """Perform chat completion"""

        pass

    @abstractmethod

    def get_available_models(self) -> List[str]:

        """Get list of available models"""

        pass

