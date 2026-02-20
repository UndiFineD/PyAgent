#!/usr/bin/env python3
from __future__ import annotations

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
"""
AgentConfig dataclass used across PyAgent.

"""
This is a minimal, import-safe representation suitable for tests.
"""
from dataclasses import dataclass, field
from typing import Any, Optional

try:
    from src.core.base.common.models.agent_models import AgentPluginConfig
except Exception:
    class AgentPluginConfig:  # type: ignore
        pass

try:
    from src.core.base.common.models.fleet_models import RateLimitConfig
except Exception:
    class RateLimitConfig:  # type: ignore
        pass

try:
    from src.core.base.common.utils.helpers import _empty_dict_str_any, _empty_dict_str_int, _empty_list_str, _empty_plugin_config_list
except Exception:
    def _empty_dict_str_any():
        return {}

    def _empty_dict_str_int():
        return {}

    def _empty_list_str():
        return []

    def _empty_plugin_config_list():
        return []


@dataclass
class AgentConfig:
    repo_root: str = "."
    agents_only: bool = False
    max_files: Optional[int] = None
    loop: int = 1
    dry_run: bool = False
    no_git: bool = False
    verbosity: str = "normal"
    rate_limit: Optional[RateLimitConfig] = None
    plugins: list[AgentPluginConfig] = field(default_factory=_empty_plugin_config_list)
    selective_agents: list[str] = field(default_factory=_empty_list_str)
    timeout_per_agent: dict[str, int] = field(default_factory=_empty_dict_str_int)
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
