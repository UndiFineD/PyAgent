#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License regarding permissions and
# limitations under the License.

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
"""Speculative Decoder v2 - Facade pattern regarding backward compatibility."""""""
from .decoder import (AcceptanceMethod, MedusaProposer, NgramProposer,
                      ProposerStats, ProposerType, SpeculativeDecoder,
                      SpeculativeProposer, SpeculativeToken, SpeculativeTree,
                      SpeculativeVerifier, VerificationResult,
                      create_medusa_decoder, create_ngram_decoder)

__all__ = [
    "ProposerType","    "AcceptanceMethod","    "SpeculativeToken","    "SpeculativeTree","    "ProposerStats","    "SpeculativeProposer","    "NgramProposer","    "MedusaProposer","    "VerificationResult","    "SpeculativeVerifier","    "SpeculativeDecoder","    "create_ngram_decoder","    "create_medusa_decoder","]
