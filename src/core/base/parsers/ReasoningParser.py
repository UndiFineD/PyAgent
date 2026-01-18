"""
ReasoningParser - Extensible framework for extracting reasoning from LLM outputs.

Phase 22 implementation based on vLLM's reasoning parser patterns.
Provides an extensible framework for extracting reasoning/thinking content from model outputs.

Features:
- ReasoningParser abstract base class
- ReasoningParserManager with lazy registration
- Built-in parsers: XML think blocks, JSON reasoning, Markdown think blocks
- extract_reasoning() for complete outputs
- extract_reasoning_streaming() for streaming outputs
- @reasoning_parser decorator for custom parsers

Use Cases:
- Chain-of-thought reasoning extraction
- Separating thinking from final answers
- Processing structured reasoning outputs
- Supporting multiple model formats (DeepSeek, Qwen, etc.)
"""

from __future__ import annotations

import importlib
import logging
import re
from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, ClassVar, TypeVar

logger = logging.getLogger(__name__)

_T = TypeVar("_T")


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class ReasoningResult:
    """
    Result of reasoning extraction.
    
    Attributes:
        reasoning: The extracted reasoning/thinking content.
        content: The extracted content/answer.
        reasoning_tokens: Token IDs for reasoning (if available).
        content_tokens: Token IDs for content (if available).
        is_complete: Whether reasoning extraction is complete.
    """
    reasoning: str | None = None
    content: str | None = None
    reasoning_tokens: list[int] | None = None
    content_tokens: list[int] | None = None
    is_complete: bool = True


@dataclass
class StreamingReasoningState:
    """
    State for streaming reasoning extraction.
    
    Tracks the current state of reasoning extraction during streaming.
    """
    accumulated_text: str = ""
    accumulated_tokens: list[int] = field(default_factory=list)
    in_reasoning: bool = False
    reasoning_buffer: str = ""
    content_buffer: str = ""
    reasoning_complete: bool = False


# ============================================================================
# Abstract Base Class
# ============================================================================


class ReasoningParser(ABC):
    """
    Abstract reasoning parser class for extracting reasoning from model outputs.
    
    Subclasses must implement:
    - is_reasoning_end: Check if reasoning section has ended
    - extract_content_ids: Extract content token IDs from full output
    - extract_reasoning: Extract reasoning from complete output
    - extract_reasoning_streaming: Extract reasoning incrementally
    
    Attributes:
        tokenizer: The tokenizer used for token-level operations.
    """
    
    # Class-level name for registration
    name: ClassVar[str] = "base"
    
    def __init__(self, tokenizer: Any = None, **kwargs: Any) -> None:
        """
        Initialize the reasoning parser.
        
        Args:
            tokenizer: Tokenizer for token-level operations (optional).
            **kwargs: Additional configuration options.
        """
        self.model_tokenizer = tokenizer
    
    @cached_property
    def vocab(self) -> dict[str, int]:
        """Get tokenizer vocabulary."""
        if self.model_tokenizer is None:
            return {}
        # Support both .vocab and .get_vocab()
        if hasattr(self.model_tokenizer, "get_vocab"):
            return self.model_tokenizer.get_vocab()
        return getattr(self.model_tokenizer, "vocab", {})
    
    @abstractmethod
    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        """
        Check if the reasoning content ends in the input_ids.
        
        Args:
            input_ids: The token IDs of the model output.
            
        Returns:
            True if reasoning section has ended.
        """
    
    def is_reasoning_end_streaming(
        self,
        input_ids: list[int],
        delta_ids: list[int],
    ) -> bool:
        """
        Check if reasoning ends during streaming (decode step).
        
        Args:
            input_ids: The entire model output token IDs.
            delta_ids: The latest tokens from current decode step.
            
        Returns:
            True if reasoning section ends in delta_ids.
        """
        return self.is_reasoning_end(input_ids)
    
    @abstractmethod
    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        """
        Extract content token IDs from the full output.
        
        Args:
            input_ids: The token IDs of the model output.
            
        Returns:
            Token IDs for the content/answer portion.
        """
    
    @abstractmethod
    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        """
        Extract reasoning content from a complete model output.
        
        Args:
            model_output: The complete model-generated string.
            request: Optional request object for context.
            
        Returns:
            ReasoningResult with extracted reasoning and content.
        """
    
    @abstractmethod
    def extract_reasoning_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
        state: StreamingReasoningState | None = None,
    ) -> tuple[ReasoningResult, StreamingReasoningState]:
        """
        Extract reasoning incrementally during streaming.
        
        Args:
            previous_text: Text accumulated before this step.
            current_text: Text accumulated including this step.
            delta_text: New text from this step.
            previous_token_ids: Token IDs before this step.
            current_token_ids: Token IDs including this step.
            delta_token_ids: New token IDs from this step.
            state: Previous streaming state (or None for first call).
            
        Returns:
            Tuple of (incremental result, updated state).
        """


# ============================================================================
# Built-in Parsers
# ============================================================================


class XMLReasoningParser(ReasoningParser):
    """
    Parser for XML-style think blocks.
    
    Extracts reasoning from <think>...</think> or <reasoning>...</reasoning> tags.
    
    Examples:
        <think>Let me analyze this step by step...</think>
        The answer is 42.
    """
    
    name: ClassVar[str] = "xml"
    
    def __init__(
        self,
        tokenizer: Any = None,
        *,
        start_tag: str = "<think>",
        end_tag: str = "</think>",
        **kwargs: Any,
    ) -> None:
        super().__init__(tokenizer, **kwargs)
        self.start_tag = start_tag
        self.end_tag = end_tag
        self._pattern = re.compile(
            rf"{re.escape(start_tag)}(.*?){re.escape(end_tag)}",
            re.DOTALL,
        )
    
    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        if self.model_tokenizer is None:
            return False
        text = self.model_tokenizer.decode(input_ids)
        return self.end_tag in text
    
    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        if self.model_tokenizer is None:
            return input_ids
        
        text = self.model_tokenizer.decode(input_ids)
        content = self._extract_content(text)
        return self.model_tokenizer.encode(content, add_special_tokens=False)
    
    def _extract_content(self, text: str) -> str:
        """Extract content after removing think blocks."""
        # Remove all think blocks
        content = self._pattern.sub("", text)
        return content.strip()
    
    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        # Find all think blocks
        matches = self._pattern.findall(model_output)
        reasoning = "\n".join(matches) if matches else None
        
        # Get content without think blocks
        content = self._extract_content(model_output)
        
        return ReasoningResult(
            reasoning=reasoning,
            content=content if content else None,
        )
    
    def extract_reasoning_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
        state: StreamingReasoningState | None = None,
    ) -> tuple[ReasoningResult, StreamingReasoningState]:
        if state is None:
            state = StreamingReasoningState()
        
        state.accumulated_text = current_text
        state.accumulated_tokens = list(current_token_ids)
        
        # Check for start of reasoning
        if self.start_tag in current_text and not state.in_reasoning:
            state.in_reasoning = True
            # Extract text before start tag as content
            before_tag = current_text.split(self.start_tag)[0]
            state.content_buffer = before_tag
        
        # Check for end of reasoning
        if self.end_tag in current_text and state.in_reasoning:
            state.in_reasoning = False
            state.reasoning_complete = True
            
            # Extract the full reasoning
            match = self._pattern.search(current_text)
            if match:
                state.reasoning_buffer = match.group(1)
            
            # Get content after end tag
            after_tag = current_text.split(self.end_tag)[-1]
            state.content_buffer += after_tag
        elif state.reasoning_complete:
            # After reasoning is complete, accumulate content
            state.content_buffer = self._extract_content(current_text)
        
        return ReasoningResult(
            reasoning=state.reasoning_buffer if state.reasoning_buffer else None,
            content=state.content_buffer if state.content_buffer else None,
            is_complete=state.reasoning_complete and self.end_tag in current_text,
        ), state


class JSONReasoningParser(ReasoningParser):
    """
    Parser for JSON-structured reasoning outputs.
    
    Expects output in format:
    {"reasoning": "...", "answer": "..."}
    """
    
    name: ClassVar[str] = "json"
    
    def __init__(
        self,
        tokenizer: Any = None,
        *,
        reasoning_key: str = "reasoning",
        answer_key: str = "answer",
        **kwargs: Any,
    ) -> None:
        super().__init__(tokenizer, **kwargs)
        self.reasoning_key = reasoning_key
        self.answer_key = answer_key
    
    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        if self.model_tokenizer is None:
            return False
        text = self.model_tokenizer.decode(input_ids)
        # Check for complete JSON
        try:
            import json
            data = json.loads(text)
            return self.answer_key in data
        except json.JSONDecodeError:
            return False
    
    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        if self.model_tokenizer is None:
            return input_ids
        
        text = self.model_tokenizer.decode(input_ids)
        result = self.extract_reasoning(text)
        if result.content:
            return self.model_tokenizer.encode(result.content, add_special_tokens=False)
        return input_ids
    
    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        import json
        
        try:
            data = json.loads(model_output)
            return ReasoningResult(
                reasoning=data.get(self.reasoning_key),
                content=data.get(self.answer_key),
            )
        except json.JSONDecodeError:
            # Try to extract JSON from text
            match = re.search(r'\{[^{}]*\}', model_output, re.DOTALL)
            if match:
                try:
                    data = json.loads(match.group())
                    return ReasoningResult(
                        reasoning=data.get(self.reasoning_key),
                        content=data.get(self.answer_key),
                    )
                except json.JSONDecodeError:
                    pass
            
            return ReasoningResult(content=model_output)
    
    def extract_reasoning_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
        state: StreamingReasoningState | None = None,
    ) -> tuple[ReasoningResult, StreamingReasoningState]:
        if state is None:
            state = StreamingReasoningState()
        
        state.accumulated_text = current_text
        
        # Try to parse as JSON
        result = self.extract_reasoning(current_text)
        if result.reasoning or result.content:
            state.reasoning_buffer = result.reasoning or ""
            state.content_buffer = result.content or ""
            state.reasoning_complete = True
        
        return result, state


class MarkdownReasoningParser(ReasoningParser):
    """
    Parser for Markdown-style think blocks.
    
    Extracts reasoning from ```thinking blocks or > prefixed lines.
    
    Examples:
        ```thinking
        Let me analyze this...
        ```
        The answer is 42.
    """
    
    name: ClassVar[str] = "markdown"
    
    def __init__(
        self,
        tokenizer: Any = None,
        *,
        block_type: str = "thinking",
        **kwargs: Any,
    ) -> None:
        super().__init__(tokenizer, **kwargs)
        self.block_type = block_type
        self._pattern = re.compile(
            rf"```{re.escape(block_type)}\n(.*?)```",
            re.DOTALL,
        )
    
    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        if self.model_tokenizer is None:
            return False
        text = self.model_tokenizer.decode(input_ids)
        # Check for complete thinking block
        return bool(self._pattern.search(text))
    
    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        if self.model_tokenizer is None:
            return input_ids
        
        text = self.model_tokenizer.decode(input_ids)
        content = self._pattern.sub("", text).strip()
        return self.model_tokenizer.encode(content, add_special_tokens=False)
    
    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        matches = self._pattern.findall(model_output)
        reasoning = "\n".join(matches) if matches else None
        content = self._pattern.sub("", model_output).strip()
        
        return ReasoningResult(
            reasoning=reasoning,
            content=content if content else None,
        )
    
    def extract_reasoning_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
        state: StreamingReasoningState | None = None,
    ) -> tuple[ReasoningResult, StreamingReasoningState]:
        if state is None:
            state = StreamingReasoningState()
        
        state.accumulated_text = current_text
        result = self.extract_reasoning(current_text)
        
        if result.reasoning:
            state.reasoning_buffer = result.reasoning
            state.reasoning_complete = True
        if result.content:
            state.content_buffer = result.content
        
        return result, state


class IdentityReasoningParser(ReasoningParser):
    """
    No-op parser that returns the full output as content.
    
    Use when no reasoning extraction is needed.
    """
    
    name: ClassVar[str] = "identity"
    
    def is_reasoning_end(self, input_ids: list[int]) -> bool:
        return True
    
    def extract_content_ids(self, input_ids: list[int]) -> list[int]:
        return input_ids
    
    def extract_reasoning(
        self,
        model_output: str,
        request: Any = None,
    ) -> ReasoningResult:
        return ReasoningResult(content=model_output)
    
    def extract_reasoning_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
        state: StreamingReasoningState | None = None,
    ) -> tuple[ReasoningResult, StreamingReasoningState]:
        if state is None:
            state = StreamingReasoningState()
        
        state.accumulated_text = current_text
        state.content_buffer = current_text
        
        return ReasoningResult(content=delta_text), state


# ============================================================================
# Parser Manager
# ============================================================================


class ReasoningParserManager:
    """
    Central registry for ReasoningParser implementations.
    
    Supports two registration modes:
    - Eager registration via register_module()
    - Lazy registration via register_lazy_module()
    
    Examples:
        >>> ReasoningParserManager.register_module("custom", CustomParser)
        >>> parser_cls = ReasoningParserManager.get_reasoning_parser("custom")
        >>> parser = parser_cls(tokenizer)
    """
    
    reasoning_parsers: ClassVar[dict[str, type[ReasoningParser]]] = {}
    lazy_parsers: ClassVar[dict[str, tuple[str, str]]] = {}  # name -> (module, class)
    
    @classmethod
    def register_module(cls, name: str, parser_class: type[ReasoningParser]) -> None:
        """
        Register a parser class.
        
        Args:
            name: Name to register under.
            parser_class: Parser class to register.
        """
        cls.reasoning_parsers[name] = parser_class
        logger.debug(f"Registered reasoning parser: {name}")
    
    @classmethod
    def register_lazy_module(
        cls,
        name: str,
        module_path: str,
        class_name: str,
    ) -> None:
        """
        Register a parser for lazy loading.
        
        Args:
            name: Name to register under.
            module_path: Module path to import from.
            class_name: Class name within the module.
        """
        cls.lazy_parsers[name] = (module_path, class_name)
        logger.debug(f"Registered lazy reasoning parser: {name} -> {module_path}.{class_name}")
    
    @classmethod
    def get_reasoning_parser(cls, name: str) -> type[ReasoningParser]:
        """
        Retrieve a registered parser class.
        
        If lazily registered, imports and caches on first access.
        
        Args:
            name: Parser name to look up.
            
        Returns:
            The parser class.
            
        Raises:
            KeyError: If parser not found.
        """
        if name in cls.reasoning_parsers:
            return cls.reasoning_parsers[name]
        
        if name in cls.lazy_parsers:
            return cls._load_lazy_parser(name)
        
        available = cls.list_registered()
        raise KeyError(
            f"Reasoning parser '{name}' not found. "
            f"Available parsers: {', '.join(available)}"
        )
    
    @classmethod
    def _load_lazy_parser(cls, name: str) -> type[ReasoningParser]:
        """Import and cache a lazily registered parser."""
        module_path, class_name = cls.lazy_parsers[name]
        
        module = importlib.import_module(module_path)
        parser_class = getattr(module, class_name)
        
        # Cache for future access
        cls.reasoning_parsers[name] = parser_class
        
        logger.debug(f"Loaded lazy reasoning parser: {name}")
        return parser_class
    
    @classmethod
    def list_registered(cls) -> list[str]:
        """Get names of all registered parsers."""
        return sorted(
            set(cls.reasoning_parsers.keys()) | set(cls.lazy_parsers.keys())
        )
    
    @classmethod
    def create_parser(
        cls,
        name: str,
        tokenizer: Any = None,
        **kwargs: Any,
    ) -> ReasoningParser:
        """
        Create a parser instance.
        
        Args:
            name: Parser name.
            tokenizer: Tokenizer for token-level operations.
            **kwargs: Additional parser configuration.
            
        Returns:
            Parser instance.
        """
        parser_cls = cls.get_reasoning_parser(name)
        return parser_cls(tokenizer, **kwargs)


# ============================================================================
# Decorator
# ============================================================================


def reasoning_parser(name: str) -> Callable[[type[ReasoningParser]], type[ReasoningParser]]:
    """
    Decorator to register a reasoning parser.
    
    Examples:
        >>> @reasoning_parser("deepseek")
        ... class DeepSeekReasoningParser(ReasoningParser):
        ...     ...
    """
    def decorator(cls: type[ReasoningParser]) -> type[ReasoningParser]:
        ReasoningParserManager.register_module(name, cls)
        return cls
    return decorator


# ============================================================================
# Register Built-in Parsers
# ============================================================================


# Register built-in parsers
ReasoningParserManager.register_module("xml", XMLReasoningParser)
ReasoningParserManager.register_module("json", JSONReasoningParser)
ReasoningParserManager.register_module("markdown", MarkdownReasoningParser)
ReasoningParserManager.register_module("identity", IdentityReasoningParser)

# Aliases
ReasoningParserManager.register_module("think", XMLReasoningParser)
ReasoningParserManager.register_module("none", IdentityReasoningParser)


# ============================================================================
# Convenience Functions
# ============================================================================


def extract_reasoning(
    model_output: str,
    parser_name: str = "xml",
    tokenizer: Any = None,
    **kwargs: Any,
) -> ReasoningResult:
    """
    Convenience function to extract reasoning from model output.
    
    Args:
        model_output: The complete model output.
        parser_name: Name of the parser to use.
        tokenizer: Optional tokenizer for token-level operations.
        **kwargs: Additional parser configuration.
        
    Returns:
        ReasoningResult with extracted reasoning and content.
    """
    parser = ReasoningParserManager.create_parser(parser_name, tokenizer, **kwargs)
    return parser.extract_reasoning(model_output)


def create_streaming_parser(
    parser_name: str = "xml",
    tokenizer: Any = None,
    **kwargs: Any,
) -> tuple[ReasoningParser, StreamingReasoningState]:
    """
    Create a parser and state for streaming extraction.
    
    Args:
        parser_name: Name of the parser to use.
        tokenizer: Optional tokenizer.
        **kwargs: Additional parser configuration.
        
    Returns:
        Tuple of (parser, initial state).
    """
    parser = ReasoningParserManager.create_parser(parser_name, tokenizer, **kwargs)
    state = StreamingReasoningState()
    return parser, state


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Data classes
    "ReasoningResult",
    "StreamingReasoningState",
    # Abstract base
    "ReasoningParser",
    # Built-in parsers
    "XMLReasoningParser",
    "JSONReasoningParser",
    "MarkdownReasoningParser",
    "IdentityReasoningParser",
    # Manager
    "ReasoningParserManager",
    # Decorator
    "reasoning_parser",
    # Convenience functions
    "extract_reasoning",
    "create_streaming_parser",
]
