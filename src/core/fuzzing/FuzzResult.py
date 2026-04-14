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

"""Typed case and campaign result models for fuzzing runs."""

from __future__ import annotations

from dataclasses import dataclass

from .exceptions import FuzzConfigurationError
from .FuzzCase import FuzzCase


@dataclass(frozen=True, slots=True)
class FuzzCaseResult:
    """Represents one executed case outcome.

    Attributes:
        case: Executed case contract.
        status: Canonical result state.
        duration_ms: Execution time in milliseconds.
        bytes_sent: Payload bytes sent to target.
        error: Optional error string.

    """

    case: FuzzCase
    status: str
    duration_ms: int
    bytes_sent: int
    error: str | None

    def __post_init__(self) -> None:
        """Validate case result fields."""
        self.validate()

    def validate(self) -> None:
        """Validate the case result contract.

        Raises:
            FuzzConfigurationError: If fields are invalid.

        """
        if not self.status:
            msg = "status must be non-empty"
            raise FuzzConfigurationError(msg)
        if self.duration_ms < 0:
            msg = "duration_ms must be >= 0"
            raise FuzzConfigurationError(msg)
        if self.bytes_sent < 0:
            msg = "bytes_sent must be >= 0"
            raise FuzzConfigurationError(msg)


@dataclass(frozen=True, slots=True)
class FuzzCampaignResult:
    """Represents deterministic aggregate outcomes for one campaign."""

    case_results: tuple[FuzzCaseResult, ...]
    summary_counts: dict[str, int]

    def validate(self) -> None:
        """Validate summary counts against case result statuses.

        Raises:
            FuzzConfigurationError: If summary counts do not match results.

        """
        expected: dict[str, int] = {}
        for item in self.case_results:
            expected[item.status] = expected.get(item.status, 0) + 1
        if expected != self.summary_counts:
            msg = "summary_counts must match aggregate case statuses"
            raise FuzzConfigurationError(msg)

    @classmethod
    def from_case_results(cls, results: list[FuzzCaseResult]) -> "FuzzCampaignResult":
        """Build deterministic summary counts from case results.

        Args:
            results: Ordered case execution results.

        Returns:
            Campaign-level aggregate result object.

        """
        counts: dict[str, int] = {}
        for item in results:
            counts[item.status] = counts.get(item.status, 0) + 1
        campaign = cls(case_results=tuple(results), summary_counts=counts)
        campaign.validate()
        return campaign
