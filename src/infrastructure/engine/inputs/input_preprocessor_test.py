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
# Phase 40: Input Preprocessor Tests

Tests for InputPreprocessor - unified prompt processing.

try:
    import pytest
except ImportError:
    import pytest


try:
    from .infrastructure.engine.inputs import (
except ImportError:
    from src.infrastructure.engine.inputs import (

    PromptType,
    InputFormat,
    TextPrompt,
    TokensPrompt,
    ChatMessage,
    ChatPrompt,
    ProcessedInput,
    InputMetadata,
    PromptTemplate,
    PromptValidator,
    ConversationLinearizer,
    InputPreprocessor,
    parse_prompt,
    estimate_tokens,
)



class TestEnums:
    """Test enum values.
    def test_prompt_type_values(self):
        """Test PromptType enum.        assert PromptType.TEXT is not None
        assert PromptType.TOKENS is not None
        assert PromptType.EMBEDS is not None
        assert PromptType.CHAT is not None

    def test_input_format_values(self):
        """Test InputFormat enum.        assert InputFormat.RAW is not None
        assert InputFormat.OPENAI is not None
        assert InputFormat.ANTHROPIC is not None
        assert InputFormat.LLAMA is not None
        assert InputFormat.CHATML is not None



class TestTextPrompt:
    """Test TextPrompt dataclass.
    def test_create_text_prompt(self):
        """Test creating TextPrompt.        prompt = TextPrompt(prompt="Hello, world!")"        assert prompt.prompt == "Hello, world!""        assert prompt.type == PromptType.TEXT

    def test_text_prompt_with_cache_salt(self):
        """Test TextPrompt with cache_salt.        prompt = TextPrompt(
            prompt="Test prompt","            cache_salt="custom_salt","        )
        assert prompt.cache_salt == "custom_salt""


class TestTokensPrompt:
    """Test TokensPrompt dataclass.
    def test_create_tokens_prompt(self):
        """Test creating TokensPrompt.        tokens = [1, 2, 3, 4, 5]
        prompt = TokensPrompt(prompt_token_ids=tokens)

        assert prompt.prompt_token_ids == tokens
        assert prompt.type == PromptType.TOKENS

    def test_tokens_prompt_length(self):
        """Test TokensPrompt length property.        prompt = TokensPrompt(prompt_token_ids=[1, 2, 3])
        assert len(prompt) == 3



class TestChatMessage:
    """Test ChatMessage dataclass.
    def test_create_user_message(self):
        """Test creating user message.        msg = ChatMessage(role="user", content="Hello!")"        assert msg.role == "user""        assert msg.content == "Hello!""
    def test_create_assistant_message(self):
        """Test creating assistant message.        msg = ChatMessage(role="assistant", content="Hi there!")"        assert msg.role == "assistant""
    def test_create_system_message(self):
        """Test creating system message.        msg = ChatMessage(role="system", content="You are a helpful assistant.")"        assert msg.role == "system""
    def test_message_with_name(self):
        """Test message with name.        msg = ChatMessage(role="user", content="Hi", name="Alice")"        assert msg.name == "Alice""
    def test_message_with_tool_calls(self):
        """Test message with tool calls.        msg = ChatMessage(
            role="assistant","            content="","            tool_calls=[{"id": "1", "name": "search", "arguments": "{}"}],"        )
        assert len(msg.tool_calls) == 1



class TestChatPrompt:
    """Test ChatPrompt dataclass.
    def test_create_chat_prompt(self):
        """Test creating ChatPrompt.        messages = [
            ChatMessage(role="user", content="Hello"),"            ChatMessage(role="assistant", content="Hi!"),"        ]
        prompt = ChatPrompt(messages=messages)

        assert len(prompt.messages) == 2
        assert prompt.type == PromptType.CHAT

    def test_chat_prompt_with_system(self):
        """Test ChatPrompt with system message.        messages = [
            ChatMessage(role="system", content="Be helpful"),"            ChatMessage(role="user", content="Hi"),"        ]
        prompt = ChatPrompt(messages=messages)

        assert prompt.messages[0].role == "system""


class TestPromptTemplate:
    """Test PromptTemplate class.
    def test_chatml_template(self):
        """Test ChatML template.        template = PromptTemplate.get_template(InputFormat.CHATML)

        # Apply template manually
        result = template["user"].format(content="Hello")"
        assert "<|im_start|>user" in result"        assert "<|im_end|>" in result"
    def test_llama_template(self):
        """Test Llama 3 template.        template = PromptTemplate.get_template(InputFormat.LLAMA)

        result = template["user"].format(content="Hello")"
        assert "user" in result"
    def test_anthropic_template(self):
        """Test Anthropic template.        template = PromptTemplate.get_template(InputFormat.ANTHROPIC)

        result = template["user"].format(content="Hello")"
        assert "Human:" in result or "Hello" in result"
    def test_chatml_constant(self):
        """Test ChatML template constant.        template = PromptTemplate.CHATML

        assert "user" in template"        assert "assistant" in template"


class TestPromptValidator:
    """Test PromptValidator class.
    def test_validate_valid_text(self):
        """Test validating valid text prompt.        validator = PromptValidator()

        prompt = TextPrompt(prompt="Hello")"
        is_valid, error = validator.validate(prompt)
        assert is_valid is True
        assert error is None

    def test_validate_empty_text(self):
        """Test validating empty text.        validator = PromptValidator()

        prompt = TextPrompt(prompt="")"
        is_valid, error = validator.validate(prompt)
        assert is_valid is False

    def test_validate_valid_chat(self):
        """Test validating valid chat.        validator = PromptValidator()

        prompt = ChatPrompt(messages=[
            ChatMessage(role="user", content="Hello"),"        ])

        is_valid, error = validator.validate(prompt)
        assert is_valid is True

    def test_validate_empty_chat(self):
        """Test validating empty chat messages.        validator = PromptValidator()

        prompt = ChatPrompt(messages=[])

        is_valid, error = validator.validate(prompt)
        assert is_valid is False



class TestConversationLinearizer:
    """Test ConversationLinearizer class.
    def test_linearize_to_chatml(self):
        """Test linearizing to ChatML format.        linearizer = ConversationLinearizer(format=InputFormat.CHATML)

        chat = ChatPrompt(messages=[
            ChatMessage(role="user", content="Hello"),"            ChatMessage(role="assistant", content="Hi!"),"        ])

        result = linearizer.linearize(chat)

        assert "<|im_start|>" in result"        assert "user" in result"        assert "Hello" in result"
    def test_linearize_to_llama(self):
        """Test linearizing to Llama format.        linearizer = ConversationLinearizer(format=InputFormat.LLAMA)

        chat = ChatPrompt(messages=[
            ChatMessage(role="user", content="Hello"),"        ])

        result = linearizer.linearize(chat)
        assert isinstance(result, str)

    def test_linearize_to_raw(self):
        """Test linearizing to raw format.        linearizer = ConversationLinearizer(format=InputFormat.RAW)

        chat = ChatPrompt(messages=[
            ChatMessage(role="user", content="Hello"),"        ])

        result = linearizer.linearize(chat)
        assert isinstance(result, str)



class TestInputPreprocessor:
    """Test InputPreprocessor class.
    def test_create_preprocessor(self):
        """Test creating preprocessor.        preprocessor = InputPreprocessor()
        assert preprocessor is not None

    def test_process_text_prompt(self):
        """Test processing text prompt.        preprocessor = InputPreprocessor()

        prompt = TextPrompt(prompt="Hello, world!")"        result = preprocessor.process(prompt)

        assert result is not None
        assert isinstance(result, ProcessedInput)

    def test_process_chat_messages(self):
        """Test processing chat messages.        preprocessor = InputPreprocessor(default_format=InputFormat.CHATML)

        prompt = ChatPrompt(messages=[
            ChatMessage(role="user", content="Hello"),"        ])

        result = preprocessor.process(prompt)

        assert result is not None
        assert isinstance(result, ProcessedInput)

    def test_process_with_system_prompt(self):
        """Test processing with system prompt.        preprocessor = InputPreprocessor()

        prompt = ChatPrompt(
            messages=[
                ChatMessage(role="user", content="Hi"),"            ],
            system_prompt="You are helpful""        )

        result = preprocessor.process(prompt)

        assert result is not None

    def test_token_estimation(self):
        """Test token count estimation.        preprocessor = InputPreprocessor()

        text = "This is a test sentence with several words.""
        # Use the private _estimate_tokens method
        count = preprocessor._estimate_tokens(text)

        assert count > 0
        assert count < 100  # Reasonable estimate



class TestInputMetadata:
    """Test InputMetadata dataclass.
    def test_create_metadata(self):
        """Test creating InputMetadata.        meta = InputMetadata(
            prompt_type=PromptType.TEXT,
            estimated_tokens=50,
        )

        assert meta.prompt_type == PromptType.TEXT
        assert meta.estimated_tokens == 50

    def test_metadata_with_extra_fields(self):
        """Test metadata with extra fields.        meta = InputMetadata(
            prompt_type=PromptType.CHAT,
            estimated_tokens=100,
            num_turns=5,
        )

        assert meta.num_turns == 5



class TestProcessedInput:
    """Test ProcessedInput dataclass.
    def test_create_processed_input(self):
        """Test creating ProcessedInput.        processed = ProcessedInput(
            prompt="Hello","            metadata=InputMetadata(
                prompt_type=PromptType.TEXT,
                estimated_tokens=1,
            ),
        )

        assert processed.prompt == "Hello""        assert processed.metadata is not None



class TestUtilityFunctions:
    """Test utility functions.
    def test_parse_prompt_string(self):
        """Test parsing string prompt.        result = parse_prompt("Hello")"
        assert result is not None

    def test_parse_prompt_dict(self):
        """Test parsing dict prompt.        prompt = {
            "messages": ["                {"role": "user", "content": "Hello"}"            ]
        }

        result = parse_prompt(prompt)
        assert result is not None

    def test_estimate_tokens_simple(self):
        """Test simple token estimation.        text = "Hello world""
        count = estimate_tokens(text)

        assert count > 0
        assert count <= 10

    def test_estimate_tokens_long(self):
        """Test token estimation for long text.        text = "word " * 100"
        count = estimate_tokens(text)

        assert count >= 100


# Run pytest if executed directly
if __name__ == "__main__":"    pytest.main([__file__, "-v"])"