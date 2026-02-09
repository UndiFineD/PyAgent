# Extracted from: C:\DEV\PyAgent\.external\agentcloud\agent-backend\src\models\sockets.py
import json
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class SocketEvents(str, Enum):
    MESSAGE = "message"
    STOP_GENERATING = "stop_generating"


class MessageType(str, Enum):
    TEXT = "text"
    CODE = "code"


class MessageDisplayType(str, Enum):
    BUBBLE = "bubble"
    INLINE = "inline"


class Message(BaseModel):
    text: str
    chunkId: Optional[str] = None
    codeBlock: Optional[List[str]] = None
    tokens: Optional[int] = None
    deltaTokens: Optional[int] = None
    first: Optional[bool] = False
    single: Optional[bool] = False
    type: Optional[MessageType] = MessageType.TEXT
    displayType: Optional[MessageDisplayType] = MessageDisplayType.BUBBLE
    timestamp: Optional[float] = datetime.now().timestamp() * 1000
    overwrite: Optional[bool] = False


class SocketMessage(BaseModel):
    room: str
    authorName: Optional[str]
    message: Message
    isFeedback: Optional[bool] = False

    def json(self, **kwargs):
        # Convert the model to a dictionary and replace enum with its value
        d = self.model_dump()
        d["event"] = d["event"].value  # Convert Enum to string
        return json.dumps(d, **kwargs)
