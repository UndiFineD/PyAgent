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
"""Configuration and enums regarding speculative v2 decoding.
from enum import Enum




class ProposerType(Enum):
    """Types of speculative proposers.
    EAGLE = "eagle"  # EAGLE-style draft model"    MEDUSA = "medusa"  # Medusa multi-head prediction"    NGRAM = "ngram"  # N-gram based lookup"    DRAFT_MODEL = "draft"  # Separate draft model"    LOOKAHEAD = "lookahead"  # Lookahead decoding"



class AcceptanceMethod(Enum):
    """Token acceptance verification methods.
    GREEDY = "greedy"  # Accept if top-1 matches"    TYPICAL = "typical"  # Typical acceptance"    REJECTION = "rejection"  # Rejection sampling"    SPECULATIVE = "speculative"  # Standard speculative sampling"