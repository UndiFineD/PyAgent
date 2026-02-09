# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-PraisonAI\src\praisonai-agents\praisonaiagents\llm\__init__.py
import os

# Ensure litellm telemetry is disabled before imports
os.environ["LITELLM_TELEMETRY"] = "False"

# Import modules
from .llm import LLM, LLMContextLengthExceededException
from .model_capabilities import (
    supports_streaming_with_tools,
    supports_structured_outputs,
)
from .model_router import (
    ModelProfile,
    ModelRouter,
    TaskComplexity,
    create_routing_agent,
)
from .openai_client import (
    ChatCompletion,
    ChatCompletionMessage,
    Choice,
    CompletionTokensDetails,
    CompletionUsage,
    OpenAIClient,
    PromptTokensDetails,
    ToolCall,
    get_openai_client,
    process_stream_chunks,
)

__all__ = [
    "LLM",
    "LLMContextLengthExceededException",
    "OpenAIClient",
    "get_openai_client",
    "ChatCompletionMessage",
    "Choice",
    "CompletionTokensDetails",
    "PromptTokensDetails",
    "CompletionUsage",
    "ChatCompletion",
    "ToolCall",
    "process_stream_chunks",
    "supports_structured_outputs",
    "supports_streaming_with_tools",
    "ModelRouter",
    "ModelProfile",
    "TaskComplexity",
    "create_routing_agent",
]
