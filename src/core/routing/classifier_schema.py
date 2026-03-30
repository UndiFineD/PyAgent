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

"""Validation for classifier output contracts."""

from __future__ import annotations

from src.core.routing.routing_models import ClassifierResult


class ClassifierSchemaError(ValueError):
    """Raised when classifier results violate required schema constraints."""


def validate_classifier_result(result: ClassifierResult) -> None:
    """Validate classifier output shape and bounds.

    Args:
        result: Classifier output to validate.

    Raises:
        ClassifierSchemaError: If schema constraints are violated.

    """
    if not result.candidate_routes:
        raise ClassifierSchemaError("candidate_routes must not be empty")
    if result.confidence < 0.0 or result.confidence > 1.0:
        raise ClassifierSchemaError("confidence must be in [0.0, 1.0]")

    last_score = float("inf")
    for candidate in result.candidate_routes:
        route = candidate.route.strip()
        if route == "":
            raise ClassifierSchemaError("candidate route must be non-empty")
        if candidate.score > last_score:
            raise ClassifierSchemaError("candidate_routes must be ordered by descending score")
        last_score = candidate.score
