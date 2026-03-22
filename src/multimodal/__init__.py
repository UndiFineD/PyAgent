#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Multimodal package for PyAgent.

Provides data models and a processing pipeline for text, image, audio,
and other media types in a unified format for LLM ingestion.

Exports
-------
- :class:`Modality` — enum of supported modalities
- :class:`MultiModalData` — single content item with metadata
- :class:`MultiModalInputs` — collection of items with context
- :class:`MultiModalProcessor` — pluggable conversion pipeline
"""

from __future__ import annotations

from .models import Modality, MultiModalData, MultiModalInputs
from .processor import MultiModalProcessor

__all__ = [
    "Modality",
    "MultiModalData",
    "MultiModalInputs",
    "MultiModalProcessor",
]


def placeholder() -> bool:
    """Legacy placeholder — kept for compatibility; always returns True."""
    return True

