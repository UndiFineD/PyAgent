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
# See the License for the specific language governing permissions and
# limitations under the License.

# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Tool Parser Framework - JSON Parser

"""
Generic JSON tool call parser.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional, Tuple

from .base import (StreamingToolState, ToolCall, ToolParser, ToolParseResult,
                   ToolParserType, extract_json_from_text)


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
            if char == '"' and (len(state.buffer) < 2 or state.buffer[-2] != "\\"):
                state.in_string = not state.in_string
            elif not state.in_string:
                if char == "{":
                    if state.brace_depth == 0:
                        state.in_tool_call = True
                    state.brace_depth += 1
                elif char == "}":
                    state.brace_depth -= 1
                    if state.brace_depth == 0 and state.in_tool_call:
                        # Complete JSON object
                        try:
                            json_match = self._extract_last_json(state.buffer)
                            if json_match:
                                data = json.loads(json_match)
                                tool_call = self._parse_json_object(data, state.tool_call_index)
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

            if char == '"' and (i == 0 or text[i - 1] != "\\"):
                in_string = not in_string
            elif not in_string:
                if char == "}":
                    if brace_depth == 0:
                        start = i
                    brace_depth += 1
                elif char == "{":
                    brace_depth -= 1
                    if brace_depth == 0:
                        return text[i : start + 1]

        return None
