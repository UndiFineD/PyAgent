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
Phase 42: Chat Template Registry Tests

Tests for the chat template infrastructure.
"""


# Import from the package
from src.infrastructure.engine.chat_templates import (
    TemplateType,
    ModelType,
    ChatTemplate,
    ChatTemplateRegistry,
    JinjaTemplate,
    TemplateResolver,
    TemplateConfig,
    RenderOptions,
    detect_template_type,
    get_template,
    register_template,
    render_template,
)


class TestTemplateType:
    """Test TemplateType enum."""

    def test_template_type_values(self):
        """Test TemplateType enum values."""
        assert TemplateType.CHATML.value == "chatml"
        assert TemplateType.LLAMA2.value == "llama2"
        assert TemplateType.LLAMA3.value == "llama3"
        assert TemplateType.MISTRAL.value == "mistral"
        assert TemplateType.PHI.value == "phi"

    def test_more_template_types(self):
        """Test more template type values."""
        assert TemplateType.VICUNA.value == "vicuna"
        assert TemplateType.ALPACA.value == "alpaca"
        assert TemplateType.GEMMA.value == "gemma"
        assert TemplateType.QWEN.value == "qwen"

    def test_special_template_types(self):
        """Test special template types."""
        assert TemplateType.JINJA.value == "jinja"
        assert TemplateType.CUSTOM.value == "custom"
        assert TemplateType.MULTIMODAL.value == "multimodal"


class TestModelType:
    """Test ModelType enum."""

    def test_model_type_values(self):
        """Test ModelType enum values."""
        assert ModelType.TEXT.value == "text"
        assert ModelType.CHAT.value == "chat"
        assert ModelType.INSTRUCT.value == "instruct"
        assert ModelType.CODE.value == "code"

    def test_multimodal_types(self):
        """Test multimodal model types."""
        assert ModelType.VISION.value == "vision"
        assert ModelType.AUDIO.value == "audio"
        assert ModelType.MULTIMODAL.value == "multimodal"


class TestTemplateConfig:
    """Test TemplateConfig class."""

    def test_template_config_creation(self):
        """Test creating TemplateConfig."""
        config = TemplateConfig(template_type=TemplateType.CHATML)
        assert config.template_type == TemplateType.CHATML

    def test_template_config_defaults(self):
        """Test TemplateConfig defaults."""
        config = TemplateConfig(template_type=TemplateType.LLAMA3)
        assert config.add_generation_prompt is True
        assert config.add_bos_token is True
        assert config.add_eos_token is True

    def test_template_config_custom(self):
        """Test custom TemplateConfig."""
        config = TemplateConfig(
            template_type=TemplateType.MISTRAL,
            add_generation_prompt=False,
            strip_whitespace=False,
        )
        assert config.add_generation_prompt is False
        assert config.strip_whitespace is False


class TestRenderOptions:
    """Test RenderOptions class."""

    def test_render_options_defaults(self):
        """Test RenderOptions defaults."""
        options = RenderOptions()
        assert options.add_generation_prompt is True
        assert options.add_special_tokens is True

    def test_render_options_custom(self):
        """Test custom RenderOptions."""
        options = RenderOptions(
            add_generation_prompt=False,
            strip_whitespace=False,
        )
        assert options.add_generation_prompt is False
        assert options.strip_whitespace is False


class TestChatTemplate:
    """Test ChatTemplate abstract class."""

    def test_chat_template_is_abstract(self):
        """Test ChatTemplate is abstract."""
        # ChatTemplate is abstract, test the class exists
        assert hasattr(ChatTemplate, 'render')
        assert hasattr(ChatTemplate, 'get_template_string')

    def test_chat_template_class_exists(self):
        """Test ChatTemplate class exists."""
        assert ChatTemplate is not None


class TestJinjaTemplate:
    """Test JinjaTemplate class."""

    def test_jinja_template_creation(self):
        """Test creating JinjaTemplate."""
        config = TemplateConfig(
            template_type=TemplateType.JINJA,
            template_string="{{ message }}",
        )
        template = JinjaTemplate(config=config)
        assert template is not None


class TestChatTemplateRegistry:
    """Test ChatTemplateRegistry class."""

    def test_registry_creation(self):
        """Test creating ChatTemplateRegistry."""
        registry = ChatTemplateRegistry()
        assert registry is not None


class TestTemplateResolver:
    """Test TemplateResolver class."""

    def test_resolver_creation(self):
        """Test creating TemplateResolver."""
        resolver = TemplateResolver()
        assert resolver is not None


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_detect_template_type_exists(self):
        """Test detect_template_type exists."""
        assert callable(detect_template_type)

    def test_get_template_exists(self):
        """Test get_template exists."""
        assert callable(get_template)

    def test_register_template_exists(self):
        """Test register_template exists."""
        assert callable(register_template)

    def test_render_template_exists(self):
        """Test render_template exists."""
        assert callable(render_template)

    def test_detect_chatml(self):
        """Test detecting ChatML format."""
        text = "<|im_start|>system\nYou are helpful<|im_end|>"
        template_type = detect_template_type(text)
        assert template_type == TemplateType.CHATML

    def test_detect_llama(self):
        """Test detecting Llama format."""
        text = "[INST] Hello [/INST]"
        template_type = detect_template_type(text)
        assert template_type is not None
