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


"""Unified time and timestamp management core."""


import time
from datetime import datetime, timezone

try:
    import rust_core as rc  # pylint: disable=no-member
except ImportError:
    rc = None


class TimeCore:
    """Ensures consistent time handling across the swarm (UTC focused)."""

    @staticmethod
    def now() -> datetime:
        """Get current UTC datetime."""
        if rc and hasattr(rc, "get_utc_timestamp_rust"):
            try:
                ts = rc.get_utc_timestamp_rust()  # pylint: disable=no-member
                return datetime.fromtimestamp(ts, tz=timezone.utc)
            except RuntimeError:  # pylint: disable=broad-exception-caught, unused-variable
                # Rust bridge reported an error; fall back to Python
                pass
        return datetime.now(timezone.utc)


    @staticmethod
    def timestamp() -> float:
        """Get current UTC timestamp."""
        if rc and hasattr(rc, "get_utc_timestamp_rust"):
            try:
                return float(rc.get_utc_timestamp_rust())  # pylint: disable=no-member
            except RuntimeError:  # pylint: disable=broad-exception-caught, unused-variable
                # Rust bridge reported an error; fall back to Python
                pass
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
