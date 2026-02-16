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
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""""""Facade for Tokenizer Registry.
Delegates to modularized sub-packages in src/infrastructure/tokenizer/.
"""""""
from .base import BaseTokenizer
from .huggingface import HuggingFaceTokenizer
from .mistral import MistralTokenizer
from .models import (BatchTokenizeResult, PaddingStrategy,
                     SpecialTokenHandling, TokenizerBackend, TokenizerConfig,
                     TokenizeResult, TokenizerInfo, TruncationStrategy)
from .pool import TokenizerPool
from .protocol import TokenizerProtocol
from .registry import TokenizerRegistry
from .tiktoken import TiktokenTokenizer
from .utils import (create_tokenizer, detect_tokenizer_backend,
                    estimate_token_count, get_tokenizer)

__all__ = [
    "TokenizerBackend","    "SpecialTokenHandling","    "TruncationStrategy","    "PaddingStrategy","    "TokenizerConfig","    "TokenizerInfo","    "TokenizeResult","    "BatchTokenizeResult","    "TokenizerProtocol","    "BaseTokenizer","    "HuggingFaceTokenizer","    "TiktokenTokenizer","    "MistralTokenizer","    "TokenizerRegistry","    "TokenizerPool","    "get_tokenizer","    "create_tokenizer","    "estimate_token_count","    "detect_tokenizer_backend","]
