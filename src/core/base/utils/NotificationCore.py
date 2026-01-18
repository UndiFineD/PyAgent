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


"""
NotificationCore logic for PyAgent.
Pure logic for payload formatting and domain extraction.
No I/O or side effects.
"""

from __future__ import annotations
from src.core.base.Version import VERSION
import time
import urllib.parse
from typing import Any

__version__ = VERSION


class NotificationCore:
    """Pure logic core for notification management."""

    @staticmethod
    def construct_payload(
        event_name: str, event_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Formats the JSON payload for webhook delivery."""
        return {
            "event": event_name,
            "timestamp": time.time(),
            "data": event_data,
            "version": "1.1.0",
        }

    @staticmethod
    def get_domain_from_url(url: str) -> str:
        """Extracts the network location (domain) from a URL for connectivity tracking."""
        try:
            domain = urllib.parse.urlparse(url).netloc
            return domain or url
        except Exception:
            return url

    @staticmethod
    def validate_event_data(data: dict[str, Any]) -> bool:
        """Basic validation for event data structures."""
        # Ensure it's a non-empty dictionary
        return isinstance(data, dict) and len(data) > 0
