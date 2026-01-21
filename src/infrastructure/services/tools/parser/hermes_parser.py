# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 41: Tool Parser Framework - Hermes Parser

"""
Hermes/NousResearch tool call parser.
"""

from __future__ import annotations

import json
import re
from typing import Optional, Tuple

from .base import (
    ToolParser,
    ToolParserType,
    ToolCall,
    ToolParseResult,
    StreamingToolState,
)


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
