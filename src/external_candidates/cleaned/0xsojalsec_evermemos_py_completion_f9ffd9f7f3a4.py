# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\core.py\component.py\llm.py\llm_adapter.py\completion_f9ffd9f7f3a4.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\component\llm\llm_adapter\completion.py

from dataclasses import dataclass, field

from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from core.component.llm.llm_adapter.message import ChatMessage


@dataclass
class ChatCompletionRequest:
    """Chat completion request data class"""

    messages: List[ChatMessage]

    model: Optional[str] = None

    temperature: Optional[float] = None

    max_tokens: Optional[int] = None

    top_p: Optional[float] = None

    frequency_penalty: Optional[float] = None

    presence_penalty: Optional[float] = None

    thinking_budget: Optional[int] = None  # Add support for thinking_budget parameter

    stream: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""

        data = {
            "messages": [msg.to_dict() for msg in self.messages],
            "stream": self.stream,
        }

        # Only add non-None fields

        for field_name in [
            "model",
            "temperature",
            "max_tokens",
            "top_p",
            "frequency_penalty",
            "presence_penalty",
            "thinking_budget",
        ]:
            value = getattr(self, field_name)

            if value is not None:
                data[field_name] = value

        return data


class ChatCompletionResponse(BaseModel, extra="allow"):
    """Chat completion response data class, compatible with extra fields"""

    id: str

    object: str

    created: int

    model: str

    choices: List[Dict[str, Any]]

    usage: Optional[Dict[str, Any]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatCompletionResponse":
        """Create response object from dictionary"""

        return cls(**data)
