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


"""Lightweight LongTermMemory shim for tests.

Provides a minimal API so cognitive agents can import and use a
placeholder long-term memory during unit tests.
"""

import logging
from typing import Any, Dict, List, Optional

try:
    from src.core.base.lifecycle.version import VERSION
except Exception:
    VERSION = "0.0.0"

__version__ = VERSION


class LongTermMemory:
    """Minimal long-term memory placeholder.

    Stores simple dictionary records in memory for testing purposes.
    """

    def __init__(self) -> None:
        self.version = VERSION
        self._store: List[Dict[str, Any]] = []
        logging.getLogger(__name__).info("LongTermMemory initialized (shim)")

    def add_record(self, record: Dict[str, Any]) -> None:
        self._store.append(record)

    def query(self, query_text: str) -> List[Dict[str, Any]]:
        # naive substring match against stored 'text' fields
        res: List[Dict[str, Any]] = []
        for r in self._store:
            text = str(r.get("text", ""))
            if query_text.lower() in text.lower():
                res.append(r)
        return res

    def clear(self) -> None:
        self._store.clear()