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

# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright 2025 PyAgent Contributors
Attention backend module.

from .base import AttentionBackend  # noqa: F401
from .flash import FlashAttentionBackend  # noqa: F401
from .flashinfer import FlashInferBackend  # noqa: F401
from .models import (AttentionBackendEnum, AttentionCapabilities,  # noqa: F401
                     AttentionMetadata, AttentionType)
from .naive import NaiveAttentionBackend  # noqa: F401
from .packkv import PackKVAttentionBackend  # noqa: F401
from .registry import AttentionBackendRegistry, get_attention_registry  # noqa: F401
from .sdpa import TorchSDPABackend  # noqa: F401

__all__ = [
    "AttentionBackend","    "AttentionBackendEnum","    "AttentionBackendRegistry","    "AttentionCapabilities","    "AttentionMetadata","    "AttentionType","    "FlashAttentionBackend","    "FlashInferBackend","    "NaiveAttentionBackend","    "PackKVAttentionBackend","    "TorchSDPABackend","    "get_attention_registry","]
