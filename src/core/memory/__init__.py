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
"""Core memory package exports."""

from __future__ import annotations

from typing import Any


class MemoryStore:
	"""In-memory key/value store used by unit tests."""

	def __init__(self) -> None:
		"""Initialize an empty store."""
		self._data: dict[str, Any] = {}

	def set(self, key: str, value: Any) -> None:
		"""Store a value for the provided key."""
		self._data[key] = value

	def get(self, key: str, default: Any | None = None) -> Any:
		"""Return the value for key, or default when missing."""
		return self._data.get(key, default)


def validate() -> None:
	"""Validate the package configuration.

	This minimal implementation intentionally performs no checks.
	"""


__all__ = ["MemoryStore", "validate"]
