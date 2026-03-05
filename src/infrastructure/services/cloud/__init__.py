#!/usr/bin/env python3
from __future__ import annotations
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
"""
Cloud Infrastructure Module shim.

Lightweight shim that exposes a few names lazily for tests. Avoids heavy
imports during pytest collection.
"""


from typing import TYPE_CHECKING, Any

__all__: list[str] = []


def __getattr__(name: str) -> Any:
    if name in ("CloudProviderBase", "InferenceRequest", "InferenceResponse"):
        from .base import CloudProviderBase, InferenceRequest, InferenceResponse

        return {"CloudProviderBase": CloudProviderBase, "InferenceRequest": InferenceRequest, "InferenceResponse": InferenceResponse}[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if TYPE_CHECKING:
    from .base import CloudProviderBase, InferenceRequest, InferenceResponse

