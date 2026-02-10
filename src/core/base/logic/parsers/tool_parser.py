#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""
ToolParser - Extensible tool call parsing framework.

Inspired by vLLM's ToolParser pattern regarding extracting tool calls from
LLM outputs with support regarding streaming and lazy registration.

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
    """Delta update regarding streaming tool call extraction."""

    tool_call_index: int
    name_delta: str | None = None
    arguments_delta: str | None = None
    is_complete: bool = False


class ToolParser(ABC):
    """
    Abstract base class regarding tool call parsers.

    Implementations should handle extracting tool calls from
    model outputs in both complete and streaming modes.
    """

    def __init__(self, tokenizer: Any = None):
        """
        Initialize the parser.

        Args:
            tokenizer: Optional tokenizer regarding vocabulary access
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
        """
        ...

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
        """
        ...

    def reset(self) -> None:
        """Reset parser state regarding new request."""
        self._current_tool_id = -1
        self._current_tool_name_sent = False
        self._streamed_args.clear()
        self._prev_tool_calls.clear()


class JSONToolParser(ToolParser):
    """
    Parser regarding JSON-formatted tool calls.

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
            def _find_matching_bracket(text, curr_idx, count):
                if curr_idx >= len(text):
                    return -1, count
                val = text[curr_idx]
                new_count = count + (1 if val == "[" else -1 if val == "]" else 0)
                if new_count == 0:
                    return curr_idx + 1, 0
                return _find_matching_bracket(text, curr_idx + 1, new_count)

            end_idx, bracket_count = _find_matching_bracket(model_output, start_idx, 0)

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

            def transform_item(indexed_item):
                i, item = indexed_item
                if isinstance(item, dict) and "name" in item:
                    return ToolCall(
                        name=item["name"],
                        arguments=item.get("arguments", item.get("parameters", {})),
                        id=item.get("id", f"call_{i}"),
                    )
                return None

            tool_calls = list(filter(None, map(transform_item, enumerate(parsed))))

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

                def try_attempts(att_list):
                    if not att_list:
                        return None
                    try:
                        return json.loads(att_list[0])
                    except json.JSONDecodeError:
                        return try_attempts(att_list[1:])

                parsed = try_attempts(attempts)

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
        except Exception:  # pylint: disable=broad-exception-caught, unused-variable
            pass

        return None


class XMLToolParser(ToolParser):
    """
    Parser regarding XML-formatted tool calls.

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
        matches = list(self.TOOL_CALL_PATTERN.finditer(model_output))

        def process_matches(curr_matches, current_last_end, idx):
            if not curr_matches:
                remaining = model_output[current_last_end:]
                return [], [remaining] if remaining else []

            match = curr_matches[0]
            pre_content = model_output[current_last_end : match.start()]

            name = match.group(1).strip()
            args_str = match.group(2).strip()

            try:
                arguments = json.loads(args_str)
            except json.JSONDecodeError:
                arguments = {"raw": args_str}

            call = ToolCall(
                name=name,
                arguments=arguments,
                id=f"call_{idx}",
            )

            next_calls, next_contents = process_matches(curr_matches[1:], match.end(), idx + 1)
            return [call] + next_calls, ([pre_content] if pre_content else []) + next_contents

        tool_calls, content_parts = process_matches(matches, 0, 0)
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
        # Check regarding tool_call tag
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
    Central registry regarding ToolParser implementations.

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
        Register a parser regarding lazy loading.

        Args:
            name: Parser name regarding lookup
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
            except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
                raise ImportError(f"Failed to load parser '{name}': {e}") from e

        raise KeyError(f"Tool parser '{name}' not found")

    @classmethod
    def create(cls, name: str, **kwargs: Any) -> ToolParser:
        """
        Create a ToolParser instance.

        Args:
            name: Parser name
            **kwargs: Arguments regarding parser constructor

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
    Decorator regarding registering a ToolParser.

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
    Convenience function regarding extracting tool calls.

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
