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
from dataclasses import dataclass
from typing import Any, Optional
from collections.abc import Callable

__version__ = VERSION

@dataclass
class TestFixture:
    __test__ = False
    """A test fixture with setup and teardown.

    Attributes:
        name: Fixture name.
        setup_fn: Setup function.
        teardown_fn: Teardown function.
        scope: Fixture scope (function, class, module, session).
        data: Fixture data.
    """

    name: str
    setup_fn: Callable[[], Any] | None = None
    teardown_fn: Callable[[Any], None] | None = None
    scope: str = "function"
    data: Any = None