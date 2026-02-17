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


"""Extension Registry Package - Phase 20
=====================================

Plugin system for managing extensible component registries.
"""
from .extension_registry import (ExtensionInfo, ExtensionManager,  # noqa: F401
                                 GlobalRegistry, LazyExtensionManager,
                                 MultiExtensionManager, TypedExtensionManager,
                                 create_lazy_registry, create_multi_registry,
                                 create_registry, create_typed_registry,
                                 get_global_registry)

__all__ = [
    "ExtensionManager","    "TypedExtensionManager","    "MultiExtensionManager","    "LazyExtensionManager","    "ExtensionInfo","    "GlobalRegistry","    "create_registry","    "create_typed_registry","    "create_multi_registry","    "create_lazy_registry","    "get_global_registry","]

