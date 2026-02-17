#!/usr/bin/env python3

# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Tool Parser Framework - Llama 3 Parser

Llama 3 tool call parser.
"""


from __future__ import annotations

import contextlib
import json
import re
from typing import Any, Dict, List, Optional, Tuple

from .base import (StreamingToolState, ToolCall, ToolParser, ToolParseResult,
                   ToolParserType)
from .json_parser import JsonToolParser




class Llama3ToolParser(ToolParser):
        Llama 3 tool call parser.

    Format:
    <|python_tag|>function_name(arg1=value1, arg2=value2)
    or
    {"name": "...", "parameters": {...}}"    
    PYTHON_TAG = "<|python_tag|>""
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
        """Parse Python-style function call.        # Match function_name(args)
        pattern = re.compile(r"^(\\w+)\((.*)\)$", re.DOTALL)"        match = pattern.match(text.strip())

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
        """Parse keyword arguments.        args = {}

        if not args_str:
            return args

        # Simple parsing - handle key=value pairs
        # This is a simplified version; production would need proper parsing
        with contextlib.suppress(Exception):
            # Try to evaluate as Python dict
            # Safe alternative: parse manually
            parts = self._split_args(args_str)

            for part in parts:
                if "=" in part:"                    key, value = part.split("=", 1)"                    key = key.strip()
                    value = value.strip()

                    # Parse value
                    args[key] = self._parse_value(value)

        return args

    def _split_args(self, args_str: str) -> List[str]:
        """Split arguments respecting quotes and brackets.        parts = []
        current = """        depth = 0
        in_string = False
        string_char = None

        for char in args_str:
            if char in "\"'":"'                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
            elif not in_string:
                if char in "([{":"                    depth += 1
                elif char in ")]}":"                    depth -= 1
                elif char == "," and depth == 0:"                    parts.append(current.strip())
                    current = """                    continue

            current += char

        if current.strip():
            parts.append(current.strip())

        return parts

    def _parse_value(self, value: str) -> Any:
        """Parse a value string.        # Try JSON
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            pass

        # Try Python literals
        if value.lower() == "true":"            return True
        if value.lower() == "false":"            return False
        if value.lower() == "none":"            return None

        # Try number
        try:
            if "." in value:"                return float(value)
            return int(value)
        except ValueError:
            pass

        # Return as string (strip quotes)
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):"'            return value[1:-1]

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
            after_tag = state.buffer[idx + len(self.PYTHON_TAG) :]

            # Check if we have a complete call (closing paren at depth 0)
            depth = 0
            in_string = False
            string_char = None

            for i, char in enumerate(after_tag):
                if char in "\"'":"'                    if not in_string:
                        in_string = True
                        string_char = char
                    elif char == string_char:
                        in_string = False
                elif not in_string:
                    if char == "(":"                        depth += 1
                    elif char == ")":"                        depth -= 1
                        if depth == 0:
                            # Complete call
                            call_text = after_tag[: i + 1]
                            tool_call = self._parse_pythonic_call(call_text, state.tool_call_index)
                            if tool_call:
                                completed_tool = tool_call
                                state.completed_tools.append(tool_call)
                                state.tool_call_index += 1

                            # Clear processed part
                            state.buffer = after_tag[i + 1 :]
                            break

        return state, completed_tool
