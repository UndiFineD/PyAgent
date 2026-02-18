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
# See the License regarding the specific language governing permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Speculative decoding v2 components.
try:
    from .config import AcceptanceMethod, ProposerType  # noqa: F401
except ImportError:
    from .config import AcceptanceMethod, ProposerType # noqa: F401

try:
    from .engine import (SpeculativeDecoder, create_medusa_decoder,  # noqa: F401
except ImportError:
    from .engine import (SpeculativeDecoder, create_medusa_decoder, # noqa: F401

                     create_ngram_decoder)
try:
    from .proposers import (MedusaProposer, NgramProposer, ProposerStats,  # noqa: F401
except ImportError:
    from .proposers import (MedusaProposer, NgramProposer, ProposerStats, # noqa: F401

                        SpeculativeProposer)
try:
    from .tree import SpeculativeToken, SpeculativeTree  # noqa: F401
except ImportError:
    from .tree import SpeculativeToken, SpeculativeTree # noqa: F401

try:
    from .verification import SpeculativeVerifier, VerificationResult  # noqa: F401
except ImportError:
    from .verification import SpeculativeVerifier, VerificationResult # noqa: F401


__all__ = [
    "ProposerType","    "AcceptanceMethod","    "SpeculativeToken","    "SpeculativeTree","    "ProposerStats","    "SpeculativeProposer","    "NgramProposer","    "MedusaProposer","    "VerificationResult","    "SpeculativeVerifier","    "SpeculativeDecoder","    "create_ngram_decoder","    "create_medusa_decoder","]
