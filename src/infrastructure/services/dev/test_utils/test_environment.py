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


"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .CleanupStrategy import CleanupStrategy
from .IsolationLevel import IsolationLevel
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional

__version__ = VERSION

@dataclass
class TestEnvironment:
    __test__ = False
    """Test environment configuration.

    Attributes:
        name: Environment name.
        env_vars: Environment variables.
        temp_dir: Temporary directory.
        isolation_level: File system isolation.
        cleanup: Cleanup strategy.
    """

    name: str
    env_vars: dict[str, str] = field(default_factory=lambda: {})
    temp_dir: Path | None = None
    isolation_level: IsolationLevel = IsolationLevel.TEMP_DIR
    cleanup: CleanupStrategy = CleanupStrategy.IMMEDIATE