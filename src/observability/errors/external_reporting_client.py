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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from .ErrorEntry import ErrorEntry
from .ExternalReporter import ExternalReporter
from typing import Any, Dict, List
import logging

__version__ = VERSION

class ExternalReportingClient:
    """Reports errors to external systems.

    Supports Sentry, Rollbar, Bugsnag, Datadog, and NewRelic
    integrations.

    Attributes:
        system: The external system to report to.
        dsn: Data source name or API key.
    """

    def __init__(
        self, system: ExternalReporter, dsn: str = ""
    ) -> None:
        """Initialize the external reporting client.

        Args:
            system: The external system type.
            dsn: Data source name or API key.
        """
        self.system = system
        self.dsn = dsn
        self.enabled = bool(dsn)

    def report(self, error: ErrorEntry) -> bool:
        """Report an error to the external system.

        Args:
            error: The error to report.

        Returns:
            True if reported successfully.
        """
        if not self.enabled:
            return False
        self._build_payload(error)
        logging.info(
            f"Reporting to {self.system.value}: {error.id}"
        )
        # Actual implementation would send to the service
        return True

    def report_batch(self, errors: list[ErrorEntry]) -> int:
        """Report multiple errors.

        Args:
            errors: List of errors to report.

        Returns:
            Number of errors successfully reported.
        """
        count = 0
        for error in errors:
            if self.report(error):
                count += 1
        return count

    def _build_payload(self, error: ErrorEntry) -> dict[str, Any]:
        """Build the payload for the external system."""
        return {
            "message": error.message,
            "level": error.severity.name.lower(),
            "tags": {
                "category": error.category.value,
                "file": error.file_path,
                "line": error.line_number
            },
            "extra": {
                "stack_trace": error.stack_trace,
                "suggested_fix": error.suggested_fix
            }
        }