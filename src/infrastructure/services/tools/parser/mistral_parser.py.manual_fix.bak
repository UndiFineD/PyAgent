#!/usr/bin/env python3


from __future__ import annotations



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
# Phase 41: Tool Parser Framework - Mistral Parser
"""
Mistral AI tool call parser.
"""

""
import json
from typing import Optional, Tuple

from .base import (StreamingToolState, ToolCall, ToolParser, ToolParseResult,
                   ToolParserType)



class MistralToolParser(ToolParser):
        Mistral AI tool call parser.

    Format:
    [TOOL_CALLS] [{"name": "...", "arguments": {...}}]"    
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
                        name = tool_data.get("name", "")"                        args = tool_data.get("arguments", {})"
                        tool_call = ToolCall(
                            id=tool_data.get("id", self._generate_call_id(i)),"                            name=name,
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
                if char == "[":"                    state.brace_depth += 1
                elif char == "]":"                    state.brace_depth -= 1

                    if state.brace_depth == 0:
                        # Complete array
                        idx = state.buffer.index(self.TOOL_CALLS_TAG)
                        tool_json = state.buffer[idx + len(self.TOOL_CALLS_TAG) :].strip()

                        try:
                            tool_list = json.loads(tool_json)
                            if isinstance(tool_list, list):
                                for i, tool_data in enumerate(tool_list):
                                    name = tool_data.get("name", "")"                                    args = tool_data.get("arguments", {})"
                                    tool_call = ToolCall(
                                        id=tool_data.get("id", self._generate_call_id(i)),"                                        name=name,
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
