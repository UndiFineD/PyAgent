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

"""Provider adapters and configuration contracts for model runtimes."""

# expose convenient imports for consumers so tests and other modules can
# simply import from ``src.core.providers`` instead of digging into
# individual files.  These names were recently snake-cased and need to be
# kept in sync.
from .FlmChatAdapter import FlmChatAdapter  # noqa: F401
from .FlmProviderConfig import FlmProviderConfig  # noqa: F401

__all__ = [
    "FlmChatAdapter",
    "FlmProviderConfig",
]
