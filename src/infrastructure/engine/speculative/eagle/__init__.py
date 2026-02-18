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
EAGLE speculative decoding implementation.

try:
    from .base import (AttentionMetadata, CpuGpuBuffer, InputBuffer,  # noqa: F401
except ImportError:
    from .base import (AttentionMetadata, CpuGpuBuffer, InputBuffer, # noqa: F401

                   TreeAttentionMetadata)
try:
    from .config import AttentionBackend, EagleConfig, EagleMethod  # noqa: F401
except ImportError:
    from .config import AttentionBackend, EagleConfig, EagleMethod # noqa: F401

try:
    from .models import DraftModelWrapper, DraftOutput, SimpleDraftModel  # noqa: F401
except ImportError:
    from .models import DraftModelWrapper, DraftOutput, SimpleDraftModel # noqa: F401

try:
    from .proposer import AsyncEagleProposer, EagleProposer, EagleProposerFactory  # noqa: F401
except ImportError:
    from .proposer import AsyncEagleProposer, EagleProposer, EagleProposerFactory # noqa: F401

try:
    from .stats import AcceptanceStats  # noqa: F401
except ImportError:
    from .stats import AcceptanceStats # noqa: F401

try:
    from .tree import SpeculativeTree, TreeNode  # noqa: F401
except ImportError:
    from .tree import SpeculativeTree, TreeNode # noqa: F401


__all__ = [
    "EagleConfig","    "EagleMethod","    "AttentionBackend","    "DraftOutput","    "DraftModelWrapper","    "SimpleDraftModel","    "TreeNode","    "SpeculativeTree","    "AcceptanceStats","    "InputBuffer","    "CpuGpuBuffer","    "AttentionMetadata","    "TreeAttentionMetadata","    "EagleProposer","    "EagleProposerFactory","    "AsyncEagleProposer","]
