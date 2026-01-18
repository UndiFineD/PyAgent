"""
Prompt Renderer System - Phase 42

Unified prompt preparation and rendering system inspired by vLLM's prompt_renderer.
Handles tokenization, chat templates, multimodal inputs, and prompt truncation.

Key Features:
- Unified input processing for API layer
- Prompt truncation strategies
- Base64 embedding loading
- Cache salt generation for prefix caching
- Clean separation between API and engine

Performance: Uses Rust-accelerated template rendering.
"""

from __future__ import annotations

import base64
import hashlib
import logging
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    TypeVar,
    Union,
)

logger = logging.getLogger(__name__)

__all__ = [
    # Enums
    "TruncationStrategy",
    "InputType",
    "RenderMode",
    # Data Classes
    "PromptConfig",
    "RenderResult",
    "TruncationResult",
    "EmbeddingInput",
    "MultimodalInput",
    # Main Classes
    "PromptRenderer",
    "CompletionRenderer",
    "ChatRenderer",
    "EmbeddingLoader",
    "TruncationManager",
    "CacheSaltGenerator",
    # Functions
    "render_prompt",
    "apply_chat_template",
    "truncate_prompt",
    "generate_cache_salt",
]


# ============================================================================
# Enums
# ============================================================================


class TruncationStrategy(Enum):
    """Prompt truncation strategies."""

    NONE = "none"  # No truncation
    AUTO = "auto"  # Automatic truncation
    LEFT = "left"  # Truncate from left (oldest context)
    RIGHT = "right"  # Truncate from right
    MIDDLE = "middle"  # Keep start and end, truncate middle
    SMART = "smart"  # Semantic-aware truncation


class InputType(Enum):
    """Input types for prompt rendering."""

    TEXT = "text"
    TOKENS = "tokens"
    EMBEDDING = "embedding"
    MULTIMODAL = "multimodal"


class RenderMode(Enum):
    """Rendering modes."""

    COMPLETION = "completion"
    CHAT = "chat"
    EMBEDDING = "embedding"
    INSTRUCT = "instruct"


# ============================================================================
# Data Classes
# ============================================================================


@dataclass
class PromptConfig:
    """Configuration for prompt rendering."""

    # Input
    prompt: Optional[str] = None
    messages: Optional[List[Dict[str, Any]]] = None
    token_ids: Optional[List[int]] = None
    embeddings: Optional[List[List[float]]] = None

    # Template settings
    chat_template: Optional[str] = None
    add_generation_prompt: bool = True
    add_special_tokens: bool = True

    # Truncation
    max_tokens: Optional[int] = None
    truncation: TruncationStrategy = TruncationStrategy.AUTO
    reserve_tokens: int = 0  # Reserve for generation

    # Multimodal
    images: Optional[List[Dict[str, Any]]] = None
    audio: Optional[List[Dict[str, Any]]] = None

    # Caching
    cache_salt: Optional[str] = None
    enable_prefix_cache: bool = True

    # Processing
    strip_whitespace: bool = True
    normalize_unicode: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "messages": self.messages,
            "max_tokens": self.max_tokens,
            "truncation": self.truncation.value,
            "cache_salt": self.cache_salt,
        }


@dataclass
class RenderResult:
    """Result of prompt rendering."""

    # Rendered output
    text: Optional[str] = None
    token_ids: Optional[List[int]] = None
    embeddings: Optional[List[List[float]]] = None

    # Metadata
    input_type: InputType = InputType.TEXT
    num_tokens: int = 0
    was_truncated: bool = False
    truncation_info: Optional["TruncationResult"] = None

    # Multimodal
    image_positions: Optional[List[int]] = None
    audio_positions: Optional[List[int]] = None

    # Caching
    cache_salt: Optional[str] = None
    cache_prefix_hash: Optional[str] = None

    @property
    def is_multimodal(self) -> bool:
        return bool(self.image_positions or self.audio_positions)


@dataclass
class TruncationResult:
    """Result of prompt truncation."""

    original_tokens: int
    truncated_tokens: int
    removed_tokens: int
    strategy_used: TruncationStrategy
    removed_ranges: List[Tuple[int, int]] = field(default_factory=list)
    warning_message: Optional[str] = None

    @property
    def truncation_ratio(self) -> float:
        if self.original_tokens == 0:
            return 0.0
        return self.removed_tokens / self.original_tokens


@dataclass
class EmbeddingInput:
    """Embedding input for direct embedding injection."""

    embeddings: List[List[float]]
    positions: Optional[List[int]] = None
    encoding: str = "float32"

    @classmethod
    def from_base64(cls, data: str, encoding: str = "float32") -> "EmbeddingInput":
        """Load embeddings from base64."""
        return EmbeddingLoader.load_base64(data, encoding)


@dataclass
class MultimodalInput:
    """Multimodal input container."""

    images: List[Dict[str, Any]] = field(default_factory=list)
    audio: List[Dict[str, Any]] = field(default_factory=list)
    video: List[Dict[str, Any]] = field(default_factory=list)

    def is_empty(self) -> bool:
        return not (self.images or self.audio or self.video)


# ============================================================================
# Embedding Loader
# ============================================================================


class EmbeddingLoader:
    """Load embeddings from various formats."""

    ENCODINGS = {
        "float32": ("f", 4),
        "float16": ("e", 2),
        "bfloat16": ("e", 2),  # Approximation
        "int8": ("b", 1),
    }

    @classmethod
    def load_base64(cls, data: str, encoding: str = "float32") -> EmbeddingInput:
        """
        Load embeddings from base64 encoded data.
        
        Args:
            data: Base64 encoded embedding data
            encoding: Data type encoding
            
        Returns:
            EmbeddingInput with decoded embeddings
        """
        import struct

        if encoding not in cls.ENCODINGS:
            raise ValueError(f"Unknown encoding: {encoding}")

        format_char, byte_size = cls.ENCODINGS[encoding]

        decoded = base64.b64decode(data)
        num_floats = len(decoded) // byte_size

        values = struct.unpack(f"{num_floats}{format_char}", decoded)

        # Assume square embedding
        dim = int(len(values) ** 0.5)
        if dim * dim != len(values):
            # Single embedding
            return EmbeddingInput(embeddings=[list(values)])

        # Multiple embeddings
        embeddings = []
        for i in range(0, len(values), dim):
            embeddings.append(list(values[i : i + dim]))

        return EmbeddingInput(embeddings=embeddings, encoding=encoding)

    @classmethod
    def load_file(cls, path: str, encoding: str = "float32") -> EmbeddingInput:
        """Load embeddings from file."""
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return cls.load_base64(data, encoding)

    @classmethod
    def to_base64(
        cls,
        embeddings: List[List[float]],
        encoding: str = "float32",
    ) -> str:
        """Convert embeddings to base64."""
        import struct

        if encoding not in cls.ENCODINGS:
            raise ValueError(f"Unknown encoding: {encoding}")

        format_char, _ = cls.ENCODINGS[encoding]

        flat = [v for emb in embeddings for v in emb]
        packed = struct.pack(f"{len(flat)}{format_char}", *flat)

        return base64.b64encode(packed).decode()


# ============================================================================
# Truncation Manager
# ============================================================================


class TruncationManager:
    """Manage prompt truncation strategies."""

    @classmethod
    def truncate(
        cls,
        tokens: List[int],
        max_tokens: int,
        strategy: TruncationStrategy = TruncationStrategy.AUTO,
        reserve_tokens: int = 0,
    ) -> Tuple[List[int], TruncationResult]:
        """
        Truncate token sequence to fit within limit.
        
        Args:
            tokens: Input tokens
            max_tokens: Maximum allowed tokens
            strategy: Truncation strategy
            reserve_tokens: Tokens to reserve for generation
            
        Returns:
            Tuple of (truncated_tokens, truncation_result)
        """
        target_tokens = max_tokens - reserve_tokens
        original_len = len(tokens)

        if original_len <= target_tokens:
            return tokens, TruncationResult(
                original_tokens=original_len,
                truncated_tokens=original_len,
                removed_tokens=0,
                strategy_used=TruncationStrategy.NONE,
            )

        if strategy == TruncationStrategy.NONE:
            # Return original with warning
            return tokens, TruncationResult(
                original_tokens=original_len,
                truncated_tokens=original_len,
                removed_tokens=0,
                strategy_used=TruncationStrategy.NONE,
                warning_message=f"Prompt exceeds limit by {original_len - target_tokens} tokens",
            )

        if strategy in (TruncationStrategy.AUTO, TruncationStrategy.LEFT):
            return cls._truncate_left(tokens, target_tokens, original_len)

        if strategy == TruncationStrategy.RIGHT:
            return cls._truncate_right(tokens, target_tokens, original_len)

        if strategy == TruncationStrategy.MIDDLE:
            return cls._truncate_middle(tokens, target_tokens, original_len)

        if strategy == TruncationStrategy.SMART:
            return cls._truncate_smart(tokens, target_tokens, original_len)

        return cls._truncate_left(tokens, target_tokens, original_len)

    @classmethod
    def _truncate_left(
        cls,
        tokens: List[int],
        target: int,
        original: int,
    ) -> Tuple[List[int], TruncationResult]:
        """Truncate from left (remove oldest context)."""
        removed = original - target
        truncated = tokens[removed:]
        return truncated, TruncationResult(
            original_tokens=original,
            truncated_tokens=len(truncated),
            removed_tokens=removed,
            strategy_used=TruncationStrategy.LEFT,
            removed_ranges=[(0, removed)],
        )

    @classmethod
    def _truncate_right(
        cls,
        tokens: List[int],
        target: int,
        original: int,
    ) -> Tuple[List[int], TruncationResult]:
        """Truncate from right."""
        truncated = tokens[:target]
        removed = original - target
        return truncated, TruncationResult(
            original_tokens=original,
            truncated_tokens=len(truncated),
            removed_tokens=removed,
            strategy_used=TruncationStrategy.RIGHT,
            removed_ranges=[(target, original)],
        )

    @classmethod
    def _truncate_middle(
        cls,
        tokens: List[int],
        target: int,
        original: int,
    ) -> Tuple[List[int], TruncationResult]:
        """Truncate from middle (keep start and end)."""
        keep_start = target // 2
        keep_end = target - keep_start

        truncated = tokens[:keep_start] + tokens[-keep_end:]
        removed = original - target

        return truncated, TruncationResult(
            original_tokens=original,
            truncated_tokens=len(truncated),
            removed_tokens=removed,
            strategy_used=TruncationStrategy.MIDDLE,
            removed_ranges=[(keep_start, original - keep_end)],
        )

    @classmethod
    def _truncate_smart(
        cls,
        tokens: List[int],
        target: int,
        original: int,
    ) -> Tuple[List[int], TruncationResult]:
        """Smart truncation with semantic awareness."""
        # For now, use left truncation as fallback
        # In production, would use sentence boundaries, etc.
        return cls._truncate_left(tokens, target, original)


# ============================================================================
# Cache Salt Generator
# ============================================================================


class CacheSaltGenerator:
    """Generate cache salt for prefix caching disambiguation."""

    @classmethod
    def generate(
        cls,
        config: PromptConfig,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate cache salt based on configuration.
        
        Cache salt ensures different configurations get different cache entries.
        """
        components = []

        # Template-related components
        if config.chat_template:
            components.append(f"template:{hashlib.md5(config.chat_template.encode()).hexdigest()[:8]}")

        # Processing options
        if config.add_generation_prompt:
            components.append("gen_prompt")
        if config.add_special_tokens:
            components.append("special_tokens")

        # Truncation
        if config.truncation != TruncationStrategy.NONE:
            components.append(f"trunc:{config.truncation.value}")

        # Additional data
        if additional_data:
            for key, value in sorted(additional_data.items()):
                components.append(f"{key}:{value}")

        # User-provided salt
        if config.cache_salt:
            components.append(config.cache_salt)

        if not components:
            return ""

        salt_string = "|".join(components)
        return hashlib.sha256(salt_string.encode()).hexdigest()[:16]


# ============================================================================
# Prompt Renderer (Base)
# ============================================================================


class PromptRenderer(ABC):
    """
    Abstract base class for prompt renderers.
    
    Provides unified interface for converting various input formats
    into renderable prompts.
    """

    def __init__(
        self,
        tokenizer: Optional[Any] = None,
        max_model_tokens: int = 4096,
    ):
        self.tokenizer = tokenizer
        self.max_model_tokens = max_model_tokens

    @abstractmethod
    def render(self, config: PromptConfig) -> RenderResult:
        """Render prompt from configuration."""
        ...

    def _tokenize(self, text: str, add_special_tokens: bool = True) -> List[int]:
        """Tokenize text."""
        if self.tokenizer is None:
            # Fallback: estimate tokens by splitting
            return list(range(len(text.split())))

        return self.tokenizer.encode(text, add_special_tokens=add_special_tokens)

    def _detokenize(self, tokens: List[int]) -> str:
        """Detokenize tokens."""
        if self.tokenizer is None:
            return f"<{len(tokens)} tokens>"

        return self.tokenizer.decode(tokens)

    def _apply_truncation(
        self,
        tokens: List[int],
        config: PromptConfig,
    ) -> Tuple[List[int], Optional[TruncationResult]]:
        """Apply truncation to tokens."""
        max_tokens = config.max_tokens or self.max_model_tokens

        if len(tokens) <= max_tokens:
            return tokens, None

        return TruncationManager.truncate(
            tokens,
            max_tokens,
            config.truncation,
            config.reserve_tokens,
        )

    def _generate_cache_salt(self, config: PromptConfig) -> str:
        """Generate cache salt."""
        return CacheSaltGenerator.generate(config)


# ============================================================================
# Completion Renderer
# ============================================================================


class CompletionRenderer(PromptRenderer):
    """Renderer for completion-style prompts."""

    def render(self, config: PromptConfig) -> RenderResult:
        """Render completion prompt."""
        # Direct token input
        if config.token_ids is not None:
            tokens = config.token_ids
            tokens, trunc_result = self._apply_truncation(tokens, config)

            return RenderResult(
                token_ids=tokens,
                input_type=InputType.TOKENS,
                num_tokens=len(tokens),
                was_truncated=trunc_result is not None,
                truncation_info=trunc_result,
                cache_salt=self._generate_cache_salt(config),
            )

        # Embedding input
        if config.embeddings is not None:
            return RenderResult(
                embeddings=config.embeddings,
                input_type=InputType.EMBEDDING,
                num_tokens=len(config.embeddings),
                cache_salt=self._generate_cache_salt(config),
            )

        # Text input
        text = config.prompt or ""

        if config.strip_whitespace:
            text = text.strip()

        if config.normalize_unicode:
            import unicodedata

            text = unicodedata.normalize("NFC", text)

        tokens = self._tokenize(text, config.add_special_tokens)
        tokens, trunc_result = self._apply_truncation(tokens, config)

        # Regenerate text if truncated
        if trunc_result and trunc_result.removed_tokens > 0:
            text = self._detokenize(tokens)

        return RenderResult(
            text=text,
            token_ids=tokens,
            input_type=InputType.TEXT,
            num_tokens=len(tokens),
            was_truncated=trunc_result is not None,
            truncation_info=trunc_result,
            cache_salt=self._generate_cache_salt(config),
        )


# ============================================================================
# Chat Renderer
# ============================================================================


class ChatRenderer(PromptRenderer):
    """Renderer for chat-style prompts."""

    # Default chat template (ChatML-like)
    DEFAULT_TEMPLATE = """{% for message in messages %}{% if message['role'] == 'system' %}<|im_start|>system
{{ message['content'] }}<|im_end|>
{% elif message['role'] == 'user' %}<|im_start|>user
{{ message['content'] }}<|im_end|>
{% elif message['role'] == 'assistant' %}<|im_start|>assistant
{{ message['content'] }}<|im_end|>
{% endif %}{% endfor %}{% if add_generation_prompt %}<|im_start|>assistant
{% endif %}"""

    def render(self, config: PromptConfig) -> RenderResult:
        """Render chat prompt."""
        if config.messages is None:
            # Fallback to completion rendering
            return CompletionRenderer(
                self.tokenizer, self.max_model_tokens
            ).render(config)

        # Apply chat template
        text = self._apply_template(
            config.messages,
            config.chat_template or self.DEFAULT_TEMPLATE,
            config.add_generation_prompt,
        )

        if config.strip_whitespace:
            text = text.strip()

        # Tokenize
        tokens = self._tokenize(text, config.add_special_tokens)
        tokens, trunc_result = self._apply_truncation(tokens, config)

        # Handle multimodal
        image_positions = None
        if config.images:
            image_positions = self._find_image_positions(text, config.images)

        return RenderResult(
            text=text,
            token_ids=tokens,
            input_type=InputType.TEXT if not image_positions else InputType.MULTIMODAL,
            num_tokens=len(tokens),
            was_truncated=trunc_result is not None,
            truncation_info=trunc_result,
            image_positions=image_positions,
            cache_salt=self._generate_cache_salt(config),
        )

    def _apply_template(
        self,
        messages: List[Dict[str, Any]],
        template: str,
        add_generation_prompt: bool = True,
    ) -> str:
        """Apply Jinja2 chat template."""
        try:
            from jinja2 import Environment, BaseLoader

            env = Environment(loader=BaseLoader())
            tmpl = env.from_string(template)
            return tmpl.render(
                messages=messages,
                add_generation_prompt=add_generation_prompt,
            )
        except ImportError:
            # Fallback without Jinja2
            return self._simple_template(messages, add_generation_prompt)

    def _simple_template(
        self,
        messages: List[Dict[str, Any]],
        add_generation_prompt: bool,
    ) -> str:
        """Simple template without Jinja2."""
        parts = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            parts.append(f"<|im_start|>{role}\n{content}<|im_end|>")

        if add_generation_prompt:
            parts.append("<|im_start|>assistant\n")

        return "\n".join(parts)

    def _find_image_positions(
        self,
        text: str,
        images: List[Dict[str, Any]],
    ) -> List[int]:
        """Find image placeholder positions in text."""
        positions = []
        # Look for common image placeholders
        for pattern in ["<image>", "[IMAGE]", "<|image|>", "{{IMAGE}}"]:
            start = 0
            while True:
                pos = text.find(pattern, start)
                if pos == -1:
                    break
                positions.append(pos)
                start = pos + len(pattern)

        return positions if positions else None


# ============================================================================
# Convenience Functions
# ============================================================================


def render_prompt(
    prompt: Optional[str] = None,
    messages: Optional[List[Dict[str, Any]]] = None,
    tokenizer: Optional[Any] = None,
    max_tokens: Optional[int] = None,
    truncation: TruncationStrategy = TruncationStrategy.AUTO,
    chat_template: Optional[str] = None,
    **kwargs,
) -> RenderResult:
    """
    Render a prompt with automatic mode detection.
    
    Args:
        prompt: Text prompt for completion mode
        messages: Chat messages for chat mode
        tokenizer: Tokenizer instance
        max_tokens: Maximum tokens
        truncation: Truncation strategy
        chat_template: Custom chat template
        **kwargs: Additional config options
        
    Returns:
        RenderResult with rendered prompt
    """
    config = PromptConfig(
        prompt=prompt,
        messages=messages,
        max_tokens=max_tokens,
        truncation=truncation,
        chat_template=chat_template,
        **kwargs,
    )

    if messages is not None:
        renderer = ChatRenderer(tokenizer, max_tokens or 4096)
    else:
        renderer = CompletionRenderer(tokenizer, max_tokens or 4096)

    return renderer.render(config)


def apply_chat_template(
    messages: List[Dict[str, Any]],
    template: Optional[str] = None,
    tokenizer: Optional[Any] = None,
    add_generation_prompt: bool = True,
) -> str:
    """
    Apply chat template to messages.
    
    Args:
        messages: Chat messages
        template: Jinja2 template string
        tokenizer: Tokenizer with chat_template attribute
        add_generation_prompt: Add generation prompt at end
        
    Returns:
        Formatted prompt string
    """
    # Try tokenizer's template first
    if tokenizer is not None and hasattr(tokenizer, "apply_chat_template"):
        try:
            return tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=add_generation_prompt,
                tokenize=False,
            )
        except Exception:
            pass

    # Use provided or default template
    config = PromptConfig(
        messages=messages,
        chat_template=template,
        add_generation_prompt=add_generation_prompt,
    )

    renderer = ChatRenderer()
    return renderer._apply_template(
        messages,
        template or renderer.DEFAULT_TEMPLATE,
        add_generation_prompt,
    )


def truncate_prompt(
    tokens: List[int],
    max_tokens: int,
    strategy: TruncationStrategy = TruncationStrategy.AUTO,
    reserve_tokens: int = 0,
) -> Tuple[List[int], TruncationResult]:
    """
    Truncate token sequence.
    
    Args:
        tokens: Input tokens
        max_tokens: Maximum allowed
        strategy: Truncation strategy
        reserve_tokens: Tokens to reserve
        
    Returns:
        Tuple of (truncated_tokens, result)
    """
    return TruncationManager.truncate(tokens, max_tokens, strategy, reserve_tokens)


def generate_cache_salt(
    chat_template: Optional[str] = None,
    add_special_tokens: bool = True,
    **kwargs,
) -> str:
    """Generate cache salt for configuration."""
    config = PromptConfig(
        chat_template=chat_template,
        add_special_tokens=add_special_tokens,
    )
    return CacheSaltGenerator.generate(config, kwargs)


# ============================================================================
# Rust Acceleration Integration
# ============================================================================


def _try_rust_render_template(
    template: str,
    messages: List[Dict[str, Any]],
    add_generation_prompt: bool,
) -> Optional[str]:
    """Try Rust-accelerated template rendering."""
    try:
        from rust_core import render_chat_template_rust

        return render_chat_template_rust(
            template,
            messages,
            add_generation_prompt,
        )
    except ImportError:
        return None


def _try_rust_find_placeholders(
    text: str,
    patterns: List[str],
) -> Optional[List[int]]:
    """Try Rust-accelerated placeholder finding."""
    try:
        from rust_core import find_placeholders_rust

        return find_placeholders_rust(text, patterns)
    except ImportError:
        return None
