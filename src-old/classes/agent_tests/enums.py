#!/usr/bin/env python3
"""Shim for agent_tests.enums expected under src.classes.agent_tests."""

from enum import Enum


class CoverageType(Enum):
    """Types of test coverage."""
    UNIT = "unit"
    INTEGRATION = "integration"


class BrowserType(Enum):
    """Supported browsers for web testing."""
    CHROME = "chrome"
    FIREFOX = "firefox"


class TestPriority(Enum):
    """Test priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TestStatus(Enum):
    """Possible test outcomes."""
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"


class TestSourceType(Enum):
    """Origin of test cases."""
    UNIT = "unit"
    AUTO_GENERATED = "auto"
    MANUAL = "manual"


class MutationOperator(Enum):
    """Types of mutation operators for mutation testing."""
    AOR = "arithmetic"
    ROR = "relational"
    LCR = "logical"


class ExecutionMode(Enum):
    """Modes of test execution."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"


__all__ = [
    "CoverageType", "BrowserType", "TestPriority", "TestStatus",
    "TestSourceType", "MutationOperator", "ExecutionMode"
]

try:
    from src.infrastructure.services.dev.agent_tests.enums import (
        CoverageType, BrowserType, TestPriority, TestStatus,
        TestSourceType, MutationOperator, ExecutionMode
    )
except Exception:
    # Minimal placeholders if infra module not available
    pass
