from enum import Enum, auto

class ReasoningFormat(Enum):
    """Supported reasoning token formats."""
    DEEPSEEK_R1 = auto()      # <think>...</think>
    QWEN3 = auto()            # <think>...</think> with reasoning_content
    MISTRAL = auto()          # [THINK]...[/THINK]
    LLAMA_COT = auto()        # <|start_think|>...<|end_think|>
    CLAUDE = auto()           # <thinking>...</thinking>
    O1_STYLE = auto()         # Internal reasoning blocks
    GENERIC = auto()          # Configurable markers
    NONE = auto()             # No reasoning extraction

class ToolCallFormat(Enum):
    """Supported tool/function call formats."""
    OPENAI = auto()           # OpenAI function calling
    HERMES = auto()           # <tool_call>JSON</tool_call>
    MISTRAL = auto()          # [TOOL_CALLS]
    LLAMA = auto()            # <|python_tag|>
    ANTHROPIC = auto()        # tool_use blocks
    CUSTOM = auto()           # Configurable format
    NONE = auto()             # No tool parsing

class ParseState(Enum):
    """State machine states for streaming parsing."""
    IDLE = auto()             # Normal content
    IN_THINK = auto()         # Inside thinking block
    IN_TOOL = auto()          # Inside tool call
    ACCUMULATING = auto()     # Accumulating potential marker
