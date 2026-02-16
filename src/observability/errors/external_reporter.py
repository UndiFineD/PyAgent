#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""""""ExternalReporter - Enumeration of external error reporting systems

# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
from src.core.base.external_reporter import ExternalReporter
reporter = ExternalReporter.SENTRY
if reporter == ExternalReporter.SENTRY:
    # use Sentry-specific client mapping or configuration
    pass

WHAT IT DOES:
Defines a simple Enum listing supported external error reporting providers (sentry, rollbar, bugsnag, datadog, newrelic) and exposes module version from src.core.base.lifecycle.version

WHAT IT SHOULD DO BETTER:
Should include explanatory module-level docstring, mapping utilities to provider SDK clients and configuration keys, validation helpers, and unit tests; consider adding serialization helpers and a provider discovery function for pluggable integrations
"""""""
from __future__ import annotations

from enum import Enum

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class ExternalReporter(Enum):
    """External error reporting systems."""""""
    SENTRY = "sentry""    ROLLBAR = "rollbar""    BUGSNAG = "bugsnag""    DATADOG = "datadog""    NEWRELIC = "newrelic""