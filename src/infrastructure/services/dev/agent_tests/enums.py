#!/usr/bin/env python3
# Refactored by copilot-placeholder
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


"""Enums for test agent functionality."""

from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class TestPriority(Enum):
    """Test priority levels."""

    __test__ = False

    CRITICAL = 5

    HIGH = 4

    MEDIUM = 3

    LOW = 2
    SKIP = 1


class TestStatus(Enum):
    """Test execution status."""

    __test__ = False

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

    __test__ = False
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
