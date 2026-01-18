# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 40: Reasoning Engine - Thinking Token and Tool Call Extraction
# Inspired by vLLM's reasoning and tool_parsers

"""
ReasoningEngine: Unified reasoning extraction for LLM outputs.

Provides:
- Streaming extraction of thinking tokens (<think>...</think>)
- Tool/function call parsing with multiple formats
- Cross-model format normalization
- Reasoning chain visualization and caching
"""

from __future__ import annotations

import json
import re
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any, Callable, Dict, Generator, Iterator, List, 
    Optional, Set, Tuple, Union
)
from collections import deque


# =============================================================================
# Enums
# =============================================================================

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


# =============================================================================
# Data Classes
# =============================================================================

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
        return len(self.thinking_blocks) > 0
    
    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0
    
    @property
    def total_thinking_length(self) -> int:
        return sum(len(block) for block in self.thinking_blocks)


# =============================================================================
# Abstract Base Classes
# =============================================================================

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


# =============================================================================
# DeepSeek R1 Reasoning Parser
# =============================================================================

class DeepSeekReasoningParser(ReasoningParser):
    """Parser for DeepSeek R1-style <think>...</think> blocks."""
    
    def __init__(self):
        super().__init__(
            reasoning_format=ReasoningFormat.DEEPSEEK_R1,
            start_marker="<think>",
            end_marker="</think>"
        )
        # Compiled regex for efficiency
        self._pattern = re.compile(
            r'<think>(.*?)</think>',
            re.DOTALL
        )
    
    def extract_thinking(self, text: str) -> Tuple[str, List[ThinkingBlock]]:
        """Extract all thinking blocks from text."""
        blocks = []
        content_parts = []
        last_end = 0
        
        for match in self._pattern.finditer(text):
            # Add content before this block
            content_parts.append(text[last_end:match.start()])
            
            # Create thinking block
            block = ThinkingBlock(
                content=match.group(1).strip(),
                start_position=match.start(),
                end_position=match.end(),
                model_format=self.reasoning_format,
                step_count=len(match.group(1).strip().split('\n'))
            )
            blocks.append(block)
            last_end = match.end()
        
        # Add remaining content
        content_parts.append(text[last_end:])
        
        return ''.join(content_parts).strip(), blocks
    
    def parse_streaming(
        self,
        token_stream: Iterator[str]
    ) -> Generator[Tuple[str, bool], None, ParseResult]:
        """Stream parse with state machine."""
        content_buffer = []
        thinking_buffer = []
        current_block_start = 0
        position = 0
        
        for token in token_stream:
            self._buffer += token
            position += len(token)
            
            while True:
                if self._state == ParseState.IDLE:
                    # Look for start marker
                    idx = self._buffer.find(self.start_marker)
                    if idx == -1:
                        # No marker, emit safe portion
                        if len(self._buffer) > len(self.start_marker):
                            emit = self._buffer[:-len(self.start_marker)]
                            content_buffer.append(emit)
                            self._buffer = self._buffer[-len(self.start_marker):]
                            yield (emit, False)
                        break
                    else:
                        # Found start, emit content before
                        if idx > 0:
                            emit = self._buffer[:idx]
                            content_buffer.append(emit)
                            yield (emit, False)
                        self._buffer = self._buffer[idx + len(self.start_marker):]
                        self._state = ParseState.IN_THINK
                        current_block_start = position - len(self._buffer)
                        
                elif self._state == ParseState.IN_THINK:
                    # Look for end marker
                    idx = self._buffer.find(self.end_marker)
                    if idx == -1:
                        # Still in thinking, emit as thinking
                        if len(self._buffer) > len(self.end_marker):
                            emit = self._buffer[:-len(self.end_marker)]
                            thinking_buffer.append(emit)
                            self._buffer = self._buffer[-len(self.end_marker):]
                            yield (emit, True)
                        break
                    else:
                        # Found end
                        thinking_content = self._buffer[:idx]
                        thinking_buffer.append(thinking_content)
                        yield (thinking_content, True)
                        
                        # Create block
                        block = ThinkingBlock(
                            content=''.join(thinking_buffer).strip(),
                            start_position=current_block_start,
                            end_position=position,
                            model_format=self.reasoning_format
                        )
                        self._thinking_blocks.append(block)
                        thinking_buffer = []
                        
                        self._buffer = self._buffer[idx + len(self.end_marker):]
                        self._state = ParseState.IDLE
        
        # Finalize
        if self._buffer:
            if self._state == ParseState.IN_THINK:
                thinking_buffer.append(self._buffer)
            else:
                content_buffer.append(self._buffer)
                yield (self._buffer, False)
        
        return ParseResult(
            content=''.join(content_buffer).strip(),
            thinking_blocks=self._thinking_blocks,
            raw_text=''.join(content_buffer) + ''.join(thinking_buffer),
            tokens_processed=position
        )


# =============================================================================
# Qwen3 Reasoning Parser
# =============================================================================

class QwenReasoningParser(ReasoningParser):
    """Parser for Qwen3-style reasoning with enable_thinking flag."""
    
    def __init__(self, enable_thinking: bool = True):
        super().__init__(
            reasoning_format=ReasoningFormat.QWEN3,
            start_marker="<think>",
            end_marker="</think>"
        )
        self.enable_thinking = enable_thinking
        self._pattern = re.compile(r'<think>(.*?)</think>', re.DOTALL)
    
    def extract_thinking(self, text: str) -> Tuple[str, List[ThinkingBlock]]:
        """Extract thinking with Qwen3 format awareness."""
        if not self.enable_thinking:
            return text, []
        
        blocks = []
        content_parts = []
        last_end = 0
        
        for match in self._pattern.finditer(text):
            content_parts.append(text[last_end:match.start()])
            
            thinking_content = match.group(1).strip()
            block = ThinkingBlock(
                content=thinking_content,
                start_position=match.start(),
                end_position=match.end(),
                model_format=self.reasoning_format,
                step_count=len([l for l in thinking_content.split('\n') if l.strip()])
            )
            blocks.append(block)
            last_end = match.end()
        
        content_parts.append(text[last_end:])
        return ''.join(content_parts).strip(), blocks
    
    def parse_streaming(
        self,
        token_stream: Iterator[str]
    ) -> Generator[Tuple[str, bool], None, ParseResult]:
        """Stream parse with thinking extraction."""
        # Reuse DeepSeek implementation with Qwen format
        deepseek = DeepSeekReasoningParser()
        deepseek.reasoning_format = self.reasoning_format
        
        result = None
        for token, is_thinking in deepseek.parse_streaming(token_stream):
            if not self.enable_thinking and is_thinking:
                continue
            yield (token, is_thinking)
            result = None
        
        # Return final result
        return ParseResult(
            content="",
            thinking_blocks=deepseek._thinking_blocks,
            raw_text=""
        )


# =============================================================================
# Generic Reasoning Parser
# =============================================================================

class GenericReasoningParser(ReasoningParser):
    """Configurable parser for any reasoning format."""
    
    def __init__(
        self,
        start_marker: str = "<think>",
        end_marker: str = "</think>",
        nested: bool = False,
    ):
        super().__init__(
            reasoning_format=ReasoningFormat.GENERIC,
            start_marker=start_marker,
            end_marker=end_marker
        )
        self.nested = nested
        self._pattern = re.compile(
            re.escape(start_marker) + r'(.*?)' + re.escape(end_marker),
            re.DOTALL
        )
    
    def extract_thinking(self, text: str) -> Tuple[str, List[ThinkingBlock]]:
        """Extract thinking with configurable markers."""
        blocks = []
        content_parts = []
        last_end = 0
        
        for match in self._pattern.finditer(text):
            content_parts.append(text[last_end:match.start()])
            
            block = ThinkingBlock(
                content=match.group(1).strip(),
                start_position=match.start(),
                end_position=match.end(),
                model_format=self.reasoning_format
            )
            blocks.append(block)
            last_end = match.end()
        
        content_parts.append(text[last_end:])
        return ''.join(content_parts).strip(), blocks
    
    def parse_streaming(
        self,
        token_stream: Iterator[str]
    ) -> Generator[Tuple[str, bool], None, ParseResult]:
        """Stream parse with generic markers."""
        content = []
        thinking = []
        position = 0
        
        for token in token_stream:
            self._buffer += token
            position += len(token)
            
            if self._state == ParseState.IDLE:
                if self.start_marker in self._buffer:
                    idx = self._buffer.find(self.start_marker)
                    if idx > 0:
                        emit = self._buffer[:idx]
                        content.append(emit)
                        yield (emit, False)
                    self._buffer = self._buffer[idx + len(self.start_marker):]
                    self._state = ParseState.IN_THINK
                    self._current_block_start = position
                elif len(self._buffer) > len(self.start_marker) * 2:
                    emit = self._buffer[:-len(self.start_marker)]
                    content.append(emit)
                    yield (emit, False)
                    self._buffer = self._buffer[-len(self.start_marker):]
                    
            elif self._state == ParseState.IN_THINK:
                if self.end_marker in self._buffer:
                    idx = self._buffer.find(self.end_marker)
                    think_content = self._buffer[:idx]
                    thinking.append(think_content)
                    yield (think_content, True)
                    
                    block = ThinkingBlock(
                        content=''.join(thinking).strip(),
                        start_position=self._current_block_start,
                        end_position=position,
                        model_format=self.reasoning_format
                    )
                    self._thinking_blocks.append(block)
                    thinking = []
                    
                    self._buffer = self._buffer[idx + len(self.end_marker):]
                    self._state = ParseState.IDLE
                elif len(self._buffer) > len(self.end_marker) * 2:
                    emit = self._buffer[:-len(self.end_marker)]
                    thinking.append(emit)
                    yield (emit, True)
                    self._buffer = self._buffer[-len(self.end_marker):]
        
        # Final flush
        if self._buffer:
            if self._state == ParseState.IN_THINK:
                thinking.append(self._buffer)
            else:
                content.append(self._buffer)
                yield (self._buffer, False)
        
        return ParseResult(
            content=''.join(content).strip(),
            thinking_blocks=self._thinking_blocks,
            raw_text=''.join(content) + ''.join(thinking),
            tokens_processed=position
        )


# =============================================================================
# OpenAI Tool Parser
# =============================================================================

class OpenAIToolParser(ToolParser):
    """Parser for OpenAI function calling format."""
    
    def __init__(self, strict: bool = False):
        super().__init__(ToolCallFormat.OPENAI, strict)
        self._function_pattern = re.compile(
            r'"function_call"\s*:\s*\{[^}]+\}',
            re.DOTALL
        )
    
    def parse_tool_calls(self, text: str) -> List[ToolCall]:
        """Parse OpenAI-style tool calls from response."""
        calls = []
        
        try:
            # Try parsing as JSON first
            data = json.loads(text)
            if isinstance(data, dict):
                if "tool_calls" in data:
                    for tc in data["tool_calls"]:
                        call = ToolCall(
                            id=tc.get("id", self.generate_call_id()),
                            name=tc.get("function", {}).get("name", ""),
                            arguments=json.loads(tc.get("function", {}).get("arguments", "{}")),
                            raw_text=json.dumps(tc),
                            format=self.tool_format
                        )
                        calls.append(call)
                elif "function_call" in data:
                    fc = data["function_call"]
                    call = ToolCall(
                        id=self.generate_call_id(),
                        name=fc.get("name", ""),
                        arguments=json.loads(fc.get("arguments", "{}")),
                        raw_text=json.dumps(fc),
                        format=self.tool_format
                    )
                    calls.append(call)
        except (json.JSONDecodeError, KeyError):
            pass
        
        return calls
    
    def parse_streaming(
        self,
        token_stream: Iterator[str]
    ) -> Generator[Tuple[str, Optional[ToolCall]], None, List[ToolCall]]:
        """Stream parse for tool calls."""
        buffer = ""
        calls = []
        
        for token in token_stream:
            buffer += token
            yield (token, None)
        
        # Parse complete buffer
        calls = self.parse_tool_calls(buffer)
        return calls


# =============================================================================
# Hermes Tool Parser
# =============================================================================

class HermesToolParser(ToolParser):
    """Parser for Hermes-style <tool_call>...</tool_call> format."""
    
    def __init__(self, strict: bool = False):
        super().__init__(ToolCallFormat.HERMES, strict)
        self._pattern = re.compile(
            r'<tool_call>\s*(.*?)\s*</tool_call>',
            re.DOTALL
        )
    
    def parse_tool_calls(self, text: str) -> List[ToolCall]:
        """Parse Hermes-style tool calls."""
        calls = []
        
        for match in self._pattern.finditer(text):
            try:
                content = match.group(1).strip()
                data = json.loads(content)
                
                call = ToolCall(
                    id=data.get("id", self.generate_call_id()),
                    name=data.get("name", data.get("function", "")),
                    arguments=data.get("arguments", data.get("parameters", {})),
                    raw_text=match.group(0),
                    format=self.tool_format,
                    position=match.start()
                )
                calls.append(call)
            except json.JSONDecodeError:
                if self.strict:
                    raise
                continue
        
        return calls
    
    def parse_streaming(
        self,
        token_stream: Iterator[str]
    ) -> Generator[Tuple[str, Optional[ToolCall]], None, List[ToolCall]]:
        """Stream parse with tool call detection."""
        buffer = ""
        calls = []
        in_tool = False
        tool_buffer = ""
        
        for token in token_stream:
            buffer += token
            
            if not in_tool:
                if "<tool_call>" in buffer:
                    idx = buffer.find("<tool_call>")
                    content_before = buffer[:idx]
                    if content_before:
                        yield (content_before, None)
                    buffer = buffer[idx + len("<tool_call>"):]
                    in_tool = True
                    tool_buffer = ""
                else:
                    if len(buffer) > 20:
                        emit = buffer[:-20]
                        yield (emit, None)
                        buffer = buffer[-20:]
            else:
                if "</tool_call>" in buffer:
                    idx = buffer.find("</tool_call>")
                    tool_buffer += buffer[:idx]
                    
                    try:
                        data = json.loads(tool_buffer.strip())
                        call = ToolCall(
                            id=data.get("id", self.generate_call_id()),
                            name=data.get("name", ""),
                            arguments=data.get("arguments", {}),
                            raw_text=f"<tool_call>{tool_buffer}</tool_call>",
                            format=self.tool_format
                        )
                        calls.append(call)
                        yield ("", call)
                    except json.JSONDecodeError:
                        pass
                    
                    buffer = buffer[idx + len("</tool_call>"):]
                    in_tool = False
                else:
                    tool_buffer += token
        
        return calls


# =============================================================================
# Unified Reasoning Engine
# =============================================================================

class ReasoningEngine:
    """
    Unified reasoning and tool call extraction engine.
    
    Features beyond vLLM:
    - Multi-format support with auto-detection
    - Reasoning chain visualization
    - Thought step caching for speculative execution
    - Quality scoring for reasoning blocks
    - Cross-model format normalization
    """
    
    # Parser registry
    _reasoning_parsers: Dict[ReasoningFormat, type] = {
        ReasoningFormat.DEEPSEEK_R1: DeepSeekReasoningParser,
        ReasoningFormat.QWEN3: QwenReasoningParser,
        ReasoningFormat.GENERIC: GenericReasoningParser,
    }
    
    _tool_parsers: Dict[ToolCallFormat, type] = {
        ToolCallFormat.OPENAI: OpenAIToolParser,
        ToolCallFormat.HERMES: HermesToolParser,
    }
    
    def __init__(
        self,
        reasoning_format: ReasoningFormat = ReasoningFormat.GENERIC,
        tool_format: ToolCallFormat = ToolCallFormat.NONE,
        enable_thinking: bool = True,
        cache_thoughts: bool = False,
        max_cached_thoughts: int = 1000,
    ):
        self.reasoning_format = reasoning_format
        self.tool_format = tool_format
        self.enable_thinking = enable_thinking
        self.cache_thoughts = cache_thoughts
        
        # Initialize parsers
        self._reasoning_parser: Optional[ReasoningParser] = None
        self._tool_parser: Optional[ToolParser] = None
        
        if reasoning_format != ReasoningFormat.NONE:
            parser_cls = self._reasoning_parsers.get(reasoning_format, GenericReasoningParser)
            self._reasoning_parser = parser_cls()
        
        if tool_format != ToolCallFormat.NONE:
            parser_cls = self._tool_parsers.get(tool_format, OpenAIToolParser)
            self._tool_parser = parser_cls()
        
        # Thought cache for speculative execution
        self._thought_cache: Dict[str, ThinkingBlock] = {}
        self._thought_lru: deque = deque(maxlen=max_cached_thoughts)
        
        # Statistics
        self._stats = {
            "total_parsed": 0,
            "thinking_blocks_extracted": 0,
            "tool_calls_parsed": 0,
            "cache_hits": 0,
        }
    
    def parse(self, text: str) -> ParseResult:
        """Parse text for reasoning and tool calls."""
        start_time = time.time()
        
        content = text
        thinking_blocks = []
        tool_calls = []
        
        # Extract thinking
        if self._reasoning_parser and self.enable_thinking:
            content, thinking_blocks = self._reasoning_parser.extract_thinking(text)
            
            # Cache thoughts
            if self.cache_thoughts:
                for block in thinking_blocks:
                    cache_key = hash(block.content[:100])
                    if cache_key not in self._thought_cache:
                        self._thought_cache[str(cache_key)] = block
                        self._thought_lru.append(cache_key)
        
        # Parse tool calls
        if self._tool_parser:
            tool_calls = self._tool_parser.parse_tool_calls(content)
        
        # Update stats
        self._stats["total_parsed"] += 1
        self._stats["thinking_blocks_extracted"] += len(thinking_blocks)
        self._stats["tool_calls_parsed"] += len(tool_calls)
        
        return ParseResult(
            content=content,
            thinking_blocks=thinking_blocks,
            tool_calls=tool_calls,
            raw_text=text,
            parse_time_ms=(time.time() - start_time) * 1000,
            tokens_processed=len(text)
        )
    
    def parse_streaming(
        self,
        token_stream: Iterator[str]
    ) -> Generator[Tuple[str, bool, Optional[ToolCall]], None, ParseResult]:
        """
        Parse streaming tokens.
        
        Yields: (token, is_thinking, tool_call_if_complete)
        """
        buffer = ""
        thinking_blocks = []
        tool_calls = []
        content_parts = []
        
        for token in token_stream:
            buffer += token
            is_thinking = False
            tool_call = None
            
            # Check for reasoning markers
            if self._reasoning_parser:
                if self._reasoning_parser._state == ParseState.IN_THINK:
                    is_thinking = True
                elif self._reasoning_parser.start_marker in buffer:
                    self._reasoning_parser._state = ParseState.IN_THINK
                    is_thinking = True
            
            if not is_thinking:
                content_parts.append(token)
            
            yield (token, is_thinking, tool_call)
        
        # Final parse for complete result
        result = self.parse(buffer)
        return result
    
    def detect_format(self, text: str) -> ReasoningFormat:
        """Auto-detect reasoning format from text."""
        if "<think>" in text and "</think>" in text:
            return ReasoningFormat.DEEPSEEK_R1
        elif "<thinking>" in text:
            return ReasoningFormat.CLAUDE
        elif "[THINK]" in text:
            return ReasoningFormat.MISTRAL
        elif "<|start_think|>" in text:
            return ReasoningFormat.LLAMA_COT
        return ReasoningFormat.NONE
    
    def score_reasoning(self, block: ThinkingBlock) -> float:
        """Score reasoning quality (0-1)."""
        score = 0.0
        content = block.content
        
        # Length bonus (prefer substantial reasoning)
        if len(content) > 100:
            score += 0.2
        if len(content) > 500:
            score += 0.1
        
        # Step count bonus
        steps = block.get_steps()
        if len(steps) >= 3:
            score += 0.2
        if len(steps) >= 5:
            score += 0.1
        
        # Logical markers bonus
        logical_markers = ["therefore", "because", "thus", "hence", "so", 
                         "first", "second", "finally", "step", "let's"]
        for marker in logical_markers:
            if marker.lower() in content.lower():
                score += 0.05
        
        # Cap at 1.0
        return min(score, 1.0)
    
    def visualize_reasoning(self, result: ParseResult) -> str:
        """Create visual representation of reasoning chain."""
        lines = ["=" * 60, "REASONING CHAIN VISUALIZATION", "=" * 60]
        
        for i, block in enumerate(result.thinking_blocks):
            lines.append(f"\n📝 Thinking Block {i+1}")
            lines.append("-" * 40)
            
            steps = block.get_steps()
            for j, step in enumerate(steps):
                lines.append(f"  {j+1}. {step[:80]}{'...' if len(step) > 80 else ''}")
            
            score = self.score_reasoning(block)
            lines.append(f"\n  Quality Score: {score:.2f}")
        
        lines.append("\n" + "=" * 60)
        lines.append(f"Final Content: {result.content[:100]}...")
        
        if result.tool_calls:
            lines.append(f"\n🔧 Tool Calls: {len(result.tool_calls)}")
            for tc in result.tool_calls:
                lines.append(f"  - {tc.name}({json.dumps(tc.arguments)[:50]}...)")
        
        return "\n".join(lines)
    
    def get_stats(self) -> Dict[str, int]:
        """Return parsing statistics."""
        return self._stats.copy()
    
    def reset(self) -> None:
        """Reset engine state."""
        if self._reasoning_parser:
            self._reasoning_parser.reset()
        if self._tool_parser:
            self._tool_parser.reset()
        self._thought_cache.clear()
        self._thought_lru.clear()


# =============================================================================
# Factory Functions
# =============================================================================

def create_reasoning_engine(
    model_name: str = "",
    enable_thinking: bool = True,
    tool_format: ToolCallFormat = ToolCallFormat.NONE,
) -> ReasoningEngine:
    """Create reasoning engine based on model name."""
    # Auto-detect format from model name
    reasoning_format = ReasoningFormat.GENERIC
    
    model_lower = model_name.lower()
    if "deepseek" in model_lower or "r1" in model_lower:
        reasoning_format = ReasoningFormat.DEEPSEEK_R1
    elif "qwen" in model_lower:
        reasoning_format = ReasoningFormat.QWEN3
    elif "claude" in model_lower:
        reasoning_format = ReasoningFormat.CLAUDE
    elif "mistral" in model_lower:
        reasoning_format = ReasoningFormat.MISTRAL
    
    return ReasoningEngine(
        reasoning_format=reasoning_format,
        tool_format=tool_format,
        enable_thinking=enable_thinking
    )


def create_tool_parser(
    format_type: ToolCallFormat = ToolCallFormat.OPENAI,
    strict: bool = False,
) -> ToolParser:
    """Create tool parser of specified format."""
    parsers = {
        ToolCallFormat.OPENAI: OpenAIToolParser,
        ToolCallFormat.HERMES: HermesToolParser,
    }
    
    parser_cls = parsers.get(format_type, OpenAIToolParser)
    return parser_cls(strict=strict)
