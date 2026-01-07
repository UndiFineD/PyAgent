#!/usr/bin/env python3

"""Auto-extracted class from agent_test_utils.py"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
import time

@dataclass
class TestSnapshot:
    __test__ = False
    """Snapshot for snapshot testing.

    Attributes:
        name: Snapshot name.
        content: Snapshot content.
        content_hash: Hash of content.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    """

    name: str
    content: str
    content_hash: str = ""
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    def __post_init__(self) -> None:
        """Compute content hash if not provided."""
        # Convert content to string if it's a dict or other type
        if isinstance(self.content, dict):
            content_str = json.dumps(self.content)
        else:
            content_str = str(self.content)
        if not self.content_hash:
            self.content_hash = hashlib.sha256(
                content_str.encode("utf-8")
            ).hexdigest()

    def __eq__(self, other: object) -> bool:
        # Compatibility: some tests compare a loaded snapshot directly
        # to a raw content object (e.g. dict).
        if isinstance(other, (dict, list, str, int, float, bool)):
            return self.content == other
        if isinstance(other, TestSnapshot):
            return (
                self.name == other.name
                and self.content == other.content
                and self.content_hash == other.content_hash
            )
        return False
