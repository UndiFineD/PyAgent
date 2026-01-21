"""
ToolParser - Extensible tool call parsing framework.

Inspired by vLLM's ToolParser pattern for extracting tool calls from
LLM outputs with support for streaming and lazy registration.

Phase 24: Advanced Observability & Parsing
"""

from __future__ import annotations

import importlib
import json
import re
from abc import ABC, abstractmethod
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, TypeVar

T = TypeVar("T", bound="ToolParser")


@dataclass
class ToolCall:
    """Represents a single tool/function call."""
    name: str
    arguments: dict[str, Any]
    id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary format."""
        result = {
            "name": self.name,
            "arguments": self.arguments,
        }
        if self.id is not None:
            result["id"] = self.id
        return result


@dataclass
class ExtractedToolCalls:
    """Result of tool call extraction."""
    tool_calls: list[ToolCall] = field(default_factory=list)
    content: str | None = None
    is_complete: bool = True
    error: str | None = None

    @property
    def has_tool_calls(self) -> bool:
        """Check if any tool calls were extracted."""
        return bool(self.tool_calls)


@dataclass
class StreamingToolCallDelta:
    """Delta update for streaming tool call extraction."""
    tool_call_index: int
    name_delta: str | None = None
    arguments_delta: str | None = None
    is_complete: bool = False


class ToolParser(ABC):
    """
    Abstract base class for tool call parsers.

    Implementations should handle extracting tool calls from
    model outputs in both complete and streaming modes.
    """

    def __init__(self, tokenizer: Any = None):
        """
        Initialize the parser.

        Args:
            tokenizer: Optional tokenizer for vocabulary access
        """
        self._tokenizer = tokenizer
        self._current_tool_id = -1
        self._current_tool_name_sent = False
        self._streamed_args: list[str] = []
        self._prev_tool_calls: list[dict[str, Any]] = []

    @cached_property
    def vocab(self) -> dict[str, int]:
        """Get tokenizer vocabulary if available."""
        if self._tokenizer is None:
            return {}
        return getattr(self._tokenizer, "get_vocab", lambda: {})()

    @abstractmethod
    def extract_tool_calls(
        self,
        model_output: str,
        tools: list[dict[str, Any]] | None = None,
    ) -> ExtractedToolCalls:
        """
        Extract tool calls from a complete model output.

        Args:
            model_output: The complete model-generated string
            tools: Optional list of available tool definitions

        Returns:
            ExtractedToolCalls with parsed tool calls
        """
        pass

    @abstractmethod
    def extract_tool_calls_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
    ) -> StreamingToolCallDelta | None:
        """
        Extract tool calls from streaming output.

        Args:
            previous_text: Text from previous iteration
            current_text: Current accumulated text
            delta_text: New text since last iteration
            previous_token_ids: Token IDs from previous iteration
            current_token_ids: Current token IDs
            delta_token_ids: New token IDs

        Returns:
            StreamingToolCallDelta or None if no update
        """
        pass

    def reset(self) -> None:
        """Reset parser state for new request."""
        self._current_tool_id = -1
        self._current_tool_name_sent = False
        self._streamed_args.clear()
        self._prev_tool_calls.clear()


class JSONToolParser(ToolParser):
    """
    Parser for JSON-formatted tool calls.

    Handles outputs like:
    [{"name": "function_name", "arguments": {"arg1": "value1"}}]
    """

    def __init__(
        self,
        tokenizer: Any = None,
        tool_call_start: str = "[",
        tool_call_end: str = "]",
    ):
        super().__init__(tokenizer)
        self.tool_call_start = tool_call_start
        self.tool_call_end = tool_call_end

    def extract_tool_calls(
        self,
        model_output: str,
        tools: list[dict[str, Any]] | None = None,
    ) -> ExtractedToolCalls:
        """Extract JSON-formatted tool calls."""
        try:
            # Find JSON array in output
            start_idx = model_output.find(self.tool_call_start)
            if start_idx == -1:
                return ExtractedToolCalls(content=model_output)

            # Try to find matching end bracket
            bracket_count = 0
            end_idx = start_idx
            for i, char in enumerate(model_output[start_idx:], start=start_idx):
                if char == "[":
                    bracket_count += 1
                elif char == "]":
                    bracket_count -= 1
                    if bracket_count == 0:
                        end_idx = i + 1
                        break

            if bracket_count != 0:
                return ExtractedToolCalls(
                    content=model_output,
                    is_complete=False,
                    error="Incomplete JSON array",
                )

            json_str = model_output[start_idx:end_idx]
            parsed = json.loads(json_str)

            if not isinstance(parsed, list):
                parsed = [parsed]

            tool_calls = []
            for i, item in enumerate(parsed):
                if isinstance(item, dict) and "name" in item:
                    tool_calls.append(ToolCall(
                        name=item["name"],
                        arguments=item.get("arguments", item.get("parameters", {})),
                        id=item.get("id", f"call_{i}"),
                    ))

            content = model_output[:start_idx].strip() or None

            return ExtractedToolCalls(
                tool_calls=tool_calls,
                content=content,
            )

        except json.JSONDecodeError as e:
            return ExtractedToolCalls(
                content=model_output,
                is_complete=False,
                error=f"JSON decode error: {e}",
            )

    def extract_tool_calls_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
    ) -> StreamingToolCallDelta | None:
        """Extract tool calls from streaming JSON output."""
        # Check if we're in a tool call
        if self.tool_call_start not in current_text:
            return None

        # Try partial parsing
        try:
            start_idx = current_text.find(self.tool_call_start)
            json_partial = current_text[start_idx:]

            # Use partial JSON parsing if available
            try:
                import partial_json_parser
                parsed = partial_json_parser.loads(json_partial)
            except ImportError:
                # Fallback: try adding closing brackets
                attempts = [
                    json_partial,
                    json_partial + "}]",
                    json_partial + "]",
                    json_partial + "}}]",
                ]
                parsed = None
                for attempt in attempts:
                    try:
                        parsed = json.loads(attempt)
                        break
                    except json.JSONDecodeError:
                        continue

                if parsed is None:
                    return None

            if isinstance(parsed, list) and parsed:
                current_call = parsed[-1]
                if isinstance(current_call, dict):
                    return StreamingToolCallDelta(
                        tool_call_index=len(parsed) - 1,
                        name_delta=current_call.get("name"),
                        arguments_delta=json.dumps(current_call.get("arguments", {})),
                        is_complete=self.tool_call_end in current_text,
                    )
        except Exception:
            pass

        return None


class XMLToolParser(ToolParser):
    """
    Parser for XML-formatted tool calls.

    Handles outputs like:
    <tool_call>
        <name>function_name</name>
        <arguments>{"arg1": "value1"}</arguments>
    </tool_call>
    """

    TOOL_CALL_PATTERN = re.compile(
        r"<tool_call>\s*<name>(.*?)</name>\s*<arguments>(.*?)</arguments>\s*</tool_call>",
        re.DOTALL,
    )

    def extract_tool_calls(
        self,
        model_output: str,
        tools: list[dict[str, Any]] | None = None,
    ) -> ExtractedToolCalls:
        """Extract XML-formatted tool calls."""
        tool_calls = []
        content_parts = []
        last_end = 0

        for i, match in enumerate(self.TOOL_CALL_PATTERN.finditer(model_output)):
            # Capture content before this tool call
            if match.start() > last_end:
                content_parts.append(model_output[last_end:match.start()])

            name = match.group(1).strip()
            args_str = match.group(2).strip()

            try:
                arguments = json.loads(args_str)
            except json.JSONDecodeError:
                arguments = {"raw": args_str}

            tool_calls.append(ToolCall(
                name=name,
                arguments=arguments,
                id=f"call_{i}",
            ))

            last_end = match.end()

        # Capture remaining content
        if last_end < len(model_output):
            content_parts.append(model_output[last_end:])

        content = "".join(content_parts).strip() or None

        return ExtractedToolCalls(
            tool_calls=tool_calls,
            content=content,
        )

    def extract_tool_calls_streaming(
        self,
        previous_text: str,
        current_text: str,
        delta_text: str,
        previous_token_ids: Sequence[int],
        current_token_ids: Sequence[int],
        delta_token_ids: Sequence[int],
    ) -> StreamingToolCallDelta | None:
        """Extract tool calls from streaming XML output."""
        # Check for tool_call tag
        if "<tool_call>" not in current_text:
            return None

        # Find incomplete tool calls
        open_count = current_text.count("<tool_call>")
        close_count = current_text.count("</tool_call>")

        if open_count > close_count:
            # We're inside an incomplete tool call
            # Extract partial name/arguments
            name_match = re.search(r"<name>(.*?)(?:</name>|$)", current_text, re.DOTALL)
            args_match = re.search(r"<arguments>(.*?)(?:</arguments>|$)", current_text, re.DOTALL)

            return StreamingToolCallDelta(
                tool_call_index=open_count - 1,
                name_delta=name_match.group(1).strip() if name_match else None,
                arguments_delta=args_match.group(1).strip() if args_match else None,
                is_complete=False,
            )

        return None


class ToolParserManager:
    """
    Central registry for ToolParser implementations.

    Supports both eager and lazy registration.
    """

    _parsers: dict[str, type[ToolParser]] = {}
    _lazy_parsers: dict[str, tuple[str, str]] = {}  # name -> (module, class_name)

    @classmethod
    def register(
        cls,
        name: str,
        parser_cls: type[ToolParser] | None = None,
    ) -> Callable[[type[ToolParser]], type[ToolParser]] | None:
        """
        Register a ToolParser class.

        Can be used as decorator or direct call:
            @ToolParserManager.register("my_parser")
            class MyParser(ToolParser): ...

            ToolParserManager.register("my_parser", MyParser)
        """
        def decorator(parser: type[ToolParser]) -> type[ToolParser]:
            if not issubclass(parser, ToolParser):
                raise TypeError(f"Must be subclass of ToolParser, got {type(parser)}")
            cls._parsers[name] = parser
            return parser

        if parser_cls is not None:
            return decorator(parser_cls)
        return decorator

    @classmethod
    def register_lazy(cls, name: str, module: str, class_name: str) -> None:
        """
        Register a parser for lazy loading.

        Args:
            name: Parser name for lookup
            module: Module path (e.g., "mypackage.parsers")
            class_name: Class name within module
        """
        cls._lazy_parsers[name] = (module, class_name)

    @classmethod
    def get(cls, name: str) -> type[ToolParser]:
        """
        Get a registered ToolParser class.

        Args:
            name: Parser name

        Returns:
            ToolParser class

        Raises:
            KeyError: If parser not found
        """
        # Check eager registrations first
        if name in cls._parsers:
            return cls._parsers[name]

        # Try lazy loading
        if name in cls._lazy_parsers:
            module_path, class_name = cls._lazy_parsers[name]
            try:
                mod = importlib.import_module(module_path)
                parser_cls = getattr(mod, class_name)
                if not issubclass(parser_cls, ToolParser):
                    raise TypeError(f"{class_name} is not a ToolParser subclass")
                cls._parsers[name] = parser_cls  # Cache it
                return parser_cls
            except Exception as e:
                raise ImportError(f"Failed to load parser '{name}': {e}") from e

        raise KeyError(f"Tool parser '{name}' not found")

    @classmethod
    def create(cls, name: str, **kwargs: Any) -> ToolParser:
        """
        Create a ToolParser instance.

        Args:
            name: Parser name
            **kwargs: Arguments for parser constructor

        Returns:
            ToolParser instance
        """
        parser_cls = cls.get(name)
        return parser_cls(**kwargs)

    @classmethod
    def list_parsers(cls) -> list[str]:
        """List all registered parser names."""
        return list(set(cls._parsers.keys()) | set(cls._lazy_parsers.keys()))


# Register built-in parsers
ToolParserManager.register("json", JSONToolParser)
ToolParserManager.register("xml", XMLToolParser)


def tool_parser(name: str) -> Callable[[type[T]], type[T]]:
    """
    Decorator for registering a ToolParser.

    Usage:
        @tool_parser("my_parser")
        class MyParser(ToolParser): ...
    """
    def decorator(cls: type[T]) -> type[T]:
        ToolParserManager.register(name, cls)  # type: ignore
        return cls
    return decorator


def extract_tool_calls(
    model_output: str,
    parser_name: str = "json",
    tools: list[dict[str, Any]] | None = None,
    **parser_kwargs: Any,
) -> ExtractedToolCalls:
    """
    Convenience function for extracting tool calls.

    Args:
        model_output: Model-generated text
        parser_name: Name of parser to use
        tools: Optional tool definitions
        **parser_kwargs: Additional parser arguments

    Returns:
        ExtractedToolCalls result
    """
    parser = ToolParserManager.create(parser_name, **parser_kwargs)
    return parser.extract_tool_calls(model_output, tools)
