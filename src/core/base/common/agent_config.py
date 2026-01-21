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

"""Auto-extracted class from agent.py"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from src.core.base.common.models import AgentPluginConfig, RateLimitConfig
from src.core.base.common.utils.helpers import (
    _empty_dict_str_any,
    _empty_plugin_config_list,
    _empty_list_str,
    _empty_dict_str_int,
)
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


@dataclass
class AgentConfig:
    """Full agent configuration loaded from config file.

    Attributes:
        repo_root: Repository root directory.
        agents_only: Process only agent files.
        max_files: Maximum files to process.
        loop: Number of processing loops.
        dry_run: Preview mode without modifications.
        no_git: Skip git operations.
        verbosity: Logging verbosity level.
        rate_limit: Rate limiting configuration.
        plugins: List of plugin configurations.
        selective_agents: Agents to execute.
        timeout_per_agent: Timeout settings per agent.
    """

    repo_root: str = "."
    agents_only: bool = False
    max_files: int | None = None
    loop: int = 1
    dry_run: bool = False
    no_git: bool = False
    verbosity: str = "normal"
    rate_limit: RateLimitConfig | None = None
    plugins: list[AgentPluginConfig] = field(default_factory=_empty_plugin_config_list)
    selective_agents: list[str] = field(default_factory=_empty_list_str)
    timeout_per_agent: dict[str, int] = field(default_factory=_empty_dict_str_int)
    # Additional CLI-equivalent settings
    enable_async: bool = False
    enable_multiprocessing: bool = False
    max_workers: int = 4
    strategy: str = "direct"
    enable_file_locking: bool = False
    incremental: bool = False
    graceful_shutdown: bool = False
    health_check: bool = False
    resume: bool = False
    diff_preview: bool = False
    webhook: list[str] = field(default_factory=_empty_list_str)
    models: dict[str, Any] = field(default_factory=_empty_dict_str_any)
