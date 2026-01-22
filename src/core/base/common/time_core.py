# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: Copyright contributors to the PyAgent project
"""Unified time and timestamp management core."""

import time
from datetime import datetime, timezone
from typing import Optional


try:
    import rust_core as rc
except ImportError:
    rc = None

class TimeCore:
    """
    Ensures consistent time handling across the swarm (UTC focused).
    """

    @staticmethod
    def now() -> datetime:
        """Get current UTC datetime."""
        if rc and hasattr(rc, "get_utc_timestamp_rust"):
            ts = rc.get_utc_timestamp_rust()
            return datetime.fromtimestamp(ts, tz=timezone.utc)
        return datetime.now(timezone.utc)

    @staticmethod
    def timestamp() -> float:
        """Get current UTC timestamp."""
        if rc and hasattr(rc, "get_utc_timestamp_rust"):
            return float(rc.get_utc_timestamp_rust())
        return time.time()

    @classmethod
    def iso_now(cls, include_z: bool = True) -> str:
        """Get ISO 8601 formatted UTC string."""
        ts = cls.now().isoformat()
        if include_z:
            return ts.replace("+00:00", "Z")
        return ts

    @staticmethod
    def format_duration(seconds: float) -> str:
        """Format seconds into HH:MM:SS."""
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{int(h):02d}:{int(m):02d}:{float(s):05.2f}"

    @staticmethod
    def parse_iso(iso_string: str) -> datetime:
        """Parse ISO string back to UTC datetime."""
        if iso_string.endswith("Z"):
            iso_string = iso_string.replace("Z", "+00:00")
        dt = datetime.fromisoformat(iso_string)
        if dt.tzinfo is None:
            return dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
