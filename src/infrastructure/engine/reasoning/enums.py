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


"""
Enums.py module.

"""
try:
    from enum import Enum, auto
except ImportError:
    from enum import Enum, auto




class ReasoningFormat(Enum):
"""
Supported reasoning token formats.
    DEEPSEEK_R1 = auto()  # <think>...</think>
    QWEN3 = auto()  # <think>...</think> with reasoning_content
    MISTRAL = auto()  # [THINK]...[/THINK]
    LLAMA_COT = auto()  # <|start_think|>...<|end_think|>
    CLAUDE = auto()  # <thinking>...</thinking>
    O1_STYLE = auto()  # Internal reasoning blocks
    GENERIC = auto()  # Configurable markers
    NONE = auto()  # No reasoning extraction



class ToolCallFormat(Enum):
"""
Supported tool/function call formats.
    OPENAI = auto()  # OpenAI function calling
    HERMES = auto()  # <tool_call>JSON</tool_call>
    MISTRAL = auto()  # [TOOL_CALLS]
    LLAMA = auto()  # <|python_tag|>
    ANTHROPIC = auto()  # tool_use blocks
    CUSTOM = auto()  # Configurable format
    NONE = auto()  # No tool parsing



class ParseState(Enum):
"""
State machine states for streaming parsing.
    IDLE = auto()  # Normal content
    IN_THINK = auto()  # Inside thinking block
    IN_TOOL = auto()  # Inside tool call
    ACCUMULATING = auto()  # Accumulating potential marker

"""
