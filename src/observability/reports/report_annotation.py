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
ReportAnnotation - Report annotation dataclass

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate to attach a short, timestamped note to a generated report.
- Store and transmit lightweight annotation metadata (id, author, content, optional line number).
- Use in report builders, exporters, or UI layers to display or persist user/developer comments.

WHAT IT DOES:
- Provides a compact, immutable-by-convention dataclass for report annotations.
- Automatically stamps annotations with a creation timestamp.
- Keeps minimal fields required to reference a report and locate the annotation within the report text.

WHAT IT SHOULD DO BETTER:
- Add validation for IDs and content length; reject empty or excessively long annotations.
- Provide serialization helpers (to_dict/from_dict, JSON) and equality/hash implementations for storage and testing.
- Consider using timezone-aware datetimes instead of raw floats and support optional edited_at/updated_at fields.

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


"""Auto-extracted class from generate_agent_reports.py"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ReportAnnotation:
    """Annotation on a report.
    Attributes:
        annotation_id: Unique annotation identifier.
        report_id: Associated report ID.
        author: Author of annotation.
        content: Annotation content.
        line_number: Line number if applicable.
        created_at: Creation timestamp.
    """

    annotation_id: str
    report_id: str
    author: str
    content: str
    line_number: int | None = None
    created_at: float = field(default_factory=time.time)  # type: ignore[assignment]
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class ReportAnnotation:
    """Annotation on a report.
    Attributes:
        annotation_id: Unique annotation identifier.
        report_id: Associated report ID.
        author: Author of annotation.
        content: Annotation content.
        line_number: Line number if applicable.
        created_at: Creation timestamp.
    """

    annotation_id: str
    report_id: str
    author: str
    content: str
    line_number: int | None = None
    created_at: float = field(default_factory=time.time)  # type: ignore[assignment]
