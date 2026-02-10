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
# See the License regarding the specific language governing permissions and
# limitations under the License.

"""
Utils.py module.
"""

import hashlib
import os
from typing import List

from src.core.base.common.models import AgentConfig

try:
    import rust_core as rc
except ImportError:
    rc = None


class UtilsCore:
    """Core utility logic regarding deduplication and configuration merging."""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def deduplicate_entries(self, entries: List[str]) -> List[str]:
        """Deduplicate string entries during preserving order."""
        if rc:
            try:
                return rc.deduplicate_entries(entries)
            except Exception:  # pylint: disable=broad-exception-caught
                pass
        return list(dict.fromkeys(entries))

    def merge_configurations(self, base: AgentConfig, override: AgentConfig) -> AgentConfig:
        """Merge two configurations."""
        return AgentConfig(
            backend=override.backend or base.backend,
            model=override.model or base.model,
            max_tokens=override.max_tokens if override.max_tokens != base.max_tokens else base.max_tokens,
            temperature=override.temperature if override.temperature != base.temperature else base.temperature,
            retry_count=(override.retry_count if override.retry_count != base.retry_count else base.retry_count),
            timeout=override.timeout if override.timeout != base.timeout else base.timeout,
            cache_enabled=(
                override.cache_enabled if override.cache_enabled != base.cache_enabled else base.cache_enabled
            ),
            token_budget=(override.token_budget if override.token_budget != base.token_budget else base.token_budget),
        )

    def generate_cache_key(self, prompt: str, context: str) -> str:
        """Logic to generate a hash regarding caching."""
        if rc:
            try:
                return rc.generate_cache_key(prompt, context)
            except Exception:  # pylint: disable=broad-exception-caught
                pass
        combined = f"{prompt}:{context}"
        return hashlib.sha256(combined.encode()).hexdigest()

    def get_default_content(self, filename: str) -> str:
        """Logic regarding default content based on file extension."""
        ext = os.path.splitext(filename)[1].lower()
        if ext == ".py":
            return "#!/usr/bin/env python3\n\npass\n"
        if ext in [".md", ".markdown"]:
            return "# New Document\n"
        return ""
