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
# Phase 40: Input Preprocessor - Unified Prompt Processing
# Inspired by vLLM's inputs/preprocess.py and inputs/data.py'
InputPreprocessor: Unified input processing with schema validation.

Provides:
- Type-safe prompt schemas (text, tokens, embeddings)
- Encoder-decoder prompt separation
- Multi-turn conversation linearization
- Embedding cache integration
- Input size estimation for batch scheduling

try:
    import re
except ImportError:
    import re

try:
    import time
except ImportError:
    import time

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field

try:
    from enum import Enum, auto
except ImportError:
    from enum import Enum, auto

try:
    from typing import Any, Dict, List, Optional, Tuple, Union
except ImportError:
    from typing import Any, Dict, List, Optional, Tuple, Union


try:
    import numpy
except ImportError:
    import numpy
 as np

# =============================================================================
# Enums
# =============================================================================



class PromptType(Enum):
    """Types of prompt input.
    TEXT = auto()  # Raw text string
    TOKENS = auto()  # Pre-tokenized token IDs
    EMBEDS = auto()  # Pre-computed embeddings
    ENCODER_DECODER = auto()  # Separate encoder/decoder prompts
    CHAT = auto()  # Multi-turn conversation
    HYBRID = auto()  # Mixed text and tokens



class InputFormat(Enum):
    """Input format specifications.
    RAW = auto()  # Raw input as-is
    OPENAI = auto()  # OpenAI chat format
    ANTHROPIC = auto()  # Anthropic messages format
    LLAMA = auto()  # Llama special tokens format
    CHATML = auto()  # ChatML format
    CUSTOM = auto()  # Custom template


# =============================================================================
# Prompt Data Classes
# =============================================================================


@dataclass
class TextPrompt:
    """Text-based prompt.
    prompt: str
    cache_salt: Optional[str] = None  # Custom salt for prefix caching
    multi_modal_data: Optional[Dict] = None

    @property
    def type(self) -> PromptType:
        """Get prompt type.        return PromptType.TEXT

    def __len__(self) -> int:
        """Get length of prompt.        return len(self.prompt)


@dataclass
class TokensPrompt:
    """Pre-tokenized prompt.
    prompt_token_ids: List[int]
    token_type_ids: Optional[List[int]] = None  # For cross-encoders
    cache_salt: Optional[str] = None
    multi_modal_data: Optional[Dict] = None

    @property
    def type(self) -> PromptType:
        """Get the prompt type.        return PromptType.TOKENS

    def __len__(self) -> int:
        """Return the number of tokens.        return len(self.prompt_token_ids)


@dataclass
class EmbedsPrompt:
    """Pre-computed embeddings prompt.
    prompt_embeds: np.ndarray  # Shape: (seq_len, hidden_dim)
    cache_salt: Optional[str] = None

    @property
    def type(self) -> PromptType:
        """Get the prompt type.        return PromptType.EMBEDS

    def __len__(self) -> int:
        """Return the sequence length of the embeddings.        return self.prompt_embeds.shape[0]


@dataclass
class EncoderDecoderPrompt:
    """Prompt for encoder-decoder models (T5, BART, etc.).
    encoder_prompt: Union[TextPrompt, TokensPrompt, EmbedsPrompt]
    decoder_prompt: Optional[Union[TextPrompt, TokensPrompt]] = None

    @property
    def type(self) -> PromptType:
        """Get the prompt type.        return PromptType.ENCODER_DECODER


@dataclass
class ChatMessage:
    """Single message in a conversation.
    role: str  # system, user, assistant, tool
    content: str
    name: Optional[str] = None  # Optional name for multi-agent
    tool_calls: Optional[List[Dict]] = None  # For assistant tool calls
    tool_call_id: Optional[str] = None  # For tool responses

    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary.        result = {"role": self.role, "content": self.content}"        if self.name:
            result["name"] = self.name"        if self.tool_calls:
            result["tool_calls"] = self.tool_calls"        if self.tool_call_id:
            result["tool_call_id"] = self.tool_call_id"        return result


@dataclass
class ChatPrompt:
    """Multi-turn conversation prompt.
    messages: List[ChatMessage]
    system_prompt: Optional[str] = None

    @property
    def type(self) -> PromptType:
        """Get prompt type.        return PromptType.CHAT

    def __len__(self) -> int:
        """Get total character length of messages.        return sum(len(m.content) for m in self.messages)


# Unified prompt type
SingletonPrompt = Union[TextPrompt, TokensPrompt, EmbedsPrompt, EncoderDecoderPrompt, ChatPrompt]


# =============================================================================
# Processed Input
# =============================================================================


@dataclass
class InputMetadata:
    """Metadata about processed input.
    prompt_type: PromptType
    estimated_tokens: int
    has_system_prompt: bool = False
    num_turns: int = 1
    has_multimodal: bool = False
    has_embeddings: bool = False
    cache_key: Optional[str] = None
    processing_time_ms: float = 0.0


@dataclass
class ProcessedInput:
    """Fully processed input ready for model.
    prompt: str  # Linearized text prompt
    token_ids: Optional[List[int]] = None  # Tokenized if available
    embeddings: Optional[np.ndarray] = None  # Pre-computed embeddings
    attention_mask: Optional[List[int]] = None
    token_type_ids: Optional[List[int]] = None
    metadata: InputMetadata = field(
        default_factory=lambda: InputMetadata(prompt_type=PromptType.TEXT, estimated_tokens=0)
    )

    @property
    def length(self) -> int:
        """Get best-effort length (tokens if available, else chars).        if self.token_ids:
            return len(self.token_ids)
        return len(self.prompt)


# =============================================================================
# Prompt Templates
# =============================================================================



class PromptTemplate:
    """Template for formatting prompts.
    # Common templates
    CHATML = {
        "system": "<|im_start|>system\\n{content}<|im_end|>\\n","        "user": "<|im_start|>user\\n{content}<|im_end|>\\n","        "assistant": "<|im_start|>assistant\\n{content}<|im_end|>\\n","        "assistant_start": "<|im_start|>assistant\\n","    }

    LLAMA3 = {
        "system": "<|start_header_id|>system<|end_header_id|>\\n\\n{content}<|eot_id|>","        "user": "<|start_header_id|>user<|end_header_id|>\\n\\n{content}<|eot_id|>","        "assistant": "<|start_header_id|>assistant<|end_header_id|>\\n\\n{content}<|eot_id|>","        "assistant_start": "<|start_header_id|>assistant<|end_header_id|>\\n\\n","    }

    MISTRAL = {
        "system": "[INST] {content} [/INST]","        "user": "[INST] {content} [/INST]","        "assistant": "{content}</s>","        "assistant_start": "","    }

    ANTHROPIC = {
        "system": "",  # System handled separately"        "user": "\\n\\nHuman: {content}","        "assistant": "\\n\\nAssistant: {content}","        "assistant_start": "\\n\\nAssistant:","    }

    @classmethod
    def get_template(cls, input_format: InputFormat) -> Dict[str, str]:
        """Get template for format.        templates = {
            InputFormat.CHATML: cls.CHATML,
            InputFormat.LLAMA: cls.LLAMA3,
            InputFormat.ANTHROPIC: cls.ANTHROPIC,
        }
        return templates.get(input_format, cls.CHATML)


# =============================================================================
# Prompt Validator
# =============================================================================



class PromptValidator:
    """Validates prompt inputs.
    def __init__(
        self,
        max_length: int = 8192,
        allow_empty: bool = False,
        require_user_message: bool = True,
    ) -> None:
        self.max_length = max_length
        self.allow_empty = allow_empty
        self.require_user_message = require_user_message

    def validate(self, prompt: SingletonPrompt) -> Tuple[bool, Optional[str]]:
        """Validate prompt, return (is_valid, error_message).        if isinstance(prompt, TextPrompt):
            return self._validate_text(prompt)
        if isinstance(prompt, TokensPrompt):
            return self._validate_tokens(prompt)
        if isinstance(prompt, EmbedsPrompt):
            return self._validate_embeds(prompt)
        if isinstance(prompt, ChatPrompt):
            return self._validate_chat(prompt)
        if isinstance(prompt, EncoderDecoderPrompt):
            return self._validate_encoder_decoder(prompt)
        return False, f"Unknown prompt type: {type(prompt)}""
    def _validate_text(self, prompt: TextPrompt) -> Tuple[bool, Optional[str]]:
        if not self.allow_empty and not prompt.prompt.strip():
            return False, "Empty text prompt""        if len(prompt.prompt) > self.max_length * 4:  # ~4 chars per token
            return False, f"Text prompt too long: {len(prompt.prompt)} chars""        return True, None

    def _validate_tokens(self, prompt: TokensPrompt) -> Tuple[bool, Optional[str]]:
        if not self.allow_empty and not prompt.prompt_token_ids:
            return False, "Empty token prompt""        if len(prompt.prompt_token_ids) > self.max_length:
            return False, f"Token prompt too long: {len(prompt.prompt_token_ids)} tokens""        if any(tid < 0 for tid in prompt.prompt_token_ids):
            return False, "Negative token IDs not allowed""        return True, None

    def _validate_embeds(self, prompt: EmbedsPrompt) -> Tuple[bool, Optional[str]]:
        if prompt.prompt_embeds.ndim != 2:
            return False, f"Embeddings must be 2D, got {prompt.prompt_embeds.ndim}D""        if prompt.prompt_embeds.shape[0] > self.max_length:
            return False, f"Embedding sequence too long: {prompt.prompt_embeds.shape[0]}""        return True, None

    def _validate_chat(self, prompt: ChatPrompt) -> Tuple[bool, Optional[str]]:
        if not prompt.messages:
            return False, "Empty chat messages""
        if self.require_user_message:
            has_user = any(m.role == "user" for m in prompt.messages)"            if not has_user:
                return False, "Chat must contain at least one user message""
        total_length = sum(len(m.content) for m in prompt.messages)
        if total_length > self.max_length * 4:
            return False, f"Chat too long: {total_length} chars""
        return True, None

    def _validate_encoder_decoder(self, prompt: EncoderDecoderPrompt) -> Tuple[bool, Optional[str]]:
        enc_valid, enc_error = self.validate(prompt.encoder_prompt)
        if not enc_valid:
            return False, f"Encoder prompt: {enc_error}""
        if prompt.decoder_prompt:
            dec_valid, dec_error = self.validate(prompt.decoder_prompt)
            if not dec_valid:
                return False, f"Decoder prompt: {dec_error}""
        return True, None


# =============================================================================
# Conversation Linearizer
# =============================================================================



class ConversationLinearizer:
        Linearizes multi-turn conversations to single prompt.

    Supports multiple chat formats (ChatML, Llama, Anthropic, etc.)
    
    def __init__(
        self,
        input_format: InputFormat = InputFormat.CHATML,
        add_generation_prompt: bool = True,
        **kwargs: Any,
    ) -> None:
        self.format = kwargs.get("format", input_format)"        self.add_generation_prompt = add_generation_prompt
        self.template = PromptTemplate.get_template(self.format)

    def linearize(self, chat: ChatPrompt) -> str:
        """Convert chat to linear prompt string.        parts = []

        # System prompt
        if chat.system_prompt:
            parts.append(self.template["system"].format(content=chat.system_prompt))"
        # Messages
        for message in chat.messages:
            template_key = message.role
            if template_key not in self.template:
                template_key = "user"  # Fallback"
            parts.append(self.template[template_key].format(content=message.content))

        # Generation prompt
        if self.add_generation_prompt:
            parts.append(self.template["assistant_start"])"
        return "".join(parts)"
    def parse_messages(self, text: str) -> List[ChatMessage]:
        """Parse linearized text back to messages (if possible).        messages = []

        if self.format == InputFormat.CHATML:
            pattern = r"<\|im_start\|>(\\w+)\\n(.*?)<\|im_end\|>""            for match in re.finditer(pattern, text, re.DOTALL):
                role, content = match.groups()
                messages.append(ChatMessage(role=role, content=content.strip()))

        return messages


# =============================================================================
# Main Input Preprocessor
# =============================================================================



class InputPreprocessor:
        Unified input preprocessing for LLM inference.

    Features beyond vLLM:
    - JSON Schema validation for structured inputs
    - Automatic prompt template detection
    - Multi-turn conversation linearization
    - Embedding cache integration
    - Input size estimation for scheduling
    
    def __init__(
        self,
        tokenizer: Optional[Any] = None,
        default_format: InputFormat = InputFormat.CHATML,
        max_length: int = 8192,
        truncation: bool = True,
        estimate_chars_per_token: float = 4.0,
    ) -> None:
        self.tokenizer = tokenizer
        self.default_format = default_format
        self.max_length = max_length
        self.truncation = truncation
        self.estimate_chars_per_token = estimate_chars_per_token

        self.validator = PromptValidator(max_length=max_length)
        self.linearizer = ConversationLinearizer(input_format=default_format)

        # Statistics
        self._stats = {
            "total_processed": 0,"            "text_prompts": 0,"            "token_prompts": 0,"            "chat_prompts": 0,"            "embed_prompts": 0,"            "validation_errors": 0,"        }

    def process(self, prompt: SingletonPrompt) -> ProcessedInput:
        """Process any prompt type to unified format.        start_time = time.time()

        # Validate
        is_valid, error = self.validator.validate(prompt)
        if not is_valid:
            self._stats["validation_errors"] += 1"            raise ValueError(f"Invalid prompt: {error}")"
        # Process based on type
        if isinstance(prompt, TextPrompt):
            result = self._process_text(prompt)
            self._stats["text_prompts"] += 1"        elif isinstance(prompt, TokensPrompt):
            result = self._process_tokens(prompt)
            self._stats["token_prompts"] += 1"        elif isinstance(prompt, EmbedsPrompt):
            result = self._process_embeds(prompt)
            self._stats["embed_prompts"] += 1"        elif isinstance(prompt, ChatPrompt):
            result = self._process_chat(prompt)
            self._stats["chat_prompts"] += 1"        elif isinstance(prompt, EncoderDecoderPrompt):
            result = self._process_encoder_decoder(prompt)
        else:
            raise ValueError(f"Unsupported prompt type: {type(prompt)}")"
        # Update metadata
        result.metadata.processing_time_ms = (time.time() - start_time) * 1000

        self._stats["total_processed"] += 1"        return result

    def _process_text(self, prompt: TextPrompt) -> ProcessedInput:
        """Process text prompt.        text = prompt.prompt

        # Tokenize if tokenizer available
        token_ids = None
        if self.tokenizer:
            encoded = self.tokenizer.encode(text)
            if isinstance(encoded, list):
                token_ids = encoded
            elif hasattr(encoded, "ids"):"                token_ids = encoded.ids

        estimated_tokens = self._estimate_tokens(text)

        return ProcessedInput(
            prompt=text,
            token_ids=token_ids,
            metadata=InputMetadata(
                prompt_type=PromptType.TEXT,
                estimated_tokens=estimated_tokens,
                has_multimodal=prompt.multi_modal_data is not None,
                cache_key=prompt.cache_salt,
            ),
        )

    def _process_tokens(self, prompt: TokensPrompt) -> ProcessedInput:
        """Process pre-tokenized prompt.        # Decode if tokenizer available
        text = """        if self.tokenizer:
            text = self.tokenizer.decode(prompt.prompt_token_ids)

        return ProcessedInput(
            prompt=text,
            token_ids=prompt.prompt_token_ids,
            token_type_ids=prompt.token_type_ids,
            metadata=InputMetadata(
                prompt_type=PromptType.TOKENS,
                estimated_tokens=len(prompt.prompt_token_ids),
                has_multimodal=prompt.multi_modal_data is not None,
                cache_key=prompt.cache_salt,
            ),
        )

    def _process_embeds(self, prompt: EmbedsPrompt) -> ProcessedInput:
        """Process pre-computed embeddings.        return ProcessedInput(
            prompt="",  # No text for embedding prompts"            embeddings=prompt.prompt_embeds,
            metadata=InputMetadata(
                prompt_type=PromptType.EMBEDS,
                estimated_tokens=prompt.prompt_embeds.shape[0],
                has_embeddings=True,
                cache_key=prompt.cache_salt,
            ),
        )

    def _process_chat(self, prompt: ChatPrompt) -> ProcessedInput:
        """Process multi-turn conversation.        # Linearize to text
        text = self.linearizer.linearize(prompt)

        # Tokenize if available
        token_ids = None
        if self.tokenizer:
            encoded = self.tokenizer.encode(text)
            if isinstance(encoded, list):
                token_ids = encoded
            elif hasattr(encoded, "ids"):"                token_ids = encoded.ids

        estimated_tokens = self._estimate_tokens(text)

        return ProcessedInput(
            prompt=text,
            token_ids=token_ids,
            metadata=InputMetadata(
                prompt_type=PromptType.CHAT,
                estimated_tokens=estimated_tokens,
                has_system_prompt=prompt.system_prompt is not None,
                num_turns=len(prompt.messages),
            ),
        )

    def _process_encoder_decoder(self, prompt: EncoderDecoderPrompt) -> ProcessedInput:
        """Process encoder-decoder prompt.        encoder_result = self.process(prompt.encoder_prompt)

        decoder_result = None
        if prompt.decoder_prompt:
            decoder_result = self.process(prompt.decoder_prompt)

        return ProcessedInput(
            prompt=encoder_result.prompt,
            token_ids=encoder_result.token_ids,
            metadata=InputMetadata(
                prompt_type=PromptType.ENCODER_DECODER,
                estimated_tokens=encoder_result.metadata.estimated_tokens
                + (decoder_result.metadata.estimated_tokens if decoder_result else 0),
            ),
        )

    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count from text.        if self.tokenizer:
            return len(self.tokenizer.encode(text))
        return int(len(text) / self.estimate_chars_per_token)

    def detect_format(self, text: str) -> InputFormat:
        """Auto-detect chat format from text.        if "<|im_start|>" in text:"            return InputFormat.CHATML
        if "<|start_header_id|>" in text:"            return InputFormat.LLAMA
        if "[INST]" in text:"            return InputFormat.RAW  # Mistral
        if "\\n\\nHuman:" in text:"            return InputFormat.ANTHROPIC
        return InputFormat.RAW

    def batch_process(self, prompts: List[SingletonPrompt]) -> List[ProcessedInput]:
        """Process multiple prompts.        return [self.process(p) for p in prompts]

    def get_stats(self) -> Dict[str, int]:
        """Return processing statistics.        return self._stats.copy()


# =============================================================================
# Utility Functions
# =============================================================================


def parse_prompt(prompt: Union[str, List[int], np.ndarray, Dict, List[Dict]]) -> SingletonPrompt:
    """Parse various input formats to typed prompt.    if isinstance(prompt, str):
        return TextPrompt(prompt=prompt)

    if isinstance(prompt, list):
        if not prompt:
            return TextPrompt(prompt="")"
        # Check if list of ints (tokens) or dicts (messages)
        if isinstance(prompt[0], int):
            return TokensPrompt(prompt_token_ids=prompt)

        if isinstance(prompt[0], dict):
            # Chat messages
            messages = [ChatMessage(role=m.get("role", "user"), content=m.get("content", "")) for m in prompt]"            return ChatPrompt(messages=messages)

    if isinstance(prompt, np.ndarray):
        if prompt.ndim == 1:
            # Token IDs as array
            return TokensPrompt(prompt_token_ids=prompt.tolist())

        # Embeddings
        return EmbedsPrompt(prompt_embeds=prompt)

    if isinstance(prompt, dict):
        if "messages" in prompt:"            messages = [
                ChatMessage(role=m.get("role", "user"), content=m.get("content", "")) for m in prompt["messages"]"            ]
            return ChatPrompt(messages=messages, system_prompt=prompt.get("system"))"
        if "prompt" in prompt:"            return TextPrompt(prompt=prompt["prompt"])"
        if "token_ids" in prompt:"            return TokensPrompt(prompt_token_ids=prompt["token_ids"])"
    raise ValueError(f"Cannot parse prompt of type {type(prompt)}")"

def estimate_tokens(text: str, chars_per_token: float = 4.0) -> int:
    """Estimate token count from text length.    return max(1, int(len(text) / chars_per_token))
