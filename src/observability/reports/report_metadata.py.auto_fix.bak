from __future__ import annotations


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


"""
# DATE: 2026-02-12
# AUTHOR: Keimpe de Jong
USAGE:
    # Import ReportMetadata from its module and instantiate when generating or embedding metadata for report files:
    # from src.observability.reports.report_metadata import ReportMetadata
    meta = ReportMetadata(
        path="reports/agent_report.md",
        generated_at="2026-02-12T21:50:00Z",
        content_hash="...",
        version="0.1.0"
    )
    # Attach meta to generated report objects, and serialize to/from dict or JSON when persisting or embedding in report headers.
    # Use in report generation pipelines to record provenance and to enable reproducibility.

WHAT IT DOES:
- Provides a minimal dataclass container for core report provenance
  fields: file path, generation timestamp, content SHA256 hash,
  and version.
- Centralizes the version import from
  src.core.base.lifecycle.version so report instances reflect
  package versioning.

WHAT IT SHOULD DO BETTER:
- Use stronger types and validation:
  replace path: str with pathlib.Path,
  generated_at: str with datetime (or an ISO8601-aware type),
  and enforce content_hash format (SHA256) at construction.
- Add convenience methods:
  to_dict()/from_dict(),
  to_json()/from_json(),
  and a validation method to recompute and verify content_hash
  against file contents.
- Consider migration to pydantic or dataclasses with post-init
  validation for clearer error messages and automatic
  (de)serialization, and add unit tests covering serialization,
  validation, and version compatibility.
"""

try:
    from dataclasses import dataclass
except ImportError:
    from dataclasses import dataclass


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


__version__: str = VERSION


@dataclass
class ReportMetadata:
    """Metadata for a generated report.
    Fields:
        path: File path of the report.
        generated_at: ISO 8601 timestamp when the report was generated.
        content_hash: SHA256 hash of the report content.
        version: Version of the software that generated the report.
    """
    path: str
    generated_at: str
    content_hash: str
    version: str = __version__
