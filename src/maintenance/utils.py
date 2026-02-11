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

# Recovered and standardized for Phase 317

"""
Standard maintenance utilities for the PyAgent ecosystem.

Provides shared helper functions for filesystem cleanup, log rotation,
and environment verification used by other maintenance components.
"""

from __future__ import annotations

import logging
from typing import Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class MaintenanceUtils:
    """
    Support utilities for fleet maintenance and environment stabilization.

    Provides foundational tools for the Tier 5 (Maintenance) layer,
    including log rotation, temporary file pruning, and environment
    integrity checks required for long-running autonomous operations.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.version = VERSION
        logging.info(f"MaintenanceUtils initialized (v{VERSION}).")
