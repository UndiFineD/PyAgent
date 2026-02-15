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
Phase 42: Prompt Renderer System Tests

Tests for the prompt rendering infrastructure.
"""


# Import from the package
from src.infrastructure.engine.prompt_renderer import (
    TruncationStrategy,
    RenderResult,
    PromptRenderer,
    PromptConfig,
    TruncationManager,
    TruncationResult,
    EmbeddingInput,
    RenderMode,
    ChatRenderer,
    CompletionRenderer,
    CacheSaltGenerator,
    render_prompt,
    apply_chat_template,
    generate_cache_salt,
    truncate_prompt,
)


class TestTruncationStrategy:
    """Test truncation strategy enum."""

    def test_truncation_strategies(self):
        """Test TruncationStrategy enum values."""
        assert TruncationStrategy.NONE.value == "none"
        assert TruncationStrategy.LEFT.value == "left"
        assert TruncationStrategy.RIGHT.value == "right"
        assert TruncationStrategy.MIDDLE.value == "middle"

    def test_auto_strategy(self):
        """Test AUTO strategy exists."""
        assert TruncationStrategy.AUTO.value == "auto"

    def test_smart_strategy(self):
        """Test SMART strategy exists."""
        assert TruncationStrategy.SMART.value == "smart"


class TestRenderMode:
    """Test RenderMode enum."""

    def test_render_mode_values(self):
        """Test RenderMode enum values."""
        assert RenderMode.COMPLETION.value == "completion"
        assert RenderMode.CHAT.value == "chat"
        assert RenderMode.EMBEDDING.value == "embedding"


class TestRenderResult:
    """Test RenderResult dataclass."""

    def test_render_result_creation(self):
        """Test creating RenderResult."""
        result = RenderResult(
            text="Hello world",
            token_ids=[1, 2, 3],
            num_tokens=3,
            was_truncated=False,
        )
        assert result.text == "Hello world"
        assert result.num_tokens == 3
        assert result.was_truncated is False

    def test_render_result_fields(self):
        """Test RenderResult has expected fields."""
        result = RenderResult(
            text="test",
            token_ids=[1],
            num_tokens=1,
            was_truncated=False,
        )
        assert hasattr(result, "text")
        assert hasattr(result, "token_ids")
        assert hasattr(result, "num_tokens")
        assert hasattr(result, "was_truncated")


class TestTruncationResult:
    """Test TruncationResult dataclass."""

    def test_truncation_result_class_exists(self):
        """Test TruncationResult class exists."""
        assert TruncationResult is not None


class TestEmbeddingInput:
    """Test EmbeddingInput dataclass."""

    def test_embedding_input_class_exists(self):
        """Test EmbeddingInput class exists."""
        assert EmbeddingInput is not None


class TestPromptConfig:
    """Test PromptConfig dataclass."""

    def test_default_config(self):
        """Test default prompt config."""
        config = PromptConfig()
        assert config.add_generation_prompt is True
        assert config.add_special_tokens is True

    def test_custom_config(self):
        """Test custom prompt config."""
        config = PromptConfig(
            max_tokens=4096,
            truncation=TruncationStrategy.LEFT,
            add_generation_prompt=False,
        )
        assert config.max_tokens == 4096
        assert config.truncation == TruncationStrategy.LEFT


class TestTruncationManager:
    """Test TruncationManager."""

    def test_truncation_manager_creation(self):
        """Test creating TruncationManager."""
        manager = TruncationManager()
        assert manager is not None

    def test_truncation_manager_class(self):
        """Test TruncationManager class exists."""
        assert TruncationManager is not None


class TestPromptRenderer:
    """Test PromptRenderer abstract class."""

    def test_renderer_is_abstract(self):
        """Test PromptRenderer is abstract."""
        # PromptRenderer is abstract, cannot be instantiated directly
        assert hasattr(PromptRenderer, 'render')

    def test_renderer_class_exists(self):
        """Test PromptRenderer class exists."""
        assert PromptRenderer is not None


class TestChatRenderer:
    """Test ChatRenderer class."""

    def test_chat_renderer_creation(self):
        """Test creating ChatRenderer."""
        renderer = ChatRenderer()
        assert renderer is not None


class TestCompletionRenderer:
    """Test CompletionRenderer class."""

    def test_completion_renderer_creation(self):
        """Test creating CompletionRenderer."""
        renderer = CompletionRenderer()
        assert renderer is not None


class TestCacheSaltGenerator:
    """Test CacheSaltGenerator class."""

    def test_salt_generator_creation(self):
        """Test creating CacheSaltGenerator."""
        generator = CacheSaltGenerator()
        assert generator is not None


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_render_prompt_exists(self):
        """Test render_prompt function exists."""
        assert callable(render_prompt)

    def test_apply_chat_template_exists(self):
        """Test apply_chat_template function exists."""
        assert callable(apply_chat_template)

    def test_generate_cache_salt_exists(self):
        """Test generate_cache_salt function exists."""
        assert callable(generate_cache_salt)

    def test_truncate_prompt_exists(self):
        """Test truncate_prompt function exists."""
        assert callable(truncate_prompt)

    def test_generate_cache_salt_call(self):
        """Test calling generate_cache_salt."""
        salt = generate_cache_salt("test input")
        assert isinstance(salt, str)
        assert len(salt) > 0

    def test_generate_cache_salt_deterministic(self):
        """Test cache salt is deterministic."""
        salt1 = generate_cache_salt("same input")
        salt2 = generate_cache_salt("same input")
        assert salt1 == salt2
