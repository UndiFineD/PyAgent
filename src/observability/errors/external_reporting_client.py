#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
ExternalReportingClient - Report errors to external monitoring services

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate with an ExternalReporter enum value and an optional DSN/API key.
- Call report(error: ErrorEntry) to send a single error (returns bool).
- Call report_batch(list[ErrorEntry]) to send multiple errors (returns int count).
Example:
    from src.integrations.external_reporting_client import ExternalReportingClient
    client = ExternalReportingClient(ExternalReporter.SENTRY, dsn="https://example")
    client.report(error_entry)
    client.report_batch([error1, error2])

WHAT IT DOES:
- Provides a lightweight client class (ExternalReportingClient) that builds
  a shaped payload from an ErrorEntry and logs a reporting action.
- Supports single and batch reporting flows, and enables/disables reporting
  based on presence of a DSN.
- Produces a consistent payload structure with message, severity level,
  tags (category, file, line) and extra (stack trace, suggested fix).

WHAT IT SHOULD DO BETTER:
- Implement the actual network transport and retry/backoff logic for each
  supported provider (Sentry, Rollbar, Bugsnag, Datadog, NewRelic) rather
  than only logging.
- Add secure DSN handling (avoid storing raw keys), validation, and
  provider-specific payload adaptations.
- Improve observability (return rich result details or errors), add
  asynchronous reporting option, rate limiting, batching optimizations,
  and unit/integration tests for provider integrations.
- Validate input ErrorEntry fields and handle partial failures in batch
  reporting (currently treats all as succeed on logging).
"""


from __future__ import annotations


try:
    import logging
except ImportError:
    import logging

try:
    from typing import Any
except ImportError:
    from typing import Any


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .error_entry import ErrorEntry
except ImportError:
    from .error_entry import ErrorEntry

try:
    from .external_reporter import ExternalReporter
except ImportError:
    from .external_reporter import ExternalReporter


__version__ = VERSION


class ExternalReportingClient:
    """Reports errors to external systems.
    Supports Sentry, Rollbar, Bugsnag, Datadog, and NewRelic integrations.

    Attributes:
        system: The external system to report to.
        dsn: Data source name or API key.
    """

    def __init__(self, system: ExternalReporter, dsn: str = "") -> None:
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
        payload = self._build_payload(error)
        logging.info(f"Reporting error to {self.system.name}: {payload}")
        return True


    def _build_payload(self, error: ErrorEntry) -> dict[str, Any]:
        """Build the payload for the external system."""
        return {
            "message": error.message,
            "level": error.severity.name.lower(),
            "tags": {
                "category": error.category.value,
                "file": error.file_path,
                "line": error.line_number,
            },
            "extra": {
                "stack_trace": error.stack_trace,
                "suggested_fix": error.suggested_fix,
            },
        }
