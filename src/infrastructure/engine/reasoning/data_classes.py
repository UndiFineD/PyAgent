import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from .enums import ReasoningFormat, ToolCallFormat

@dataclass
class ReasoningToken:
    """A single token with reasoning metadata."""
    token_id: int
    text: str
    is_thinking: bool = False
    is_tool_call: bool = False
    thinking_depth: int = 0
    timestamp: float = field(default_factory=time.time)

@dataclass
class ThinkingBlock:
    """A complete thinking/reasoning block."""
    content: str
    start_position: int
    end_position: int
    model_format: ReasoningFormat = ReasoningFormat.GENERIC
    quality_score: Optional[float] = None
    step_count: int = 0
    tokens: List[ReasoningToken] = field(default_factory=list)
    
    def __len__(self) -> int:
        return len(self.content)
    
    def get_steps(self, delimiter: str = "\n") -> List[str]:
        """Extract reasoning steps."""
        steps = [s.strip() for s in self.content.split(delimiter) if s.strip()]
        return steps

@dataclass
class ToolCall:
    """A parsed tool/function call."""
    id: str
    name: str
    arguments: Dict[str, Any]
    raw_text: str = ""
    format: ToolCallFormat = ToolCallFormat.OPENAI
    position: int = 0
    is_complete: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": "function",
            "function": {
                "name": self.name,
                "arguments": json.dumps(self.arguments)
            }
        }

@dataclass
class ToolCallResult:
    """Result from tool execution."""
    tool_call_id: str
    content: str
    is_error: bool = False
    execution_time: float = 0.0

@dataclass
class ParseResult:
    """Result of parsing a generation stream."""
    content: str                                  # Final content (without thinking)
    thinking_blocks: List[ThinkingBlock] = field(default_factory=list)
    tool_calls: List[ToolCall] = field(default_factory=list)
    raw_text: str = ""                           # Original full text
    parse_time_ms: float = 0.0
    tokens_processed: int = 0
    
    @property
    def has_thinking(self) -> bool:
        return bool(self.thinking_blocks)
    
    @property
    def has_tool_calls(self) -> bool:
        return bool(self.tool_calls)
    
    @property
    def total_thinking_length(self) -> int:
        return sum(len(block) for block in self.thinking_blocks)
