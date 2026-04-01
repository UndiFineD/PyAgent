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


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "PromoteLegacyIdeas.py"
    spec = importlib.util.spec_from_file_location("PromoteLegacyIdeas", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def test_promote_top_ideas_creates_markdown_files(tmp_path: Path) -> None:
    module = _load_module()
    input_jsonl = tmp_path / "ideas.jsonl"
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    state_file = tmp_path / "state.json"
    manifest = tmp_path / "manifest.json"
    archive_dir.mkdir(parents=True)

    _write_jsonl(
        input_jsonl,
        [
            {
                "idea_id": "legacy-a-01",
                "source_file": "src/a.py",
                "archetype": "hardening",
                "title": "a hardening",
                "template_markdown": "# legacy-a-01 - a hardening\n\n## Priority scoring\n- priority_score: 5\n",
            },
            {
                "idea_id": "legacy-b-01",
                "source_file": "src/b.py",
                "archetype": "performance",
                "title": "b performance",
                "template_markdown": "# legacy-b-01 - b performance\n\n## Priority scoring\n- priority_score: 4\n",
            },
        ],
    )

    result = module.promote(
        input_path=input_jsonl,
        ideas_dir=ideas_dir,
        archive_dir=archive_dir,
        state_path=state_file,
        top_n=1,
        min_priority=1,
        max_per_source=1,
        manifest_path=manifest,
    )

    assert result["selected_count"] == 1
    promoted_file = Path(result["selected"][0]["file"])
    assert promoted_file.exists()
    content = promoted_file.read_text(encoding="utf-8")
    assert content.startswith("# idea000001 - ")


def test_promote_uses_state_for_idempotency(tmp_path: Path) -> None:
    module = _load_module()
    input_jsonl = tmp_path / "ideas.jsonl"
    ideas_dir = tmp_path / "docs" / "project" / "ideas"
    archive_dir = ideas_dir / "archive"
    state_file = tmp_path / "state.json"
    manifest = tmp_path / "manifest.json"
    archive_dir.mkdir(parents=True)

    _write_jsonl(
        input_jsonl,
        [
            {
                "idea_id": "legacy-a-01",
                "source_file": "src/a.py",
                "archetype": "hardening",
                "title": "a hardening",
                "template_markdown": "# legacy-a-01 - a hardening\n\n## Priority scoring\n- priority_score: 5\n",
            }
        ],
    )

    first = module.promote(
        input_path=input_jsonl,
        ideas_dir=ideas_dir,
        archive_dir=archive_dir,
        state_path=state_file,
        top_n=10,
        min_priority=1,
        max_per_source=1,
        manifest_path=manifest,
    )
    second = module.promote(
        input_path=input_jsonl,
        ideas_dir=ideas_dir,
        archive_dir=archive_dir,
        state_path=state_file,
        top_n=10,
        min_priority=1,
        max_per_source=1,
        manifest_path=manifest,
    )

    assert first["selected_count"] == 1
    assert second["selected_count"] == 0
