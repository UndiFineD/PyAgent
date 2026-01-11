#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from .CleanupStrategy import CleanupStrategy
from .IsolationLevel import IsolationLevel

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Optional

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
    env_vars: Dict[str, str] = field(default_factory=lambda: {})
    temp_dir: Optional[Path] = None
    isolation_level: IsolationLevel = IsolationLevel.TEMP_DIR
    cleanup: CleanupStrategy = CleanupStrategy.IMMEDIATE
