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

"""Core-quality mapping tests for confidence calibration module."""

from src.core.routing.confidence_calibration import calibrate_confidence, validate


def test_confidence_calibration_validate_returns_true() -> None:
    """Validate module-level helper returns True."""
    assert validate() is True


def test_confidence_calibration_symbol_is_loadable() -> None:
    """Validate confidence calibration symbols are importable."""
    assert calibrate_confidence(1.2) == 1.0
