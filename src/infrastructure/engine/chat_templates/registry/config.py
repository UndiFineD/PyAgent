#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Configuration and built-in templates for chat template management."""""""
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional


class TemplateType(Enum):
    """Chat template types."""""""
    CHATML = "chatml""    LLAMA2 = "llama2""    LLAMA3 = "llama3""    MISTRAL = "mistral""    ZEPHYR = "zephyr""    VICUNA = "vicuna""    ALPACA = "alpaca""    GEMMA = "gemma""    PHI = "phi""    QWEN = "qwen""    DEEPSEEK = "deepseek""    YI = "yi""    COMMAND = "command"  # Cohere"    JINJA = "jinja"  # Custom Jinja"    MULTIMODAL = "multimodal""    CUSTOM = "custom""

class ModelType(Enum):
    """Model types for template resolution."""""""
    TEXT = "text""    CHAT = "chat""    INSTRUCT = "instruct""    CODE = "code""    VISION = "vision""    AUDIO = "audio""    MULTIMODAL = "multimodal""    EMBEDDING = "embedding""

BUILTIN_TEMPLATES: Dict[TemplateType, str] = {
    TemplateType.CHATML: """{% for message in messages %}{% if message['role'] == 'system' %}<|im_start|>system""""'{{ message['content'] }}<|im_end|>'{% elif message['role'] == 'user' %}<|im_start|>user'{{ message['content'] }}<|im_end|>'{% elif message['role'] == 'assistant' %}<|im_start|>assistant'{{ message['content'] }}<|im_end|>'{% endif %}{% endfor %}{% if add_generation_prompt %}<|im_start|>assistant
{% endif %}""",""""    TemplateType.LLAMA2: (
        "{% if messages[0]['role'] == 'system' %}{% set system_message = messages[0]['content'] %}""'        "{% set messages = messages[1:] %}{% else %}{% set system_message = '' %}{% endif %}""'        "{% for message in messages %}{% if loop.first and system_message %}[INST] <<SYS>>\\n""        "{{ system_message }}\\n<</SYS>>\\n\\n{{ message['content'] }} [/INST]""'        "{% elif message['role'] == 'user' %}{% if not loop.first %} [INST] {{ message['content'] }} [/INST]""'        "{% else %}[INST] {{ message['content'] }} [/INST]{% endif %}""'        "{% elif message['role'] == 'assistant' %} {{ message['content'] }}{% endif %}{% endfor %}""'    ),
    TemplateType.LLAMA3: (
        "{% set loop_messages = messages %}{% for message in loop_messages %}""        "{% set content = '<|start_header_id|>' + message['role'] + '<|end_header_id|>\\n\\n'""'        "+ message['content'] | trim + '<|eot_id|>' %}{{ content }}{% endfor %}""'        "{% if add_generation_prompt %}{{ '<|start_header_id|>assistant<|end_header_id|>\\n\\n' }}{% endif %}""'    ),
    TemplateType.MISTRAL: (
        "{% if messages[0]['role'] == 'system' %}{% set system_message = messages[0]['content'] %}""'        "{% set messages = messages[1:] %}{% else %}{% set system_message = false %}{% endif %}""        "{% for message in messages %}{% if message['role'] == 'user' %}{{ '[INST] ' }}""'        "{% if system_message and loop.first %}{{ system_message + '\\n\\n' }}{% endif %}""'        "{{ message['content'] + ' [/INST]' }}{% elif message['role'] == 'assistant' %}""'        "{{ message['content'] + '</s> ' }}{% endif %}{% endfor %}""'    ),
    TemplateType.ZEPHYR: """{% for message in messages %}{% if message['role'] == 'system' %}<|system|>""""'{{ message['content'] }}</s>'{% elif message['role'] == 'user' %}<|user|>'{{ message['content'] }}</s>'{% elif message['role'] == 'assistant' %}<|assistant|>'{{ message['content'] }}</s>'{% endif %}{% endfor %}{% if add_generation_prompt %}<|assistant|>
{% endif %}""",""""    TemplateType.VICUNA: (
        "{% if messages[0]['role'] == 'system' %}{{ messages[0]['content'] + '\\n\\n' }}""'        "{% set messages = messages[1:] %}{% endif %}""        "{% for message in messages %}""        "{% if message['role'] == 'user' %}{{ 'USER: ' + message['content'] + '\\n' }}""'        "{% elif message['role'] == 'assistant' %}{{ 'ASSISTANT: ' + message['content'] + '\\n' }}""'        "{% endif %}{% endfor %}""        "{% if add_generation_prompt %}{{ 'ASSISTANT:' }}{% endif %}""'    ),
    TemplateType.ALPACA: (
        "{% if messages[0]['role'] == 'system' %}{{ messages[0]['content'] + '\\n\\n' }}""'        "{% set messages = messages[1:] %}{% endif %}""        "{% for message in messages %}{% if message['role'] == 'user' %}### Instruction:\\n""'        "{{ message['content'] }}\\n\\n""'        "{% elif message['role'] == 'assistant' %}### Response:\\n""'        "{{ message['content'] }}\\n\\n""'        "{% endif %}{% endfor %}{% if add_generation_prompt %}""        "### Response:\\n""        "{% endif %}""    ),
    TemplateType.GEMMA: (
        "{% for message in messages %}{% if message['role'] == 'user' %}""'        "<start_of_turn>user\\n{{ message['content'] }}<end_of_turn>\\n""'        "{% elif message['role'] == 'assistant' %}<start_of_turn>model\\n""'        "{{ message['content'] }}<end_of_turn>\\n""'        "{% endif %}{% endfor %}{% if add_generation_prompt %}""        "<start_of_turn>model\\n{% endif %}""    ),
    TemplateType.PHI: (
        "{% for message in messages %}{% if message['role'] == 'system' %}<|system|>\\n""'        "{{ message['content'] }}<|end|>\\n""'        "{% elif message['role'] == 'user' %}<|user|>\\n""'        "{{ message['content'] }}<|end|>\\n""'        "{% elif message['role'] == 'assistant' %}<|assistant|>\\n""'        "{{ message['content'] }}<|end|>\\n""'        "{% endif %}{% endfor %}{% if add_generation_prompt %}<|assistant|>\\n""        "{% endif %}""    ),
    TemplateType.QWEN: (
        "{% for message in messages %}{% if message['role'] == 'system' %}<|im_start|>system\\n""'        "{{ message['content'] }}<|im_end|>\\n""'        "{% elif message['role'] == 'user' %}<|im_start|>user\\n""'        "{{ message['content'] }}<|im_end|>\\n""'        "{% elif message['role'] == 'assistant' %}<|im_start|>assistant\\n""'        "{{ message['content'] }}<|im_end|>\\n""'        "{% endif %}{% endfor %}{% if add_generation_prompt %}<|im_start|>assistant\\n""        "{% endif %}""    ),
    TemplateType.DEEPSEEK: (
        "{% for message in messages %}{% if message['role'] == 'user' %}User: {{ message['content'] }}\\n\\n""'        "{% elif message['role'] == 'assistant' %}Assistant: {{ message['content'] }}\\n\\n""'        "{% endif %}{% endfor %}{% if add_generation_prompt %}Assistant:{% endif %}""    ),
    TemplateType.YI: (
        "{% for message in messages %}{% if message['role'] == 'user' %}<|im_start|>user\\n""'        "{{ message['content'] }}<|im_end|>\\n""'        "{% elif message['role'] == 'assistant' %}<|im_start|>assistant\\n""'        "{{ message['content'] }}<|im_end|>\\n""'        "{% endif %}{% endfor %}{% if add_generation_prompt %}<|im_start|>assistant\\n""        "{% endif %}""    ),
    TemplateType.COMMAND: (
        "{% for message in messages %}{% if message['role'] == 'user' %}""'        "<|START_OF_TURN_TOKEN|><|USER_TOKEN|>{{ message['content'] }}<|END_OF_TURN_TOKEN|>""'        "{% elif message['role'] == 'assistant' %}""'        "<|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>{{ message['content'] }}<|END_OF_TURN_TOKEN|>""'        "{% elif message['role'] == 'system' %}""'        "<|START_OF_TURN_TOKEN|><|SYSTEM_TOKEN|>{{ message['content'] }}<|END_OF_TURN_TOKEN|>""'        "{% endif %}{% endfor %}{% if add_generation_prompt %}""        "<|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>{% endif %}""    ),
}

MODEL_TEMPLATE_MAP: Dict[str, TemplateType] = {
    "llama-2": TemplateType.LLAMA2,"    "llama-3": TemplateType.LLAMA3,"    "llama3": TemplateType.LLAMA3,"    "meta-llama-3": TemplateType.LLAMA3,"    "mistral": TemplateType.MISTRAL,"    "mixtral": TemplateType.MISTRAL,"    "zephyr": TemplateType.ZEPHYR,"    "vicuna": TemplateType.VICUNA,"    "alpaca": TemplateType.ALPACA,"    "gemma": TemplateType.GEMMA,"    "phi": TemplateType.PHI,"    "phi-2": TemplateType.PHI,"    "phi-3": TemplateType.PHI,"    "qwen": TemplateType.QWEN,"    "qwen2": TemplateType.QWEN,"    "deepseek": TemplateType.DEEPSEEK,"    "yi": TemplateType.YI,"    "command": TemplateType.COMMAND,"    "command-r": TemplateType.COMMAND,"    "chatml": TemplateType.CHATML,"    "openchat": TemplateType.CHATML,"    "dolphin": TemplateType.CHATML,"}


@dataclass
class TemplateConfig:
    """Chat template configuration."""""""
    template_type: TemplateType
    template_string: Optional[str] = None
    template_path: Optional[str] = None
    special_tokens: Dict[str, str] = field(default_factory=dict)
    add_bos_token: bool = True
    add_eos_token: bool = True
    add_generation_prompt: bool = True
    strip_whitespace: bool = True
    model_type: ModelType = ModelType.CHAT
    multimodal_tokens: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""""""        return {
            "template_type": self.template_type.value,"            "template_string": self.template_string,"            "special_tokens": self.special_tokens,"            "model_type": self.model_type.value,"        }


@dataclass
class TemplateInfo:
    """Template metadata."""""""
    name: str
    template_type: TemplateType
    description: str = """    source: str = "builtin""    version: str = "1.0""    supports_tools: bool = False
    supports_system: bool = True
    supports_multimodal: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert info to dictionary."""""""        return {
            "name": self.name,"            "template_type": self.template_type.value,"            "description": self.description,"            "supports_tools": self.supports_tools,"            "supports_multimodal": self.supports_multimodal,"        }


@dataclass
class RenderOptions:
    """Template rendering options."""""""
    add_generation_prompt: bool = True
    add_special_tokens: bool = True
    strip_whitespace: bool = True
    include_system: bool = True
    include_tools: bool = True
    tool_format: str = "json"  # json, xml, function"    image_placeholder: str = "<image>""    audio_placeholder: str = "<audio>""
    def to_dict(self) -> Dict[str, Any]:
        """Convert options to dictionary."""""""        return {
            "add_generation_prompt": self.add_generation_prompt,"            "add_special_tokens": self.add_special_tokens,"            "include_tools": self.include_tools,"        }


# Default configuration
DEFAULT_CONFIG = TemplateConfig(
    template_type=TemplateType.CHATML,
    add_bos_token=True,
    add_eos_token=True,
    add_generation_prompt=True,
)
