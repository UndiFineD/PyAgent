# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_evermemos.py\src.py\core.py\component.py\llm.py\llm_adapter.py\message_43a9931da206.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-EverMemOS\src\core\component\llm\llm_adapter\message.py

from dataclasses import dataclass

from enum import Enum

from typing import Dict


class MessageRole(Enum):
    """Message role enumeration"""

    SYSTEM = "system"

    USER = "user"

    ASSISTANT = "assistant"


@dataclass
class ChatMessage:
    """Chat message data class"""

    role: MessageRole

    content: str

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary format"""

        return {"role": self.role.value, "content": self.content}
