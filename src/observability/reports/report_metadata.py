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
from src.core.base.version import VERSION
from dataclasses import dataclass

__version__ = VERSION


@dataclass
class ReportMetadata:
    """Metadata for a generated report.
    Attributes:
        path: Path to source file.
        generated_at: Timestamp of generation.
        content_hash: SHA256 hash of content.
        version: Report version string.
    """

    path: str
    generated_at: str
    content_hash: str
    version: str
