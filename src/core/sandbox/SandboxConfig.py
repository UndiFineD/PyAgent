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

"""SandboxConfig — immutable policy envelope for the agent execution sandbox."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class SandboxConfig:
    """Immutable policy envelope passed to SandboxedStorageTransaction and SandboxMixin.

    Attributes:
        allowed_paths:   Allowlist of root directories; resolved at validation time.
        allowed_hosts:   Allowlist of exact-match hostnames / IP strings.
        allow_all_hosts: When True, _validate_host() is a no-op (bypass for trusted agents).
        agent_id:        UUID string identifying the agent instance owning this config.

    """

    allowed_paths: list[Path]
    allowed_hosts: list[str]
    allow_all_hosts: bool = False
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @classmethod
    def from_strings(
        cls,
        paths: list[str],
        hosts: list[str],
        allow_all_hosts: bool = False,
        agent_id: str | None = None,
    ) -> "SandboxConfig":
        """Convenience constructor that converts string paths to pathlib.Path objects.

        Args:
            paths:           List of filesystem path strings for the allowlist.
            hosts:           List of exact-match hostname strings for the allowlist.
            allow_all_hosts: Pass True to skip host validation entirely.
            agent_id:        Optional UUID string; auto-generated when omitted.

        Returns:
            A fully constructed SandboxConfig instance.

        """
        return cls(
            allowed_paths=[Path(p) for p in paths],
            allowed_hosts=list(hosts),
            allow_all_hosts=allow_all_hosts,
            agent_id=agent_id or str(uuid.uuid4()),
        )
