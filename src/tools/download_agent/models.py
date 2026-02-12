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
models.py - Data models for the Download Agent

[Brief Summary]
DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- Instantiate DownloadConfig to configure runs (paths, retries, timeouts, dry-run, verbosity).
- Use DownloadResult to collect and return per-URL results from download worker functions or agents.
- Example (conceptual): cfg = DownloadConfig(base_dir="out", dry_run=True); result = DownloadResult(url="http://…", success=False, destination="", file_type="")

WHAT IT DOES:
- Declares two simple dataclasses used by the Download Agent: DownloadResult and DownloadConfig.
- DownloadResult captures the outcome of a single download (url, success flag, destination path, file type, size, error message and optional metadata).
- DownloadConfig centralizes default runtime parameters for download operations (input file location, base directory, retry and timeout behavior, pacing, and CLI-like flags such as skip_existing, dry_run and verbose).

WHAT IT SHOULD DO BETTER:
- Add type aliases and stricter typing (e.g., TypedDict for metadata or Optional[str] where appropriate) and validate fields (paths, non-negative integers) either via __post_init__ or a factory/validator to fail-fast on incorrect configs.
- Document units and expectations more explicitly (e.g., whether size_bytes is exact or estimated, what file_type values are allowed).
- Consider providing convenience methods on DownloadConfig (e.g., resolve_base_dir(), load_urls()) and on DownloadResult (to_dict(), human_readable_size()) to centralize common behavior and improve testability.
- Add comprehensive docstrings and examples for each class and consider using pydantic/dataclasses with validators if stricter runtime guarantees are required.

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

"""
Data models for the Download Agent.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class DownloadResult:
    """Result of a download operation."""
    url: str
    success: bool
    destination: str
    file_type: str
    size_bytes: int = 0
    error_message: str = ""
    metadata: dict[str, Any] | None = None


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
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass
class DownloadResult:
    """Result of a download operation."""
    url: str
    success: bool
    destination: str
    file_type: str
    size_bytes: int = 0
    error_message: str = ""
    metadata: dict[str, Any] | None = None


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
