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
"""Lane sync tests for /api/projects stage artifact progression."""
from __future__ import annotations

import shutil
from pathlib import Path

import backend.app as app_mod
from fastapi.testclient import TestClient


def test_projects_auto_advance_to_in_sprint_from_stage_artifacts(monkeypatch) -> None:
    """A Discovery project advances to In Sprint when design/test artifacts exist."""
    client = TestClient(app_mod.app, raise_server_exceptions=False)

    project_id = "prj9999993"
    project_copy = list(app_mod._PROJECTS)
    app_mod._PROJECTS = [
        {
            "id": project_id,
            "name": "lane-sync-test",
            "lane": "Discovery",
            "summary": "sync stage test",
            "branch": None,
            "pr": None,
            "priority": "P3",
            "budget_tier": "S",
            "tags": ["test"],
            "created": "2026-03-28",
            "updated": "2026-03-28",
        }
    ]

    project_dir = Path(app_mod._PROJECT_ROOT) / "docs" / "project" / f"{project_id}-lane-sync-test"
    project_dir.mkdir(parents=True, exist_ok=True)
    design_file = project_dir / "lane-sync-test.design.md"
    test_file = project_dir / "lane-sync-test.test.md"
    design_file.write_text("# design\n", encoding="utf-8")
    test_file.write_text("# test\n", encoding="utf-8")

    monkeypatch.setattr(app_mod, "_save_projects", lambda: None)

    try:
        response = client.get("/api/projects")
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 1
        assert payload[0]["id"] == project_id
        assert payload[0]["lane"] == "In Sprint"
    finally:
        app_mod._PROJECTS = project_copy
        shutil.rmtree(project_dir, ignore_errors=True)


def test_projects_auto_advance_to_review_from_exec_or_ql_artifacts(monkeypatch) -> None:
    """A project advances to Review when exec/ql stage artifacts exist."""
    client = TestClient(app_mod.app, raise_server_exceptions=False)

    project_id = "prj9999992"
    project_copy = list(app_mod._PROJECTS)
    app_mod._PROJECTS = [
        {
            "id": project_id,
            "name": "lane-review-sync-test",
            "lane": "In Sprint",
            "summary": "sync stage test",
            "branch": None,
            "pr": None,
            "priority": "P3",
            "budget_tier": "S",
            "tags": ["test"],
            "created": "2026-03-28",
            "updated": "2026-03-28",
        }
    ]

    project_dir = Path(app_mod._PROJECT_ROOT) / "docs" / "project" / f"{project_id}-lane-review-sync-test"
    project_dir.mkdir(parents=True, exist_ok=True)
    exec_file = project_dir / "lane-review-sync-test.exec.md"
    exec_file.write_text("# exec\n", encoding="utf-8")

    monkeypatch.setattr(app_mod, "_save_projects", lambda: None)

    try:
        response = client.get("/api/projects")
        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 1
        assert payload[0]["id"] == project_id
        assert payload[0]["lane"] == "Review"
    finally:
        app_mod._PROJECTS = project_copy
        shutil.rmtree(project_dir, ignore_errors=True)
