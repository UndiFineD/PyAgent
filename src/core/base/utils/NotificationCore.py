#!/usr/bin/env python3

"""
NotificationCore logic for PyAgent.
Pure logic for payload formatting and domain extraction.
No I/O or side effects.
"""

import time
import urllib.parse
from typing import Dict, Any, Optional

class NotificationCore:
    """Pure logic core for notification management."""

    @staticmethod
    def construct_payload(event_name: str, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Formats the JSON payload for webhook delivery."""
        return {
            'event': event_name,
            'timestamp': time.time(),
            'data': event_data,
            'version': '1.1.0'
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
    def validate_event_data(data: Dict[str, Any]) -> bool:
        """Basic validation for event data structures."""
        # Ensure it's a non-empty dictionary
        return isinstance(data, dict) and len(data) > 0
