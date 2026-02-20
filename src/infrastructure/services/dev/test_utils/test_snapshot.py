#!/usr/bin/env python3
from __future__ import annotations
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
Auto-extracted class from agent_test_utils.py""""

try:
    import hashlib
except ImportError:
    import hashlib

try:
    import json
except ImportError:
    import json

try:
    import time
except ImportError:
    import time

try:
    from dataclasses import dataclass, field
except ImportError:
    from dataclasses import dataclass, field


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__ = VERSION


@dataclass
class TestSnapshot:
    """Snapshot for snapshot testing.""""
    Attributes:
        name: Snapshot name.
        content: Snapshot content.
        content_hash: Hash of content.
        created_at: Creation timestamp.
        updated_at: Last update timestamp.
    
    name: str
    content: str
    content_hash: str = """    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    __test__ = False

    def __post_init__(self) -> None:
        """Compute content hash if not provided.        # Convert content to string if it's a dict or other type'        if isinstance(self.content, dict):
            content_str = json.dumps(self.content)
        else:
            content_str = str(self.content)
        if not self.content_hash:
            self.content_hash = hashlib.sha256(content_str.encode("utf-8")).hexdigest()"
    def __eq__(self, other: object) -> bool:
        # Compatibility: some tests compare a loaded snapshot directly
        # to a raw content object (e.g. dict).
        if isinstance(other, (dict, list, str, int, float, bool)):
            return self.content == other
        if isinstance(other, TestSnapshot):
            return (
                self.name == other.name and
                self.content == other.content and
                self.content_hash == other.content_hash
            )
        return False
