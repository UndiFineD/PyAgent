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

"""Confidence calibration helpers for route classification."""

from __future__ import annotations


def calibrate_confidence(raw_confidence: float) -> float:
    """Clamp confidence into the closed interval [0.0, 1.0].

    Args:
        raw_confidence: Raw confidence value from classifier.

    Returns:
        Bounded confidence value in [0.0, 1.0].

    """
    if raw_confidence < 0.0:
        return 0.0
    if raw_confidence > 1.0:
        return 1.0
    return raw_confidence


def validate() -> bool:
    """Validate confidence calibration boundaries.

    Returns:
        True when calibration clamps values to expected bounds.

    """
    return calibrate_confidence(-0.1) == 0.0 and calibrate_confidence(1.1) == 1.0 and calibrate_confidence(0.5) == 0.5
