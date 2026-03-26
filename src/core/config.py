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

"""Core agent configuration — dataclass-based, validated, serialisable.

Provides :class:`AgentConfig` (per-agent settings), :class:`SwarmConfig`
(cluster-level settings) and :func:`load_config` / :func:`save_config` for
JSON round-trips.  All values are validated on construction so downstream
code can trust the invariants without repeated checks.
"""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# AgentConfig
# ---------------------------------------------------------------------------

_DEFAULT_MAX_TOKENS = 4096
_DEFAULT_TIMEOUT = 30.0
_DEFAULT_LLM_MODEL = "flm-default"


@dataclass
class AgentConfig:
    """Configuration for a single PyAgent agent instance.

    Parameters
    ----------
    name:
        Unique agent identifier (must be a non-empty string).
    llm_model:
        LLM model identifier used by this agent.
    max_tokens:
        Maximum token budget for a single response.
    timeout:
        Request timeout in seconds.
    enabled:
        Whether this agent should participate in the swarm.
    tags:
        Arbitrary string tags for filtering / routing.
    extra:
        Freeform extra settings not captured by the typed fields.

    """

    name: str
    llm_model: str = _DEFAULT_LLM_MODEL
    max_tokens: int = _DEFAULT_MAX_TOKENS
    timeout: float = _DEFAULT_TIMEOUT
    enabled: bool = True
    tags: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("AgentConfig.name must be a non-empty string")
        if self.max_tokens <= 0:
            raise ValueError(f"max_tokens must be positive, got {self.max_tokens}")
        if self.timeout <= 0:
            raise ValueError(f"timeout must be positive, got {self.timeout}")
        if not self.llm_model or not self.llm_model.strip():
            raise ValueError("llm_model must be a non-empty string")

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a plain dictionary (JSON-safe)."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentConfig":
        """Deserialise from a dictionary (e.g. from JSON).

        Unknown keys are collected into *extra* to allow forward-compatible
        config files.
        """
        known = {"name", "llm_model", "max_tokens", "timeout", "enabled", "tags", "extra"}
        base = {k: v for k, v in data.items() if k in known}
        unknown = {k: v for k, v in data.items() if k not in known}
        if unknown:
            base.setdefault("extra", {}).update(unknown)
        return cls(**base)


# ---------------------------------------------------------------------------
# SwarmConfig
# ---------------------------------------------------------------------------

_DEFAULT_SWARM_CONCURRENCY = 4
_DEFAULT_HEARTBEAT_INTERVAL = 5.0


@dataclass
class SwarmConfig:
    """Cluster-level configuration shared by all agents in the swarm.

    Parameters
    ----------
    swarm_id:
        Unique identifier for this swarm deployment.
    max_concurrency:
        Maximum number of agents allowed to run concurrently.
    heartbeat_interval:
        Seconds between liveness heartbeats.
    log_level:
        Root log level (``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``).
    agents:
        Per-agent configurations indexed by agent name.

    """

    swarm_id: str = "default-swarm"
    max_concurrency: int = _DEFAULT_SWARM_CONCURRENCY
    heartbeat_interval: float = _DEFAULT_HEARTBEAT_INTERVAL
    log_level: str = "INFO"
    agents: dict[str, AgentConfig] = field(default_factory=dict)

    _VALID_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})

    def __post_init__(self) -> None:
        if self.max_concurrency <= 0:
            raise ValueError(f"max_concurrency must be positive, got {self.max_concurrency}")
        if self.heartbeat_interval <= 0:
            raise ValueError(f"heartbeat_interval must be positive, got {self.heartbeat_interval}")
        if self.log_level.upper() not in self._VALID_LOG_LEVELS:
            raise ValueError(
                f"log_level must be one of {sorted(self._VALID_LOG_LEVELS)}, got {self.log_level!r}"
            )
        self.log_level = self.log_level.upper()

    def add_agent(self, config: AgentConfig) -> None:
        """Register an :class:`AgentConfig` by its name."""
        self.agents[config.name] = config

    def remove_agent(self, name: str) -> AgentConfig | None:
        """Remove and return the agent config for *name*, or ``None``."""
        return self.agents.pop(name, None)

    def get_agent(self, name: str) -> AgentConfig | None:
        """Look up an agent config by name."""
        return self.agents.get(name)

    def enabled_agents(self) -> list[AgentConfig]:
        """Return all agent configs where ``enabled=True``."""
        return [a for a in self.agents.values() if a.enabled]

    def to_dict(self) -> dict[str, Any]:
        """Serialise to a nested plain dictionary."""
        d = {
            "swarm_id": self.swarm_id,
            "max_concurrency": self.max_concurrency,
            "heartbeat_interval": self.heartbeat_interval,
            "log_level": self.log_level,
            "agents": {name: cfg.to_dict() for name, cfg in self.agents.items()},
        }
        return d

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SwarmConfig":
        """Deserialise from a nested dictionary."""
        raw_agents: dict[str, Any] = data.pop("agents", {})
        cfg = cls(**data)
        cfg.agents = {name: AgentConfig.from_dict(d) for name, d in raw_agents.items()}
        return cfg


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def load_config(path: str | os.PathLike[str]) -> SwarmConfig:
    """Load a :class:`SwarmConfig` from a JSON file at *path*.

    Parameters
    ----------
    path:
        Filesystem path to a JSON configuration file.

    Raises
    ------
    FileNotFoundError:
        If the file does not exist.
    ValueError:
        If the JSON cannot be parsed or config validation fails.

    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {p}")
    try:
        data: dict[str, Any] = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {p}: {exc}") from exc
    return SwarmConfig.from_dict(data)


def save_config(config: SwarmConfig, path: str | os.PathLike[str]) -> None:
    """Serialise *config* to a JSON file at *path*.

    The parent directory is created if it does not exist.

    Parameters
    ----------
    config:
        The :class:`SwarmConfig` to persist.
    path:
        Destination file path.

    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(config.to_dict(), indent=2), encoding="utf-8")


def validate() -> bool:
    """Confirm the config module is importable and core classes are accessible."""
    assert AgentConfig and SwarmConfig and load_config and save_config  # noqa: S101
    return True
