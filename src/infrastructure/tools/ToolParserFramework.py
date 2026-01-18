# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Tool Parser Framework - Model-Specific Parsing

"""
Tool/function call parsing with model-specific parsers.

Inspired by vLLM's tool_parsers patterns, this module provides:
- Model-specific tool call parsing (Hermes, Llama3, Mistral, etc.)
- Streaming tool call extraction
- JSON schema validation
- Multi-tool support

Beyond vLLM:
- Unified parser registry
- Streaming partial JSON parsing
- Auto-detection of tool format
- Tool call validation
"""

from __future__ import annotations

import json
import re
import threading
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Pattern,
    Set,
    Tuple,
    Type,
    Union,
)


# =============================================================================
# Enums
# =============================================================================

class ToolParserType(Enum):
    """Supported tool parser types."""
    GENERIC_JSON = auto()      # Generic JSON parsing
    HERMES = auto()            # Hermes/NousResearch format
    LLAMA3 = auto()            # Llama 3 function calling
    MISTRAL = auto()           # Mistral AI format
    GRANITE = auto()           # IBM Granite format
    QWEN = auto()              # Qwen format
    JAMBA = auto()             # AI21 Jamba format
    DEEPSEEKV3 = auto()        # DeepSeek V3 format
    INTERNLM = auto()          # InternLM format
    PYTHONIC = auto()          # Python-style function calls


class ToolCallStatus(Enum):
    """Tool call parsing status."""
    PENDING = auto()           # Still parsing
    COMPLETE = auto()          # Successfully parsed
    INVALID = auto()           # Parse error
    PARTIAL = auto()           # Partial/streaming


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ToolParameter:
    """Tool parameter definition."""
    name: str
    param_type: str = "string"
    description: str = ""
    required: bool = True
    default: Optional[Any] = None
    enum: Optional[List[str]] = None


@dataclass
class ToolCall:
    """Parsed tool/function call."""
    id: str                                 # Unique call ID
    name: str                               # Function/tool name
    arguments: Dict[str, Any]               # Parsed arguments
    raw_arguments: str = ""                 # Original JSON string
    status: ToolCallStatus = ToolCallStatus.COMPLETE
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": "function",
            "function": {
                "name": self.name,
                "arguments": self.raw_arguments or json.dumps(self.arguments),
            },
        }
    
    def to_openai_format(self) -> Dict[str, Any]:
        """Convert to OpenAI API format."""
        return {
            "id": self.id,
            "type": "function",
            "function": {
                "name": self.name,
                "arguments": self.raw_arguments or json.dumps(self.arguments),
            },
        }


@dataclass
class ToolParseResult:
    """Result of tool call parsing."""
    tool_calls: List[ToolCall] = field(default_factory=list)
    content: str = ""                       # Non-tool content
    raw_output: str = ""                    # Full raw output
    complete: bool = True
    errors: List[str] = field(default_factory=list)
    
    @property
    def has_tool_calls(self) -> bool:
        return len(self.tool_calls) > 0
    
    @property
    def is_valid(self) -> bool:
        return all(tc.status == ToolCallStatus.COMPLETE for tc in self.tool_calls)


@dataclass
class StreamingToolState:
    """State for streaming tool parsing."""
    buffer: str = ""
    in_tool_call: bool = False
    current_tool: Optional[ToolCall] = None
    completed_tools: List[ToolCall] = field(default_factory=list)
    tool_call_index: int = 0
    brace_depth: int = 0
    in_string: bool = False


# =============================================================================
# Base Tool Parser
# =============================================================================

class ToolParser(ABC):
    """Base class for tool parsers."""
    
    @property
    @abstractmethod
    def parser_type(self) -> ToolParserType:
        """Return parser type."""
        ...
    
    @abstractmethod
    def parse(self, text: str) -> ToolParseResult:
        """
        Parse tool calls from text.
        
        Args:
            text: Model output text
        
        Returns:
            ToolParseResult with extracted tool calls
        """
        ...
    
    @abstractmethod
    def parse_streaming(
        self,
        delta: str,
        state: StreamingToolState,
    ) -> Tuple[StreamingToolState, Optional[ToolCall]]:
        """
        Parse streaming token.
        
        Args:
            delta: New token(s)
            state: Current parsing state
        
        Returns:
            (updated_state, completed_tool_call_if_any)
        """
        ...
    
    def _generate_call_id(self, index: int = 0) -> str:
        """Generate a unique call ID."""
        import uuid
        return f"call_{uuid.uuid4().hex[:24]}"


# =============================================================================
# Generic JSON Tool Parser
# =============================================================================

class JsonToolParser(ToolParser):
    """
    Generic JSON tool call parser.
    
    Expects format:
    {"name": "function_name", "arguments": {...}}
    or
    {"function": {"name": "...", "arguments": {...}}}
    """
    
    @property
    def parser_type(self) -> ToolParserType:
        return ToolParserType.GENERIC_JSON
    
    def parse(self, text: str) -> ToolParseResult:
        result = ToolParseResult(raw_output=text)
        
        # Try to find JSON objects
        json_matches = extract_json_from_text(text)
        
        for i, json_str in enumerate(json_matches):
            try:
                data = json.loads(json_str)
                tool_call = self._parse_json_object(data, i)
                if tool_call:
                    result.tool_calls.append(tool_call)
            except json.JSONDecodeError as e:
                result.errors.append(f"JSON parse error: {e}")
        
        # Extract non-tool content
        result.content = self._extract_content(text, json_matches)
        
        return result
    
    def _parse_json_object(
        self,
        data: Dict[str, Any],
        index: int,
    ) -> Optional[ToolCall]:
        """Parse a JSON object as a tool call."""
        # OpenAI format
        if "function" in data and isinstance(data["function"], dict):
            func = data["function"]
            name = func.get("name", "")
            args_raw = func.get("arguments", "{}")
            
            if isinstance(args_raw, str):
                try:
                    args = json.loads(args_raw)
                except json.JSONDecodeError:
                    args = {}
            else:
                args = args_raw
            
            return ToolCall(
                id=data.get("id", self._generate_call_id(index)),
                name=name,
                arguments=args,
                raw_arguments=args_raw if isinstance(args_raw, str) else json.dumps(args_raw),
            )
        
        # Direct format
        if "name" in data:
            name = data["name"]
            args = data.get("arguments", data.get("parameters", {}))
            
            return ToolCall(
                id=data.get("id", self._generate_call_id(index)),
                name=name,
                arguments=args if isinstance(args, dict) else {},
                raw_arguments=json.dumps(args),
            )
        
        return None
    
    def _extract_content(
        self,
        text: str,
        json_matches: List[str],
    ) -> str:
        """Extract non-JSON content."""
        content = text
        for match in json_matches:
            content = content.replace(match, "", 1)
        return content.strip()
    
    def parse_streaming(
        self,
        delta: str,
        state: StreamingToolState,
    ) -> Tuple[StreamingToolState, Optional[ToolCall]]:
        state.buffer += delta
        completed_tool = None
        
        # Track brace depth
        for char in delta:
            if char == '"' and (len(state.buffer) < 2 or state.buffer[-2] != '\\'):
                state.in_string = not state.in_string
            elif not state.in_string:
                if char == '{':
                    if state.brace_depth == 0:
                        state.in_tool_call = True
                    state.brace_depth += 1
                elif char == '}':
                    state.brace_depth -= 1
                    if state.brace_depth == 0 and state.in_tool_call:
                        # Complete JSON object
                        try:
                            json_match = self._extract_last_json(state.buffer)
                            if json_match:
                                data = json.loads(json_match)
                                tool_call = self._parse_json_object(
                                    data, state.tool_call_index
                                )
                                if tool_call:
                                    completed_tool = tool_call
                                    state.completed_tools.append(tool_call)
                                    state.tool_call_index += 1
                        except json.JSONDecodeError:
                            pass
                        state.in_tool_call = False
        
        return state, completed_tool
    
    def _extract_last_json(self, text: str) -> Optional[str]:
        """Extract the last complete JSON object."""
        brace_depth = 0
        start = -1
        in_string = False
        
        for i in range(len(text) - 1, -1, -1):
            char = text[i]
            
            if char == '"' and (i == 0 or text[i-1] != '\\'):
                in_string = not in_string
            elif not in_string:
                if char == '}':
                    if brace_depth == 0:
                        start = i
                    brace_depth += 1
                elif char == '{':
                    brace_depth -= 1
                    if brace_depth == 0:
                        return text[i:start+1]
        
        return None


# =============================================================================
# Hermes Tool Parser
# =============================================================================

class HermesToolParser(ToolParser):
    """
    Hermes/NousResearch tool call parser.
    
    Format:
    <tool_call>
    {"name": "...", "arguments": {...}}
    </tool_call>
    """
    
    TOOL_CALL_OPEN = "<tool_call>"
    TOOL_CALL_CLOSE = "</tool_call>"
    
    @property
    def parser_type(self) -> ToolParserType:
        return ToolParserType.HERMES
    
    def parse(self, text: str) -> ToolParseResult:
        result = ToolParseResult(raw_output=text)
        
        # Find all tool_call blocks
        pattern = re.compile(
            rf"{re.escape(self.TOOL_CALL_OPEN)}\s*(.*?)\s*{re.escape(self.TOOL_CALL_CLOSE)}",
            re.DOTALL
        )
        
        matches = pattern.findall(text)
        content = text
        
        for i, match in enumerate(matches):
            try:
                data = json.loads(match.strip())
                name = data.get("name", "")
                args = data.get("arguments", {})
                
                tool_call = ToolCall(
                    id=self._generate_call_id(i),
                    name=name,
                    arguments=args,
                    raw_arguments=json.dumps(args),
                )
                result.tool_calls.append(tool_call)
            except json.JSONDecodeError as e:
                result.errors.append(f"JSON parse error in tool_call: {e}")
        
        # Remove tool_call blocks from content
        result.content = pattern.sub("", text).strip()
        
        return result
    
    def parse_streaming(
        self,
        delta: str,
        state: StreamingToolState,
    ) -> Tuple[StreamingToolState, Optional[ToolCall]]:
        state.buffer += delta
        completed_tool = None
        
        # Check for tool_call open tag
        if self.TOOL_CALL_OPEN in state.buffer and not state.in_tool_call:
            state.in_tool_call = True
        
        # Check for tool_call close tag
        if state.in_tool_call and self.TOOL_CALL_CLOSE in state.buffer:
            # Extract the tool call
            pattern = re.compile(
                rf"{re.escape(self.TOOL_CALL_OPEN)}\s*(.*?)\s*{re.escape(self.TOOL_CALL_CLOSE)}",
                re.DOTALL
            )
            match = pattern.search(state.buffer)
            
            if match:
                try:
                    data = json.loads(match.group(1).strip())
                    name = data.get("name", "")
                    args = data.get("arguments", {})
                    
                    completed_tool = ToolCall(
                        id=self._generate_call_id(state.tool_call_index),
                        name=name,
                        arguments=args,
                        raw_arguments=json.dumps(args),
                    )
                    state.completed_tools.append(completed_tool)
                    state.tool_call_index += 1
                except json.JSONDecodeError:
                    pass
                
                # Remove processed tool call from buffer
                state.buffer = pattern.sub("", state.buffer, count=1)
            
            state.in_tool_call = False
        
        return state, completed_tool


# =============================================================================
# Llama 3 Tool Parser
# =============================================================================

class Llama3ToolParser(ToolParser):
    """
    Llama 3 tool call parser.
    
    Format:
    <|python_tag|>function_name(arg1=value1, arg2=value2)
    or
    {"name": "...", "parameters": {...}}
    """
    
    PYTHON_TAG = "<|python_tag|>"
    
    @property
    def parser_type(self) -> ToolParserType:
        return ToolParserType.LLAMA3
    
    def parse(self, text: str) -> ToolParseResult:
        result = ToolParseResult(raw_output=text)
        
        # Check for python_tag format
        if self.PYTHON_TAG in text:
            parts = text.split(self.PYTHON_TAG)
            result.content = parts[0].strip()
            
            for i, part in enumerate(parts[1:]):
                tool_call = self._parse_pythonic_call(part.strip(), i)
                if tool_call:
                    result.tool_calls.append(tool_call)
        else:
            # Try JSON format
            json_parser = JsonToolParser()
            return json_parser.parse(text)
        
        return result
    
    def _parse_pythonic_call(
        self,
        text: str,
        index: int,
    ) -> Optional[ToolCall]:
        """Parse Python-style function call."""
        # Match function_name(args)
        pattern = re.compile(r'^(\w+)\((.*)\)$', re.DOTALL)
        match = pattern.match(text.strip())
        
        if not match:
            return None
        
        name = match.group(1)
        args_str = match.group(2).strip()
        
        # Parse arguments
        args = self._parse_kwargs(args_str)
        
        return ToolCall(
            id=self._generate_call_id(index),
            name=name,
            arguments=args,
            raw_arguments=json.dumps(args),
        )
    
    def _parse_kwargs(self, args_str: str) -> Dict[str, Any]:
        """Parse keyword arguments."""
        args = {}
        
        if not args_str:
            return args
        
        # Simple parsing - handle key=value pairs
        # This is a simplified version; production would need proper parsing
        try:
            # Try to evaluate as Python dict
            # Safe alternative: parse manually
            parts = self._split_args(args_str)
            
            for part in parts:
                if '=' in part:
                    key, value = part.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Parse value
                    args[key] = self._parse_value(value)
        except Exception:
            pass
        
        return args
    
    def _split_args(self, args_str: str) -> List[str]:
        """Split arguments respecting quotes and brackets."""
        parts = []
        current = ""
        depth = 0
        in_string = False
        string_char = None
        
        for char in args_str:
            if char in '"\'':
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
            elif not in_string:
                if char in '([{':
                    depth += 1
                elif char in ')]}':
                    depth -= 1
                elif char == ',' and depth == 0:
                    parts.append(current.strip())
                    current = ""
                    continue
            
            current += char
        
        if current.strip():
            parts.append(current.strip())
        
        return parts
    
    def _parse_value(self, value: str) -> Any:
        """Parse a value string."""
        # Try JSON
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass
        
        # Try Python literals
        if value.lower() == 'true':
            return True
        if value.lower() == 'false':
            return False
        if value.lower() == 'none':
            return None
        
        # Try number
        try:
            if '.' in value:
                return float(value)
            return int(value)
        except ValueError:
            pass
        
        # Return as string (strip quotes)
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        
        return value
    
    def parse_streaming(
        self,
        delta: str,
        state: StreamingToolState,
    ) -> Tuple[StreamingToolState, Optional[ToolCall]]:
        state.buffer += delta
        completed_tool = None
        
        # Check for python_tag
        if self.PYTHON_TAG in state.buffer:
            idx = state.buffer.index(self.PYTHON_TAG)
            after_tag = state.buffer[idx + len(self.PYTHON_TAG):]
            
            # Check if we have a complete call (closing paren at depth 0)
            depth = 0
            in_string = False
            string_char = None
            
            for i, char in enumerate(after_tag):
                if char in '"\'':
                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False
                elif not in_string:
                    if char == '(':
                        depth += 1
                    elif char == ')':
                        depth -= 1
                        if depth == 0:
                            # Complete call
                            call_text = after_tag[:i+1]
                            tool_call = self._parse_pythonic_call(
                                call_text, state.tool_call_index
                            )
                            if tool_call:
                                completed_tool = tool_call
                                state.completed_tools.append(tool_call)
                                state.tool_call_index += 1
                            
                            # Clear processed part
                            state.buffer = after_tag[i+1:]
                            break
        
        return state, completed_tool


# =============================================================================
# Mistral Tool Parser
# =============================================================================

class MistralToolParser(ToolParser):
    """
    Mistral AI tool call parser.
    
    Format:
    [TOOL_CALLS] [{"name": "...", "arguments": {...}}]
    """
    
    TOOL_CALLS_TAG = "[TOOL_CALLS]"
    
    @property
    def parser_type(self) -> ToolParserType:
        return ToolParserType.MISTRAL
    
    def parse(self, text: str) -> ToolParseResult:
        result = ToolParseResult(raw_output=text)
        
        if self.TOOL_CALLS_TAG not in text:
            # No tool calls
            result.content = text
            return result
        
        parts = text.split(self.TOOL_CALLS_TAG, 1)
        result.content = parts[0].strip()
        
        if len(parts) > 1:
            tool_json = parts[1].strip()
            
            try:
                # Parse as JSON array
                tool_list = json.loads(tool_json)
                
                if isinstance(tool_list, list):
                    for i, tool_data in enumerate(tool_list):
                        name = tool_data.get("name", "")
                        args = tool_data.get("arguments", {})
                        
                        tool_call = ToolCall(
                            id=tool_data.get("id", self._generate_call_id(i)),
                            name=name,
                            arguments=args,
                            raw_arguments=json.dumps(args),
                        )
                        result.tool_calls.append(tool_call)
            except json.JSONDecodeError as e:
                result.errors.append(f"JSON parse error: {e}")
        
        return result
    
    def parse_streaming(
        self,
        delta: str,
        state: StreamingToolState,
    ) -> Tuple[StreamingToolState, Optional[ToolCall]]:
        state.buffer += delta
        completed_tool = None
        
        if self.TOOL_CALLS_TAG in state.buffer and not state.in_tool_call:
            state.in_tool_call = True
            state.brace_depth = 0
        
        if state.in_tool_call:
            # Track array completion
            for char in delta:
                if char == '[':
                    state.brace_depth += 1
                elif char == ']':
                    state.brace_depth -= 1
                    
                    if state.brace_depth == 0:
                        # Complete array
                        idx = state.buffer.index(self.TOOL_CALLS_TAG)
                        tool_json = state.buffer[idx + len(self.TOOL_CALLS_TAG):].strip()
                        
                        try:
                            tool_list = json.loads(tool_json)
                            if isinstance(tool_list, list):
                                for i, tool_data in enumerate(tool_list):
                                    name = tool_data.get("name", "")
                                    args = tool_data.get("arguments", {})
                                    
                                    tool_call = ToolCall(
                                        id=tool_data.get("id", self._generate_call_id(i)),
                                        name=name,
                                        arguments=args,
                                        raw_arguments=json.dumps(args),
                                    )
                                    state.completed_tools.append(tool_call)
                                
                                if state.completed_tools:
                                    completed_tool = state.completed_tools[-1]
                        except json.JSONDecodeError:
                            pass
                        
                        state.in_tool_call = False
                        state.buffer = ""
        
        return state, completed_tool


# =============================================================================
# Granite Tool Parser
# =============================================================================

class GraniteToolParser(ToolParser):
    """
    IBM Granite tool call parser.
    
    Format:
    <|tool_call|>
    {"name": "...", "arguments": {...}}
    <|end_of_text|>
    """
    
    TOOL_CALL_TAG = "<|tool_call|>"
    END_TAG = "<|end_of_text|>"
    
    @property
    def parser_type(self) -> ToolParserType:
        return ToolParserType.GRANITE
    
    def parse(self, text: str) -> ToolParseResult:
        result = ToolParseResult(raw_output=text)
        
        if self.TOOL_CALL_TAG not in text:
            result.content = text
            return result
        
        # Split by tool_call tag
        parts = text.split(self.TOOL_CALL_TAG)
        result.content = parts[0].strip()
        
        for i, part in enumerate(parts[1:]):
            # Remove end tag
            tool_json = part.replace(self.END_TAG, "").strip()
            
            try:
                data = json.loads(tool_json)
                name = data.get("name", "")
                args = data.get("arguments", {})
                
                tool_call = ToolCall(
                    id=self._generate_call_id(i),
                    name=name,
                    arguments=args,
                    raw_arguments=json.dumps(args),
                )
                result.tool_calls.append(tool_call)
            except json.JSONDecodeError as e:
                result.errors.append(f"JSON parse error: {e}")
        
        return result
    
    def parse_streaming(
        self,
        delta: str,
        state: StreamingToolState,
    ) -> Tuple[StreamingToolState, Optional[ToolCall]]:
        state.buffer += delta
        completed_tool = None
        
        if self.TOOL_CALL_TAG in state.buffer:
            state.in_tool_call = True
        
        if state.in_tool_call and self.END_TAG in state.buffer:
            # Extract between tags
            start = state.buffer.index(self.TOOL_CALL_TAG) + len(self.TOOL_CALL_TAG)
            end = state.buffer.index(self.END_TAG)
            tool_json = state.buffer[start:end].strip()
            
            try:
                data = json.loads(tool_json)
                name = data.get("name", "")
                args = data.get("arguments", {})
                
                completed_tool = ToolCall(
                    id=self._generate_call_id(state.tool_call_index),
                    name=name,
                    arguments=args,
                    raw_arguments=json.dumps(args),
                )
                state.completed_tools.append(completed_tool)
                state.tool_call_index += 1
            except json.JSONDecodeError:
                pass
            
            state.buffer = state.buffer[end + len(self.END_TAG):]
            state.in_tool_call = False
        
        return state, completed_tool


# =============================================================================
# Tool Parser Registry
# =============================================================================

class ToolParserRegistry:
    """
    Registry for tool parsers.
    
    Features:
    - Parser registration by type
    - Auto-detection of parser type
    - Model name to parser mapping
    """
    
    _instance: Optional["ToolParserRegistry"] = None
    _lock = threading.Lock()
    
    def __new__(cls) -> "ToolParserRegistry":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._init_registry()
            return cls._instance
    
    def _init_registry(self):
        self._parsers: Dict[ToolParserType, Type[ToolParser]] = {
            ToolParserType.GENERIC_JSON: JsonToolParser,
            ToolParserType.HERMES: HermesToolParser,
            ToolParserType.LLAMA3: Llama3ToolParser,
            ToolParserType.MISTRAL: MistralToolParser,
            ToolParserType.GRANITE: GraniteToolParser,
        }
        
        # Model name patterns to parser types
        self._model_patterns: List[Tuple[Pattern, ToolParserType]] = [
            (re.compile(r"hermes", re.I), ToolParserType.HERMES),
            (re.compile(r"llama.*3", re.I), ToolParserType.LLAMA3),
            (re.compile(r"mistral", re.I), ToolParserType.MISTRAL),
            (re.compile(r"granite", re.I), ToolParserType.GRANITE),
            (re.compile(r"qwen", re.I), ToolParserType.GENERIC_JSON),
        ]
    
    def get_parser(
        self,
        parser_type: ToolParserType,
    ) -> ToolParser:
        """Get a parser by type."""
        parser_class = self._parsers.get(parser_type)
        if parser_class is None:
            raise ValueError(f"Unknown parser type: {parser_type}")
        return parser_class()
    
    def get_parser_for_model(
        self,
        model_name: str,
    ) -> ToolParser:
        """Get a parser based on model name."""
        for pattern, parser_type in self._model_patterns:
            if pattern.search(model_name):
                return self.get_parser(parser_type)
        
        # Default to generic JSON
        return self.get_parser(ToolParserType.GENERIC_JSON)
    
    def register_parser(
        self,
        parser_type: ToolParserType,
        parser_class: Type[ToolParser],
    ):
        """Register a custom parser."""
        self._parsers[parser_type] = parser_class
    
    def register_model_pattern(
        self,
        pattern: str,
        parser_type: ToolParserType,
    ):
        """Register a model pattern to parser mapping."""
        self._model_patterns.insert(0, (re.compile(pattern, re.I), parser_type))
    
    def detect_parser_type(
        self,
        text: str,
    ) -> ToolParserType:
        """Auto-detect parser type from text."""
        if HermesToolParser.TOOL_CALL_OPEN in text:
            return ToolParserType.HERMES
        if Llama3ToolParser.PYTHON_TAG in text:
            return ToolParserType.LLAMA3
        if MistralToolParser.TOOL_CALLS_TAG in text:
            return ToolParserType.MISTRAL
        if GraniteToolParser.TOOL_CALL_TAG in text:
            return ToolParserType.GRANITE
        
        return ToolParserType.GENERIC_JSON


# =============================================================================
# Streaming Tool Parser
# =============================================================================

class StreamingToolParser:
    """
    High-level streaming tool parser.
    
    Features:
    - Auto-detects parser type
    - Maintains streaming state
    - Yields tool calls as they complete
    """
    
    def __init__(
        self,
        parser_type: Optional[ToolParserType] = None,
        model_name: Optional[str] = None,
    ):
        registry = ToolParserRegistry()
        
        if parser_type:
            self._parser = registry.get_parser(parser_type)
        elif model_name:
            self._parser = registry.get_parser_for_model(model_name)
        else:
            self._parser = registry.get_parser(ToolParserType.GENERIC_JSON)
        
        self._state = StreamingToolState()
    
    def feed(self, delta: str) -> Optional[ToolCall]:
        """
        Feed a token/delta to the parser.
        
        Returns:
            Completed ToolCall if one was finished, else None
        """
        self._state, completed = self._parser.parse_streaming(delta, self._state)
        return completed
    
    def finalize(self) -> ToolParseResult:
        """
        Finalize parsing and return all results.
        """
        # Parse any remaining buffer
        if self._state.buffer:
            result = self._parser.parse(self._state.buffer)
            result.tool_calls = self._state.completed_tools + result.tool_calls
            return result
        
        return ToolParseResult(
            tool_calls=self._state.completed_tools,
            content=self._state.buffer,
            raw_output=self._state.buffer,
        )
    
    def reset(self):
        """Reset parser state."""
        self._state = StreamingToolState()
    
    @property
    def completed_tools(self) -> List[ToolCall]:
        """Get all completed tool calls so far."""
        return self._state.completed_tools.copy()


# =============================================================================
# Utility Functions
# =============================================================================

def parse_tool_call(
    text: str,
    parser_type: Optional[ToolParserType] = None,
    model_name: Optional[str] = None,
) -> ToolParseResult:
    """
    Parse tool calls from text.
    
    Args:
        text: Model output text
        parser_type: Specific parser type (auto-detected if None)
        model_name: Model name for parser selection
    
    Returns:
        ToolParseResult with extracted tool calls
    """
    registry = ToolParserRegistry()
    
    if parser_type:
        parser = registry.get_parser(parser_type)
    elif model_name:
        parser = registry.get_parser_for_model(model_name)
    else:
        # Auto-detect
        detected_type = registry.detect_parser_type(text)
        parser = registry.get_parser(detected_type)
    
    return parser.parse(text)


def extract_json_from_text(text: str) -> List[str]:
    """
    Extract all JSON objects from text.
    
    Returns:
        List of JSON strings
    """
    results = []
    
    brace_depth = 0
    start_idx = -1
    in_string = False
    
    for i, char in enumerate(text):
        if char == '"' and (i == 0 or text[i-1] != '\\'):
            in_string = not in_string
        elif not in_string:
            if char == '{':
                if brace_depth == 0:
                    start_idx = i
                brace_depth += 1
            elif char == '}':
                brace_depth -= 1
                if brace_depth == 0 and start_idx >= 0:
                    results.append(text[start_idx:i+1])
                    start_idx = -1
    
    return results


def validate_tool_call(
    tool_call: ToolCall,
    tool_schema: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, List[str]]:
    """
    Validate a tool call against a schema.
    
    Returns:
        (is_valid, list_of_errors)
    """
    errors = []
    
    # Basic validation
    if not tool_call.name:
        errors.append("Tool name is required")
    
    if not isinstance(tool_call.arguments, dict):
        errors.append("Arguments must be a dictionary")
    
    # Schema validation
    if tool_schema and "parameters" in tool_schema:
        params = tool_schema["parameters"]
        required = params.get("required", [])
        properties = params.get("properties", {})
        
        for req in required:
            if req not in tool_call.arguments:
                errors.append(f"Missing required parameter: {req}")
        
        for key, value in tool_call.arguments.items():
            if key not in properties:
                errors.append(f"Unknown parameter: {key}")
    
    return len(errors) == 0, errors
