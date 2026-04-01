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
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "ProposeLegacyIdeaMerges.py"
    spec = importlib.util.spec_from_file_location("ProposeLegacyIdeaMerges", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row) + "\n")


def test_proposals_cluster_same_source_file(tmp_path: Path) -> None:
    module = _load_module()
    input_jsonl = tmp_path / "ideas.jsonl"
    output_json = tmp_path / "proposals.json"
    output_md = tmp_path / "proposals.md"

    _write_jsonl(
        input_jsonl,
        [
            {
                "idea_id": "legacy-a-01",
                "source_file": "src/a.py",
                "archetype": "hardening",
                "title": "A hardening",
                "template_markdown": "## Priority scoring\n- priority_score: 5\n",
            },
            {
                "idea_id": "legacy-a-02",
                "source_file": "src/a.py",
                "archetype": "performance",
                "title": "A performance",
                "template_markdown": "## Priority scoring\n- priority_score: 4\n",
            },
            {
                "idea_id": "legacy-b-01",
                "source_file": "src/b.py",
                "archetype": "docs",
                "title": "B docs",
                "template_markdown": "## Priority scoring\n- priority_score: 1\n",
            },
        ],
    )

    payload = module.propose_merges(
        input_path=input_jsonl,
        output_json=output_json,
        output_markdown=output_md,
        min_group_size=2,
        max_group_size=4,
        min_priority=2,
    )

    assert payload["proposal_count"] == 1
    proposal = payload["proposals"][0]
    assert proposal["source_file"] == "src/a.py"
    assert proposal["member_count"] == 2
    assert output_json.exists()
    assert output_md.exists()
