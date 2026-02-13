#!/usr/bin/env python3
# Refactored by copilot-placeholder
# Refactored by copilot-placeholder
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
ConflictResolution - Resolution dataclass for conflicting improvements

Brief Summary
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate to represent the outcome of resolving a conflict between proposed improvements.
- Example: cr = ConflictResolution(improvement_id="imp-123", resolution=improvement_obj, strategy="merge", resolved_by="keimpe")

WHAT IT DOES:
- Simple dataclass encapsulating an improvement conflict resolution: stores the conflicting improvement ID, the chosen Improvement instance, the strategy used, and who resolved it.

WHAT IT SHOULD DO BETTER:
- Add validation to ensure resolution is an Improvement and improvement_id is non-empty.
- Provide serialization (to_dict/from_dict), equality/hash implementations, and richer strategies enum instead of free-form strings.
- Include unit tests, logging of resolution actions, and optional timestamping of when the conflict was resolved.

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


"""Auto-extracted class from agent_improvements.py"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement

__version__ = VERSION


@dataclass
class ConflictResolution:
    """Resolution for a conflicting improvement.

    Attributes:
        improvement_id: ID of conflicting improvement.
        resolution: Resolved improvement version.
        strategy: Resolution strategy used.
        resolved_by: Who resolved the conflict.
    """

    improvement_id: str
    resolution: Improvement
    strategy: str = "manual"
    resolved_by: str = ""
"""

from __future__ import annotations

from dataclasses import dataclass

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement

__version__ = VERSION


@dataclass
class ConflictResolution:
    """Resolution for a conflicting improvement.

    Attributes:
        improvement_id: ID of conflicting improvement.
        resolution: Resolved improvement version.
        strategy: Resolution strategy used.
        resolved_by: Who resolved the conflict.
    """

    improvement_id: str
    resolution: Improvement
    strategy: str = "manual"
    resolved_by: str = ""
