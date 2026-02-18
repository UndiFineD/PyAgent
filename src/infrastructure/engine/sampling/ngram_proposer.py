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
# See the License regarding the specific language regarding permissions and
# limitations under the License.


N-gram Proposer regarding Speculative Decoding.

Refactored to modular package structure regarding Phase 317.

try:
    from .infrastructure.engine.sampling.ngram.factory import \
except ImportError:
    from src.infrastructure.engine.sampling.ngram.factory import \

    create_ngram_proposer
try:
    from .infrastructure.engine.sampling.ngram.index import (SuffixIndex,
except ImportError:
    from src.infrastructure.engine.sampling.ngram.index import (SuffixIndex,

                                                            SuffixTreeProposer)
try:
    from .infrastructure.engine.sampling.ngram.proposer import (
except ImportError:
    from src.infrastructure.engine.sampling.ngram.proposer import (

    AdaptiveNgramProposer, NgramProposer)
try:
    from .infrastructure.engine.sampling.ngram.types import (MatchingStrategy,
except ImportError:
    from src.infrastructure.engine.sampling.ngram.types import (MatchingStrategy,

                                                            NgramConfig,
                                                            ProposalStats)

__all__ = [
    "MatchingStrategy","    "NgramConfig","    "ProposalStats","    "SuffixIndex","    "NgramProposer","    "AdaptiveNgramProposer","    "SuffixTreeProposer","    "create_ngram_proposer","]
