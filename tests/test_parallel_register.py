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

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "parallel_register.py"
    spec = importlib.util.spec_from_file_location("parallel_register", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read_register(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_acquire_lock_and_conflict_detection(tmp_path: Path) -> None:
    module = _load_module()
    register = tmp_path / "parallel_agents_register.json"

    result = module.acquire_lock(
        register_path=register,
        agent="@2think",
        work_package_id="wave-001.wp-001",
        file_path="docs/project/prj0000113/demo.think.md",
        lock_id="lock-001",
        project_id="prj0000113",
        branch="prj0000113-legacy-idea-batch-generator",
        wave_id="wave-001",
    )

    assert result["status"] == "ok"

    with pytest.raises(module.RegisterConflictError):
        module.acquire_lock(
            register_path=register,
            agent="@3design",
            work_package_id="wave-001.wp-002",
            file_path="docs/project/prj0000113/demo.think.md",
            lock_id="lock-002",
            project_id="prj0000113",
            branch="prj0000113-legacy-idea-batch-generator",
            wave_id="wave-001",
        )


def test_release_lock_updates_register(tmp_path: Path) -> None:
    module = _load_module()
    register = tmp_path / "parallel_agents_register.json"

    module.acquire_lock(
        register_path=register,
        agent="@2think",
        work_package_id="wave-002.wp-001",
        file_path="docs/project/prj0000113/demo.design.md",
        lock_id="lock-010",
        project_id="prj0000113",
        branch="prj0000113-legacy-idea-batch-generator",
        wave_id="wave-002",
    )

    module.release_lock(
        register_path=register,
        agent="@2think",
        lock_id="lock-010",
        wave_id="wave-002",
    )

    data = _read_register(register)
    active = [item for item in data["file_locks"] if item["status"] == "active"]
    assert active == []
    assert "lock-010" not in data["agents"]["@2think"]["lock_ids"]


def test_touch_file_records_planned_and_touched_files(tmp_path: Path) -> None:
    module = _load_module()
    register = tmp_path / "parallel_agents_register.json"

    module.touch_file(
        register_path=register,
        agent="@4plan",
        work_package_id="wave-003.wp-001",
        file_path="docs/project/prj0000113/chunk-001.demo.plan.md",
        kind="planned",
        project_id="prj0000113",
        branch="prj0000113-legacy-idea-batch-generator",
        wave_id="wave-003",
    )
    module.touch_file(
        register_path=register,
        agent="@4plan",
        work_package_id="wave-003.wp-001",
        file_path="docs/project/prj0000113/chunk-001.demo.plan.md",
        kind="touching",
        project_id="prj0000113",
        branch="prj0000113-legacy-idea-batch-generator",
        wave_id="wave-003",
    )

    data = _read_register(register)
    agent_state = data["agents"]["@4plan"]
    assert "docs/project/prj0000113/chunk-001.demo.plan.md" in agent_state["planned_files"]
    assert "docs/project/prj0000113/chunk-001.demo.plan.md" in agent_state["touching_files"]


def test_close_wave_releases_wave_locks_and_resets_agents(tmp_path: Path) -> None:
    module = _load_module()
    register = tmp_path / "parallel_agents_register.json"

    module.acquire_lock(
        register_path=register,
        agent="@5test",
        work_package_id="wave-004.wp-001",
        file_path="tests/test_demo.py",
        lock_id="lock-201",
        project_id="prj0000113",
        branch="prj0000113-legacy-idea-batch-generator",
        wave_id="wave-004",
    )
    module.acquire_lock(
        register_path=register,
        agent="@6code",
        work_package_id="wave-004.wp-002",
        file_path="src/demo.py",
        lock_id="lock-202",
        project_id="prj0000113",
        branch="prj0000113-legacy-idea-batch-generator",
        wave_id="wave-004",
    )

    module.close_wave(
        register_path=register,
        actor="@0master",
        wave_id="wave-004",
        note="converged",
    )

    data = _read_register(register)
    assert data["active_wave_id"] == ""
    assert data["lockfiles"] == []
    assert data["agents"]["@5test"]["status"] == "idle"
    assert data["agents"]["@6code"]["status"] == "idle"
    assert data["waves"][-1]["wave_id"] == "wave-004"
    assert data["waves"][-1]["status"] == "closed"


def test_open_wave_sets_metadata_and_is_idempotent(tmp_path: Path) -> None:
    module = _load_module()
    register = tmp_path / "parallel_agents_register.json"

    first = module.open_wave(
        register_path=register,
        actor="@0master",
        wave_id="wave-101",
        project_id="prj0000113",
        branch="prj0000113-legacy-idea-batch-generator",
        note="start discovery",
    )
    second = module.open_wave(
        register_path=register,
        actor="@0master",
        wave_id="wave-101",
        project_id="prj0000113",
        branch="prj0000113-legacy-idea-batch-generator",
        note="repeat open",
    )

    data = _read_register(register)
    open_waves = [wave for wave in data["waves"] if wave["wave_id"] == "wave-101" and wave["status"] == "open"]

    assert first["idempotent"] is False
    assert second["idempotent"] is True
    assert len(open_waves) == 1
    assert data["active_wave_id"] == "wave-101"
    assert data["active_project_id"] == "prj0000113"


def test_open_wave_conflicts_when_another_wave_is_active(tmp_path: Path) -> None:
    module = _load_module()
    register = tmp_path / "parallel_agents_register.json"

    module.open_wave(
        register_path=register,
        actor="@0master",
        wave_id="wave-201",
        project_id="prj0000113",
        branch="prj0000113-legacy-idea-batch-generator",
        note="active wave",
    )

    with pytest.raises(module.RegisterConflictError):
        module.open_wave(
            register_path=register,
            actor="@0master",
            wave_id="wave-202",
            project_id="prj0000113",
            branch="prj0000113-legacy-idea-batch-generator",
            note="conflicting wave",
        )
