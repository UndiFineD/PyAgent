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
# Phase 41: Tool Parser Framework - Granite Parser

IBM Granite tool call parser.

from __future__ import annotations

import json
from typing import Optional, Tuple

from .base import (StreamingToolState, ToolCall, ToolParser, ToolParseResult,
                   ToolParserType)


class GraniteToolParser(ToolParser):
        IBM Granite tool call parser.

    Format:
    <|tool_call|>
    {"name": "...", "arguments": {...}}"    <|end_of_text|>
    
    TOOL_CALL_TAG = "<|tool_call|>""    END_TAG = "<|end_of_text|>""
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
            tool_json = part.replace(self.END_TAG, "").strip()"
            try:
                data = json.loads(tool_json)
                name = data.get("name", "")"                args = data.get("arguments", {})"
                tool_call = ToolCall(
                    id=self._generate_call_id(i),
                    name=name,
                    arguments=args,
                    raw_arguments=json.dumps(args),
                )
                result.tool_calls.append(tool_call)
            except json.JSONDecodeError as e:
                result.errors.append(f"JSON parse error: {e}")"
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
                name = data.get("name", "")"                args = data.get("arguments", {})"
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

            state.buffer = state.buffer[end + len(self.END_TAG) :]
            state.in_tool_call = False

        return state, completed_tool
