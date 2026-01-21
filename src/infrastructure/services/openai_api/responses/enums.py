# SPDX-License-Identifier: Apache-2.0
from enum import Enum

class ResponseStatus(Enum):
    """Response processing status."""
    QUEUED = "queued"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"
    INCOMPLETE = "incomplete"

class ResponseType(Enum):
    """Response object types."""
    MESSAGE = "message"
    TOOL_CALL = "function_call"
    REASONING = "reasoning"

class ContentPartType(Enum):
    """Content part types."""
    TEXT = "text"
    IMAGE_URL = "image_url"
    IMAGE_FILE = "image_file"
    AUDIO = "audio"
    REFUSAL = "refusal"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"

class ToolType(Enum):
    """Tool types."""
    FUNCTION = "function"
    CODE_INTERPRETER = "code_interpreter"
    FILE_SEARCH = "file_search"
    WEB_SEARCH = "web_search"
    COMPUTER = "computer"
    MCP = "mcp"

class RoleType(Enum):
    """Message role types."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"
    DEVELOPER = "developer"
