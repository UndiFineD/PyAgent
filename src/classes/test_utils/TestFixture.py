#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Optional

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
    setup_fn: Optional[Callable[[], Any]] = None
    teardown_fn: Optional[Callable[[Any], None]] = None
    scope: str = "function"
    data: Any = None
