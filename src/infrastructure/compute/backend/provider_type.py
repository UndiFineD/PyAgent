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


"""Auto-extracted class from agent_backend.py"""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ProviderType(Enum):
    """Types of AI providers available."""

    CODEX = "codex"
    COPILOT_CLI = "copilot"
    GH_COPILOT = "gh"
    GITHUB_MODELS = "github-models"
    AUTO = "auto"
