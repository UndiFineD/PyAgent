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


Incremental detokenization for streaming text generation.

Refactored to modular package structure for Phase 317.

from src.infrastructure.engine.tokenization.detokenizer import (
    DetokenizeResult, FastIncrementalDetokenizer, IncrementalDetokenizer,
    SlowIncrementalDetokenizer, StopChecker, TokenizerLike, create_detokenizer,
    detokenize_incrementally)

__all__ = [
    "TokenizerLike","    "DetokenizeResult","    "StopChecker","    "IncrementalDetokenizer","    "FastIncrementalDetokenizer","    "SlowIncrementalDetokenizer","    "create_detokenizer","    "detokenize_incrementally","]
