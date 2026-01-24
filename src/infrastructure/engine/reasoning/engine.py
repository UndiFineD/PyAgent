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

"""
Engine.py module.
"""

import json
import time
from collections import deque
from typing import Dict, Generator, Iterator, Optional, Tuple

from .data_classes import ParseResult, ThinkingBlock, ToolCall
from .enums import ParseState, ReasoningFormat, ToolCallFormat
from .implementations import (DeepSeekReasoningParser, GenericReasoningParser,
                              HermesToolParser, OpenAIToolParser,
                              QwenReasoningParser)
from .parsers import ReasoningParser, ToolParser


class ReasoningEngine:
    """
    Unified reasoning and tool call extraction engine.
    """

    _reasoning_parsers: Dict[ReasoningFormat, type] = {
        ReasoningFormat.DEEPSEEK_R1: DeepSeekReasoningParser,
        ReasoningFormat.QWEN3: QwenReasoningParser,
        ReasoningFormat.GENERIC: GenericReasoningParser,
    }

    _tool_parsers: Dict[ToolCallFormat, type] = {
        ToolCallFormat.OPENAI: OpenAIToolParser,
        ToolCallFormat.HERMES: HermesToolParser,
    }

    def __init__(
        self,
        reasoning_format: ReasoningFormat = ReasoningFormat.GENERIC,
        tool_format: ToolCallFormat = ToolCallFormat.NONE,
        enable_thinking: bool = True,
        cache_thoughts: bool = False,
        max_cached_thoughts: int = 1000,
    ):
        self.reasoning_format = reasoning_format
        self.tool_format = tool_format
        self.enable_thinking = enable_thinking
        self.cache_thoughts = cache_thoughts

        self._reasoning_parser: Optional[ReasoningParser] = None
        self._tool_parser: Optional[ToolParser] = None

        if reasoning_format != ReasoningFormat.NONE:
            parser_cls = self._reasoning_parsers.get(reasoning_format, GenericReasoningParser)
            self._reasoning_parser = parser_cls()

        if tool_format != ToolCallFormat.NONE:
            parser_cls = self._tool_parsers.get(tool_format, OpenAIToolParser)
            self._tool_parser = parser_cls()

        self._thought_cache: Dict[str, ThinkingBlock] = {}
        self._thought_lru: deque = deque(maxlen=max_cached_thoughts)

        self._stats = {
            "total_parsed": 0,
            "thinking_blocks_extracted": 0,
            "tool_calls_parsed": 0,
            "cache_hits": 0,
        }

    def parse(self, text: str) -> ParseResult:
        start_time = time.time()
        content = text
        thinking_blocks = []
        tool_calls = []

        if self._reasoning_parser and self.enable_thinking:
            content, thinking_blocks = self._reasoning_parser.extract_thinking(text)
            if self.cache_thoughts:
                for block in thinking_blocks:
                    cache_key = hash(block.content[:100])
                    if cache_key not in self._thought_cache:
                        self._thought_cache[str(cache_key)] = block
                        self._thought_lru.append(cache_key)

        if self._tool_parser:
            tool_calls = self._tool_parser.parse_tool_calls(content)

        self._stats["total_parsed"] += 1
        self._stats["thinking_blocks_extracted"] += len(thinking_blocks)
        self._stats["tool_calls_parsed"] += len(tool_calls)

        return ParseResult(
            content=content,
            thinking_blocks=thinking_blocks,
            tool_calls=tool_calls,
            raw_text=text,
            parse_time_ms=(time.time() - start_time) * 1000,
            tokens_processed=len(text),
        )

    def parse_streaming(
        self, token_stream: Iterator[str]
    ) -> Generator[Tuple[str, bool, Optional[ToolCall]], None, ParseResult]:
        buffer = ""
        for token in token_stream:
            buffer += token
            is_thinking = False
            tool_call = None
            if self._reasoning_parser:
                if self._reasoning_parser._state == ParseState.IN_THINK:
                    is_thinking = True
                elif self._reasoning_parser.start_marker in buffer:
                    self._reasoning_parser._state = ParseState.IN_THINK
                    is_thinking = True
            yield (token, is_thinking, tool_call)
        return self.parse(buffer)

    def detect_format(self, text: str) -> ReasoningFormat:
        if "<think>" in text and "</think>" in text:
            return ReasoningFormat.DEEPSEEK_R1
        if "<thinking>" in text:
            return ReasoningFormat.CLAUDE
        if "[THINK]" in text:
            return ReasoningFormat.MISTRAL
        if "<|start_think|>" in text:
            return ReasoningFormat.LLAMA_COT
        return ReasoningFormat.NONE

    def score_reasoning(self, block: ThinkingBlock) -> float:
        score = 0.0
        content = block.content
        if len(content) > 100:
            score += 0.2
        if len(content) > 500:
            score += 0.1
        steps = block.get_steps()
        if len(steps) >= 3:
            score += 0.2
        if len(steps) >= 5:
            score += 0.1
        logical_markers = [
            "therefore", "because", "thus", "hence", "so",
            "first", "second", "finally", "step", "let's"
        ]
        for marker in logical_markers:
            if marker.lower() in content.lower():
                score += 0.05
        return min(score, 1.0)

    def visualize_reasoning(self, result: ParseResult) -> str:
        lines = ["=" * 60, "REASONING CHAIN VISUALIZATION", "=" * 60]
        for i, block in enumerate(result.thinking_blocks):
            lines.append(f"\n📝 Thinking Block {i + 1}")
            lines.append("-" * 40)
            steps = block.get_steps()
            for j, step in enumerate(steps):
                lines.append(f"  {j + 1}. {step[:80]}{'...' if len(step) > 80 else ''}")
            score = self.score_reasoning(block)
            lines.append(f"\n  Quality Score: {score:.2f}")
        lines.append("\n" + "=" * 60)
        lines.append(f"Final Content: {result.content[:100]}...")
        if result.tool_calls:
            lines.append(f"\n🔧 Tool Calls: {len(result.tool_calls)}")
            for tc in result.tool_calls:
                lines.append(f"  - {tc.name}({json.dumps(tc.arguments)[:50]}...)")
        return "\n".join(lines)

    def get_stats(self) -> Dict[str, int]:
        return self._stats.copy()

    def reset(self) -> None:
        if self._reasoning_parser:
            self._reasoning_parser.reset()
        if self._tool_parser:
            self._tool_parser.reset()
        self._thought_cache.clear()
        self._thought_lru.clear()


def create_reasoning_engine(
    model_name: str = "", enable_thinking: bool = True, tool_format: ToolCallFormat = ToolCallFormat.NONE
) -> ReasoningEngine:
    reasoning_format = ReasoningFormat.GENERIC
    model_lower = model_name.lower()
    if "deepseek" in model_lower or "r1" in model_lower:
        reasoning_format = ReasoningFormat.DEEPSEEK_R1
    elif "qwen" in model_lower:
        reasoning_format = ReasoningFormat.QWEN3
    elif "claude" in model_lower:
        reasoning_format = ReasoningFormat.CLAUDE
    elif "mistral" in model_lower:
        reasoning_format = ReasoningFormat.MISTRAL

    return ReasoningEngine(reasoning_format=reasoning_format, tool_format=tool_format, enable_thinking=enable_thinking)


def create_tool_parser(format_type: ToolCallFormat = ToolCallFormat.OPENAI, strict: bool = False) -> ToolParser:
    parsers = {ToolCallFormat.OPENAI: OpenAIToolParser, ToolCallFormat.HERMES: HermesToolParser}
    parser_cls = parsers.get(format_type, OpenAIToolParser)
    return parser_cls(strict=strict)
