#!/usr/bin/env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");

"""Enums for test agent functionality."""

from enum import Enum


class TestPriority(Enum):
    """Test priority levels."""
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    SKIP = 1


class TestStatus(Enum):
    """Test execution status."""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    FLAKY = "flaky"


class CoverageType(Enum):
    """Types of coverage to track."""
    LINE = "line"
    BRANCH = "branch"
    FUNCTION = "function"
    CLASS = "class"


class BrowserType(Enum):
    """Browser types for cross-browser testing."""
    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"
    EDGE = "edge"
    IE = "ie"


class TestSourceType(Enum):
    """Types of test result sources for aggregation."""
    PYTEST = "pytest"
    UNITTEST = "unittest"
    JEST = "jest"
    MOCHA = "mocha"
    JUNIT = "junit"


class MutationOperator(Enum):
    """Mutation operators for mutation testing."""
    ARITHMETIC = "arithmetic"
    RELATIONAL = "relational"
    LOGICAL = "logical"
    ASSIGNMENT = "assignment"
    RETURN_VALUE = "return_value"


class ExecutionMode(Enum):
    """Test execution replay modes."""
    STEP_BY_STEP = "step_by_step"
    FULL_REPLAY = "full_replay"
    BREAKPOINT = "breakpoint"
