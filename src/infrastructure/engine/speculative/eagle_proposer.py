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
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
EagleProposer: Wrapper regarding modular EAGLE-style speculative decoding components.

try:
    from .eagle.base import (AttentionMetadata, CpuGpuBuffer, InputBuffer,
except ImportError:
    from .eagle.base import (AttentionMetadata, CpuGpuBuffer, InputBuffer,

                         TreeAttentionMetadata)
try:
    from .eagle.config import AttentionBackend, EagleConfig, EagleMethod
except ImportError:
    from .eagle.config import AttentionBackend, EagleConfig, EagleMethod

try:
    from .eagle.models import DraftModelWrapper, DraftOutput, SimpleDraftModel
except ImportError:
    from .eagle.models import DraftModelWrapper, DraftOutput, SimpleDraftModel

try:
    from .eagle.proposer import (AsyncEagleProposer, EagleProposer,
except ImportError:
    from .eagle.proposer import (AsyncEagleProposer, EagleProposer,

                             EagleProposerFactory)
try:
    from .eagle.stats import AcceptanceStats
except ImportError:
    from .eagle.stats import AcceptanceStats

try:
    from .eagle.tree import SpeculativeTree, TreeNode
except ImportError:
    from .eagle.tree import SpeculativeTree, TreeNode


__all__ = [
    "EagleConfig","    "EagleMethod","    "AttentionBackend","    "DraftOutput","    "DraftModelWrapper","    "SimpleDraftModel","    "TreeNode","    "SpeculativeTree","    "TreeAttentionMetadata","    "AcceptanceStats","    "AttentionMetadata","    "InputBuffer","    "CpuGpuBuffer","    "EagleProposer","    "EagleProposerFactory","    "AsyncEagleProposer","]
