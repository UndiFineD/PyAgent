# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Utility functions and loaders for prompt rendering.
"""

from __future__ import annotations

import base64
from typing import Any, Dict, List, Optional, Tuple

from .models import (
    EmbeddingInput,
    PromptConfig,
    RenderResult,
    TruncationResult,
    TruncationStrategy,
)
from .salt import CacheSaltGenerator
from .truncation import TruncationManager


class EmbeddingLoader:
    """Load embeddings from various formats."""

    ENCODINGS = {
        "float32": ("f", 4),
        "float16": ("e", 2),
        "bfloat16": ("e", 2),
        "int8": ("b", 1),
    }

    @classmethod
    def load_base64(cls, data: str, encoding: str = "float32") -> EmbeddingInput:
        """Load embeddings from base64 encoded data."""
        import struct

        if encoding not in cls.ENCODINGS:
            raise ValueError(f"Unknown encoding: {encoding}")

        format_char, byte_size = cls.ENCODINGS[encoding]
        decoded = base64.b64decode(data)
        num_floats = len(decoded) // byte_size
        values = struct.unpack(f"{num_floats}{format_char}", decoded)

        dim = int(len(values) ** 0.5)
        if dim * dim != len(values):
            return EmbeddingInput(embeddings=[list(values)])

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


def render_prompt(
    prompt: Optional[str] = None,
    messages: Optional[List[Dict[str, Any]]] = None,
    tokenizer: Optional[Any] = None,
    max_tokens: Optional[int] = None,
    truncation: TruncationStrategy = TruncationStrategy.AUTO,
    chat_template: Optional[str] = None,
    **kwargs,
) -> RenderResult:
    """Render a prompt with automatic mode detection."""
    from .renderers import ChatRenderer, CompletionRenderer

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
    """Apply chat template to messages."""
    if tokenizer is not None and hasattr(tokenizer, "apply_chat_template"):
        try:
            return tokenizer.apply_chat_template(
                messages,
                add_generation_prompt=add_generation_prompt,
                tokenize=False,
            )
        except Exception:
            pass

    from .renderers import ChatRenderer
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
    """Truncate token sequence."""
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


def _try_rust_render_template(
    template: str,
    messages: List[Dict[str, Any]],
    add_generation_prompt: bool,
) -> Optional[str]:
    """Try Rust-accelerated template rendering."""
    try:
        from rust_core import render_chat_template_rust
        return render_chat_template_rust(template, messages, add_generation_prompt)
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
