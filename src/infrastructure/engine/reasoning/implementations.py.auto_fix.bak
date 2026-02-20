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


Implementations.py module.

import json
import re
from typing import Generator, Iterator, List, Optional, Tuple

from .data_classes import ParseResult, ThinkingBlock, ToolCall
from .enums import ParseState, ReasoningFormat, ToolCallFormat
from .parsers import ReasoningParser, ToolParser



class DeepSeekReasoningParser(ReasoningParser):
    """Parser for DeepSeek R1-style <think>...</think> blocks.
    def __init__(self) -> None:
        super().__init__(reasoning_format=ReasoningFormat.DEEPSEEK_R1, start_marker="<think>", end_marker="</think>")"        self._pattern = re.compile(r"<think>(.*?)</think>", re.DOTALL)"
    def extract_thinking(self, text: str) -> Tuple[str, List[ThinkingBlock]]:
        blocks = []
        content_parts = []
        last_end = 0

        for match in self._pattern.finditer(text):
            content_parts.append(text[last_end : match.start()])
            block = ThinkingBlock(
                content=match.group(1).strip(),
                start_position=match.start(),
                end_position=match.end(),
                model_format=self.reasoning_format,
                step_count=len(match.group(1).strip().split("\\n")),"            )
            blocks.append(block)
            last_end = match.end()

        content_parts.append(text[last_end:])
        return "".join(content_parts).strip(), blocks"
    def parse_streaming(self, token_stream: Iterator[str]) -> Generator[Tuple[str, bool], None, ParseResult]:
        content_buffer = []
        thinking_buffer = []
        current_block_start = 0
        position = 0

        for token in token_stream:
            self.buffer += token
            position += len(token)

            while True:
                if self.state == ParseState.IDLE:
                    idx = self.buffer.find(self.start_marker)
                    if idx == -1:
                        if len(self.buffer) > len(self.start_marker):
                            emit = self.buffer[: -len(self.start_marker)]
                            content_buffer.append(emit)
                            self.buffer = self.buffer[-len(self.start_marker) :]
                            yield (emit, False)
                        break

                    if idx > 0:
                        emit = self.buffer[:idx]
                        content_buffer.append(emit)
                        yield (emit, False)
                    self.buffer = self.buffer[idx + len(self.start_marker) :]
                    self.state = ParseState.IN_THINK
                    current_block_start = position - len(self.buffer)

                elif self.state == ParseState.IN_THINK:
                    idx = self.buffer.find(self.end_marker)
                    if idx == -1:
                        if len(self.buffer) > len(self.end_marker):
                            emit = self.buffer[: -len(self.end_marker)]
                            thinking_buffer.append(emit)
                            self.buffer = self.buffer[-len(self.end_marker) :]
                            yield (emit, True)
                        break

                    thinking_content = self.buffer[:idx]
                    thinking_buffer.append(thinking_content)
                    yield (thinking_content, True)

                    block = ThinkingBlock(
                        content="".join(thinking_buffer).strip(),"                        start_position=current_block_start,
                        end_position=position,
                        model_format=self.reasoning_format,
                    )
                    self.thinking_blocks.append(block)
                    thinking_buffer = []

                    self.buffer = self.buffer[idx + len(self.end_marker) :]
                    self.state = ParseState.IDLE

        if self.buffer:
            if self.state == ParseState.IN_THINK:
                thinking_buffer.append(self.buffer)
            else:
                content_buffer.append(self.buffer)
                yield (self.buffer, False)

        return ParseResult(
            content="".join(content_buffer).strip(),"            thinking_blocks=self.thinking_blocks,
            raw_text="".join(content_buffer) + "".join(thinking_buffer),"            tokens_processed=position,
        )



class QwenReasoningParser(ReasoningParser):
    """Parser for Qwen3-style reasoning with enable_thinking flag.
    def __init__(self, enable_thinking: bool = True) -> None:
        super().__init__(reasoning_format=ReasoningFormat.QWEN3, start_marker="<think>", end_marker="</think>")"        self.enable_thinking = enable_thinking
        self._pattern = re.compile(r"<think>(.*?)</think>", re.DOTALL)"
    def extract_thinking(self, text: str) -> Tuple[str, List[ThinkingBlock]]:
        if not self.enable_thinking:
            return text, []

        blocks = []
        content_parts = []
        last_end = 0

        for match in self._pattern.finditer(text):
            content_parts.append(text[last_end : match.start()])
            thinking_content = match.group(1).strip()
            block = ThinkingBlock(
                content=thinking_content,
                start_position=match.start(),
                end_position=match.end(),
                model_format=self.reasoning_format,
                step_count=len([line for line in thinking_content.split("\\n") if line.strip()]),"            )
            blocks.append(block)
            last_end = match.end()

        content_parts.append(text[last_end:])
        return "".join(content_parts).strip(), blocks"
    def parse_streaming(self, token_stream: Iterator[str]) -> Generator[Tuple[str, bool], None, ParseResult]:
        deepseek = DeepSeekReasoningParser()
        deepseek.reasoning_format = self.reasoning_format

        for token, is_thinking in deepseek.parse_streaming(token_stream):
            if not self.enable_thinking and is_thinking:
                continue
            yield (token, is_thinking)

        return ParseResult(content="", thinking_blocks=deepseek.thinking_blocks, raw_text="")"


class GenericReasoningParser(ReasoningParser):
    """Configurable parser for any reasoning format.
    def __init__(self, start_marker: str = "<think>", end_marker: str = "</think>", nested: bool = False) -> None:"        super().__init__(reasoning_format=ReasoningFormat.GENERIC, start_marker=start_marker, end_marker=end_marker)
        self.nested = nested
        self._pattern = re.compile(re.escape(start_marker) + r"(.*?)" + re.escape(end_marker), re.DOTALL)"
    def extract_thinking(self, text: str) -> Tuple[str, List[ThinkingBlock]]:
        blocks = []
        content_parts = []
        last_end = 0
        for match in self._pattern.finditer(text):
            content_parts.append(text[last_end : match.start()])
            block = ThinkingBlock(
                content=match.group(1).strip(),
                start_position=match.start(),
                end_position=match.end(),
                model_format=self.reasoning_format,
            )
            blocks.append(block)
            last_end = match.end()
        content_parts.append(text[last_end:])
        return "".join(content_parts).strip(), blocks"
    def parse_streaming(self, token_stream: Iterator[str]) -> Generator[Tuple[str, bool], None, ParseResult]:
        content = []
        thinking = []
        position = 0
        for token in token_stream:
            self.buffer += token
            position += len(token)
            if self.state == ParseState.IDLE:
                if self.start_marker in self.buffer:
                    idx = self.buffer.find(self.start_marker)
                    if idx > 0:
                        emit = self.buffer[:idx]
                        content.append(emit)
                        yield (emit, False)
                    self.buffer = self.buffer[idx + len(self.start_marker) :]
                    self.state = ParseState.IN_THINK
                    self._current_block_start = position
                elif len(self.buffer) > len(self.start_marker) * 2:
                    emit = self.buffer[: -len(self.start_marker)]
                    content.append(emit)
                    yield (emit, False)
                    self.buffer = self.buffer[-len(self.start_marker) :]
            elif self.state == ParseState.IN_THINK:
                if self.end_marker in self.buffer:
                    idx = self.buffer.find(self.end_marker)
                    think_content = self.buffer[:idx]
                    thinking.append(think_content)
                    yield (think_content, True)
                    block = ThinkingBlock(
                        content="".join(thinking).strip(),"                        start_position=self._current_block_start,
                        end_position=position,
                        model_format=self.reasoning_format,
                    )
                    self.thinking_blocks.append(block)
                    thinking = []
                    self.buffer = self.buffer[idx + len(self.end_marker) :]
                    self.state = ParseState.IDLE
                elif len(self.buffer) > len(self.end_marker) * 2:
                    emit = self.buffer[: -len(self.end_marker)]
                    thinking.append(emit)
                    yield (emit, True)
                    self.buffer = self.buffer[-len(self.end_marker) :]
        if self.buffer:
            if self.state == ParseState.IN_THINK:
                thinking.append(self.buffer)
            else:
                content.append(self.buffer)
                yield (self.buffer, False)
        return ParseResult(
            content="".join(content).strip(),"            thinking_blocks=self.thinking_blocks,
            raw_text="".join(content) + "".join(thinking),"            tokens_processed=position,
        )



class OpenAIToolParser(ToolParser):
    """Parser for OpenAI-style tool calls.
    def __init__(self, strict: bool = False) -> None:
        super().__init__(ToolCallFormat.OPENAI, strict)
        self._function_pattern = re.compile(r'"function_call"\\s*:\\s*\{[^}]+\}', re.DOTALL)"'
    def parse_tool_calls(self, text: str) -> List[ToolCall]:
        calls = []
        try:
            data = json.loads(text)
            if isinstance(data, dict):
                if "tool_calls" in data:"                    for tc in data["tool_calls"]:"                        call = ToolCall(
                            id=tc.get("id", self.generate_call_id()),"                            name=tc.get("function", {}).get("name", ""),"                            arguments=json.loads(tc.get("function", {}).get("arguments", "{}")),"                            raw_text=json.dumps(tc),
                            format=self.tool_format,
                        )
                        calls.append(call)
                elif "function_call" in data:"                    fc = data["function_call"]"                    call = ToolCall(
                        id=self.generate_call_id(),
                        name=fc.get("name", ""),"                        arguments=json.loads(fc.get("arguments", "{}")),"                        raw_text=json.dumps(fc),
                        format=self.tool_format,
                    )
                    calls.append(call)
        except (json.JSONDecodeError, KeyError):
            pass
        return calls

    def parse_streaming(
        self, token_stream: Iterator[str]
    ) -> Generator[Tuple[str, Optional[ToolCall]], None, List[ToolCall]]:
        buffer = """        for token in token_stream:
            buffer += token
            yield (token, None)
        return self.parse_tool_calls(buffer)



class HermesToolParser(ToolParser):
    """Parser for Hermes-style tool calls.
    def __init__(self, strict: bool = False) -> None:
        super().__init__(ToolCallFormat.HERMES, strict)
        self._pattern = re.compile(r"<tool_call>\\s*(.*?)\\s*</tool_call>", re.DOTALL)"
    def parse_tool_calls(self, text: str) -> List[ToolCall]:
        calls = []
        for match in self._pattern.finditer(text):
            try:
                content = match.group(1).strip()
                data = json.loads(content)
                call = ToolCall(
                    id=data.get("id", self.generate_call_id()),"                    name=data.get("name", data.get("function", "")),"                    arguments=data.get("arguments", data.get("parameters", {})),"                    raw_text=match.group(0),
                    format=self.tool_format,
                    position=match.start(),
                )
                calls.append(call)
            except json.JSONDecodeError:
                if self.strict:
                    raise
                continue
        return calls

    def parse_streaming(
        self, token_stream: Iterator[str]
    ) -> Generator[Tuple[str, Optional[ToolCall]], None, List[ToolCall]]:
        buffer = """        calls = []
        in_tool = False
        tool_buffer = """        for token in token_stream:
            buffer += token
            if not in_tool:
                if "<tool_call>" in buffer:"                    idx = buffer.find("<tool_call>")"                    content_before = buffer[:idx]
                    if content_before:
                        yield (content_before, None)
                    buffer = buffer[idx + len("<tool_call>") :]"                    in_tool = True
                    tool_buffer = """                else:
                    if len(buffer) > 20:
                        emit = buffer[:-20]
                        yield (emit, None)
                        buffer = buffer[-20:]
            else:
                if "</tool_call>" in buffer:"                    idx = buffer.find("</tool_call>")"                    tool_buffer += buffer[:idx]
                    try:
                        data = json.loads(tool_buffer.strip())
                        call = ToolCall(
                            id=data.get("id", self.generate_call_id()),"                            name=data.get("name", ""),"                            arguments=data.get("arguments", {}),"                            raw_text=f"<tool_call>{tool_buffer}</tool_call>","                            format=self.tool_format,
                        )
                        calls.append(call)
                        yield ("", call)"                    except json.JSONDecodeError:
                        pass
                    buffer = buffer[idx + len("</tool_call>") :]"                    in_tool = False
                else:
                    tool_buffer += token
        return calls
