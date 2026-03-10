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
"""Minimal observability helpers."""

from __future__ import annotations
import json
from typing import Any, Mapping


def emit_metric(name: str, value: Any, labels: Mapping[str, Any] | None = None) -> None:
    """Emit a lightweight metric representation to stdout (structured JSON).

    This is intentionally minimal so tests/CI can call it without external
    dependencies. Consumers may later replace with real metrics exporters.
    """
    payload = {"metric": name, "value": value, "labels": dict(labels or {})}
    print(json.dumps(payload))


def validate() -> None:
    """Lightweight import-safe validation hook."""
    # emit a harmless metric to ensure function executes
    emit_metric("core.test.metric", 1, {"unit": "count"})
