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
ErrorCluster - Grouping container for similar agent errors

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
Instantiate ErrorCluster to group related error identifiers, attach a human name, matching pattern and optional description for aggregation and reporting within agent error handling

WHAT IT DOES:
Holds metadata for a cluster of similar errors: id, name, pattern, list of error_ids and an optional description used by higher-level error aggregation and diagnostics

WHAT IT SHOULD DO BETTER:
Document validation rules for pattern and id, provide immutability or controlled mutation methods, and add helper methods for merging, matching and serializing clusters

FILE CONTENT SUMMARY:
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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ErrorCluster:
    """A cluster of similar errors."""

    id: str
    name: str
    pattern: str
    error_ids: list[str] = field(default_factory=lambda: [])
    description: str = ""
"""

from __future__ import annotations

from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ErrorCluster:
    """A cluster of similar errors."""

    id: str
    name: str
    pattern: str
    error_ids: list[str] = field(default_factory=lambda: [])
    description: str = ""
