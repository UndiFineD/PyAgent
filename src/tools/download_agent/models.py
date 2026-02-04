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
Data models for the Download Agent.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class DownloadResult:
    """Result of a download operation."""
    url: str
    success: bool
    destination: str
    file_type: str
    size_bytes: int = 0
    error_message: str = ""
    metadata: Dict = None


@dataclass
class DownloadConfig:
    """Configuration for download operations."""
    urls_file: str = "docs/download/urls.txt"
    base_dir: str = "."
    max_retries: int = 3
    timeout_seconds: int = 30
    delay_between_downloads: float = 1.0
    skip_existing: bool = True
    dry_run: bool = False
    verbose: bool = False