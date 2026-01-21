from abc import ABC, abstractmethod
from typing import Generator, Iterator, List, Optional, Tuple
from .enums import ReasoningFormat, ToolCallFormat, ParseState
from .data_classes import ThinkingBlock, ToolCall, ParseResult

class ReasoningParser(ABC):
    """Abstract base for reasoning token extraction."""
    
    def __init__(
        self,
        reasoning_format: ReasoningFormat = ReasoningFormat.GENERIC,
        start_marker: str = "<think>",
        end_marker: str = "</think>",
    ):
        self.reasoning_format = reasoning_format
        self.start_marker = start_marker
        self.end_marker = end_marker
        self._state = ParseState.IDLE
        self._buffer = ""
        self._thinking_blocks: List[ThinkingBlock] = []
        self._current_block_start = 0
    
    @abstractmethod
    def extract_thinking(self, text: str) -> Tuple[str, List[ThinkingBlock]]:
        """Extract thinking blocks from text, return content and blocks."""
        pass
    
    @abstractmethod
    def parse_streaming(
        self, 
        token_stream: Iterator[str]
    ) -> Generator[Tuple[str, bool], None, ParseResult]:
        """Parse streaming tokens, yield (token, is_thinking)."""
        pass
    
    def reset(self) -> None:
        """Reset parser state."""
        self._state = ParseState.IDLE
        self._buffer = ""
        self._thinking_blocks = []
        self._current_block_start = 0

class ToolParser(ABC):
    """Abstract base for tool/function call parsing."""
    
    def __init__(
        self,
        tool_format: ToolCallFormat = ToolCallFormat.OPENAI,
        strict: bool = False,
    ):
        self.tool_format = tool_format
        self.strict = strict
        self._tool_call_counter = 0
    
    @abstractmethod
    def parse_tool_calls(self, text: str) -> List[ToolCall]:
        """Parse tool calls from text."""
        pass
    
    @abstractmethod
    def parse_streaming(
        self,
        token_stream: Iterator[str]
    ) -> Generator[Tuple[str, Optional[ToolCall]], None, List[ToolCall]]:
        """Parse streaming tokens for tool calls."""
        pass
    
    def generate_call_id(self) -> str:
        """Generate unique tool call ID."""
        self._tool_call_counter += 1
        return f"call_{self._tool_call_counter:08d}"
    
    def reset(self) -> None:
        """Reset parser state."""
        self._tool_call_counter = 0
