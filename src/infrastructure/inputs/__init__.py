# Copyright (c) 2026 PyAgent Authors. All rights reserved.
# Phase 40: Input Processing Package

"""
Input Processing for unified prompt handling.

This package provides:
- Type-safe prompt schemas (text, tokens, embeddings)
- Encoder-decoder prompt separation
- Multi-turn conversation linearization
- Input size estimation for scheduling
"""

from .input_preprocessor import (
    # Enums
    PromptType,
    InputFormat,
    
    # Data classes
    TextPrompt,
    TokensPrompt,
    EmbedsPrompt,
    EncoderDecoderPrompt,
    ChatMessage,
    ChatPrompt,
    ProcessedInput,
    InputMetadata,
    
    # Core classes
    PromptTemplate,
    InputPreprocessor,
    PromptValidator,
    ConversationLinearizer,
    
    # Utilities
    parse_prompt,
    estimate_tokens,
)

__all__ = [
    # Enums
    "PromptType",
    "InputFormat",
    
    # Data classes
    "TextPrompt",
    "TokensPrompt",
    "EmbedsPrompt",
    "EncoderDecoderPrompt",
    "ChatMessage",
    "ChatPrompt",
    "ProcessedInput",
    "InputMetadata",
    
    # Core classes
    "PromptTemplate",
    "InputPreprocessor",
    "PromptValidator",
    "ConversationLinearizer",
    
    # Utilities
    "parse_prompt",
    "estimate_tokens",
]
