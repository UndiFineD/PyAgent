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

"""Tests for src/core/config.py — AgentConfig, SwarmConfig, load_config, save_config."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.core.config import AgentConfig, SwarmConfig, load_config, save_config

# ---------------------------------------------------------------------------
# AgentConfig — construction and validation
# ---------------------------------------------------------------------------


def test_agent_config_defaults() -> None:
    """Creating an AgentConfig with only a name should set defaults for all other fields."""
    cfg = AgentConfig(name="coder")
    assert cfg.llm_model == "flm-default"
    assert cfg.max_tokens == 4096
    assert cfg.timeout == 30.0
    assert cfg.enabled is True
    assert cfg.tags == []
    assert cfg.extra == {}


def test_agent_config_custom_values() -> None:
    """Creating an AgentConfig with custom values should set those values correctly."""
    cfg = AgentConfig(
        name="tester",
        llm_model="llama3",
        max_tokens=2048,
        timeout=60.0,
        enabled=False,
        tags=["ci", "slow"],
        extra={"seed": 42},
    )
    assert cfg.name == "tester"
    assert cfg.max_tokens == 2048
    assert not cfg.enabled
    assert "ci" in cfg.tags
    assert cfg.extra["seed"] == 42


def test_agent_config_empty_name_raises() -> None:
    with pytest.raises(ValueError, match="name"):
        AgentConfig(name="")


def test_agent_config_blank_name_raises() -> None:
    with pytest.raises(ValueError, match="name"):
        AgentConfig(name="   ")


def test_agent_config_negative_max_tokens_raises() -> None:
    with pytest.raises(ValueError, match="max_tokens"):
        AgentConfig(name="x", max_tokens=0)


def test_agent_config_negative_timeout_raises() -> None:
    with pytest.raises(ValueError, match="timeout"):
        AgentConfig(name="x", timeout=-1.0)


def test_agent_config_empty_llm_model_raises() -> None:
    with pytest.raises(ValueError, match="llm_model"):
        AgentConfig(name="x", llm_model="")


# ---------------------------------------------------------------------------
# AgentConfig — serialisation
# ---------------------------------------------------------------------------


def test_agent_config_to_dict_round_trip() -> None:
    original = AgentConfig(name="agent1", tags=["a", "b"], extra={"k": "v"})
    d = original.to_dict()
    restored = AgentConfig.from_dict(d)
    assert restored.name == original.name
    assert restored.tags == original.tags
    assert restored.extra == original.extra


def test_agent_config_from_dict_unknown_keys_go_to_extra() -> None:
    data = {"name": "x", "future_field": "foo", "another": 42}
    cfg = AgentConfig.from_dict(data)
    assert cfg.extra["future_field"] == "foo"
    assert cfg.extra["another"] == 42


# ---------------------------------------------------------------------------
# SwarmConfig — construction and validation
# ---------------------------------------------------------------------------


def test_swarm_config_defaults() -> None:
    cfg = SwarmConfig()
    assert cfg.swarm_id == "default-swarm"
    assert cfg.max_concurrency == 4
    assert cfg.log_level == "INFO"
    assert cfg.agents == {}


def test_swarm_config_log_level_normalised_to_upper() -> None:
    cfg = SwarmConfig(log_level="debug")
    assert cfg.log_level == "DEBUG"


def test_swarm_config_invalid_log_level_raises() -> None:
    with pytest.raises(ValueError, match="log_level"):
        SwarmConfig(log_level="VERBOSE")


def test_swarm_config_nonpositive_concurrency_raises() -> None:
    with pytest.raises(ValueError, match="max_concurrency"):
        SwarmConfig(max_concurrency=0)


def test_swarm_config_nonpositive_heartbeat_raises() -> None:
    with pytest.raises(ValueError, match="heartbeat_interval"):
        SwarmConfig(heartbeat_interval=0.0)


# ---------------------------------------------------------------------------
# SwarmConfig — agent management
# ---------------------------------------------------------------------------


def test_swarm_add_and_get_agent() -> None:
    swarm = SwarmConfig()
    agent = AgentConfig(name="planner")
    swarm.add_agent(agent)
    assert swarm.get_agent("planner") is agent


def test_swarm_remove_agent() -> None:
    swarm = SwarmConfig()
    swarm.add_agent(AgentConfig(name="exec"))
    removed = swarm.remove_agent("exec")
    assert removed is not None
    assert swarm.get_agent("exec") is None


def test_swarm_remove_nonexistent_returns_none() -> None:
    swarm = SwarmConfig()
    assert swarm.remove_agent("ghost") is None


def test_swarm_enabled_agents_filters_disabled() -> None:
    swarm = SwarmConfig()
    swarm.add_agent(AgentConfig(name="on", enabled=True))
    swarm.add_agent(AgentConfig(name="off", enabled=False))
    enabled = swarm.enabled_agents()
    names = [a.name for a in enabled]
    assert "on" in names
    assert "off" not in names


# ---------------------------------------------------------------------------
# SwarmConfig — serialisation
# ---------------------------------------------------------------------------


def test_swarm_config_to_dict_round_trip() -> None:
    swarm = SwarmConfig(swarm_id="test-swarm", max_concurrency=8)
    swarm.add_agent(AgentConfig(name="a1", tags=["tag1"]))
    d = swarm.to_dict()
    assert d["swarm_id"] == "test-swarm"
    assert "a1" in d["agents"]


def test_swarm_config_from_dict() -> None:
    data = {
        "swarm_id": "s1",
        "max_concurrency": 2,
        "heartbeat_interval": 10.0,
        "log_level": "WARNING",
        "agents": {"bot": {"name": "bot", "llm_model": "gpt4", "max_tokens": 1000}},
    }
    cfg = SwarmConfig.from_dict(data)
    assert cfg.swarm_id == "s1"
    bot = cfg.get_agent("bot")
    assert bot is not None
    assert bot.llm_model == "gpt4"


# ---------------------------------------------------------------------------
# load_config / save_config
# ---------------------------------------------------------------------------


def test_save_and_load_round_trip(tmp_path: Path) -> None:
    swarm = SwarmConfig(swarm_id="persisted", max_concurrency=6)
    swarm.add_agent(AgentConfig(name="worker", tags=["prod"]))

    path = tmp_path / "config.json"
    save_config(swarm, path)

    loaded = load_config(path)
    assert loaded.swarm_id == "persisted"
    assert loaded.max_concurrency == 6
    worker = loaded.get_agent("worker")
    assert worker is not None
    assert "prod" in worker.tags


def test_load_config_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_config(tmp_path / "nonexistent.json")


def test_load_config_invalid_json(tmp_path: Path) -> None:
    bad = tmp_path / "bad.json"
    bad.write_text("not json!!!", encoding="utf-8")
    with pytest.raises(ValueError, match="Invalid JSON"):
        load_config(bad)


def test_save_config_creates_parent_dirs(tmp_path: Path) -> None:
    nested = tmp_path / "a" / "b" / "c" / "config.json"
    save_config(SwarmConfig(), nested)
    assert nested.exists()
    # Verify it's valid JSON
    data = json.loads(nested.read_text())
    assert "swarm_id" in data
