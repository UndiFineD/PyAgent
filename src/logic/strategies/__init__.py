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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Auto-generated module exports."""

from __future__ import annotations
from src.core.base.version import VERSION as VERSION
from typing import Optional, List, Dict
from collections.abc import Callable
from .AgentStrategy import AgentStrategy as AgentStrategy
from .ChainOfThoughtStrategy import ChainOfThoughtStrategy as ChainOfThoughtStrategy
from .DirectStrategy import DirectStrategy as DirectStrategy
from .ReflexionStrategy import ReflexionStrategy as ReflexionStrategy

# Type alias for the backend function signature
# (prompt, system_prompt, history) -> response
BackendFunction = Callable[[str, str | None, list[dict[str, str]] | None], str]

__version__ = VERSION
