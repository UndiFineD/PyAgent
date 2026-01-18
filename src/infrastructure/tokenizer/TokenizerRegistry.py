# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""
Facade for Tokenizer Registry.
Delegates to modularized sub-packages in src/infrastructure/tokenizer/.
"""

from .models import (
    TokenizerBackend as TokenizerBackend,
    SpecialTokenHandling as SpecialTokenHandling,
    TruncationStrategy as TruncationStrategy,
    PaddingStrategy as PaddingStrategy,
    TokenizerConfig as TokenizerConfig,
    TokenizerInfo as TokenizerInfo,
    TokenizeResult as TokenizeResult,
    BatchTokenizeResult as BatchTokenizeResult,
)
from .protocol import TokenizerProtocol as TokenizerProtocol
from .base import BaseTokenizer as BaseTokenizer
from .huggingface import HuggingFaceTokenizer as HuggingFaceTokenizer
from .tiktoken import TiktokenTokenizer as TiktokenTokenizer
from .mistral import MistralTokenizer as MistralTokenizer
from .registry import TokenizerRegistry as TokenizerRegistry
from .pool import TokenizerPool as TokenizerPool
from .utils import (
    get_tokenizer as get_tokenizer,
    create_tokenizer as create_tokenizer,
    estimate_token_count as estimate_token_count,
    detect_tokenizer_backend as detect_tokenizer_backend,
)
