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
from pathlib import Path


def _load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "GenerateLegacyIdeas.py"
    spec = importlib.util.spec_from_file_location("GenerateLegacyIdeas", module_path)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_generator_excludes_dot_directories_and_limits_ideas(tmp_path: Path) -> None:
    module = _load_module()
    legacy = tmp_path / "legacy"
    (legacy / "src").mkdir(parents=True)
    (legacy / ".git" / "objects").mkdir(parents=True)

    (legacy / "src" / "app.py").write_text("def hello():\n    return 1\n", encoding="utf-8")
    (legacy / ".git" / "objects" / "ignored.py").write_text("def bad():\n    return 2\n", encoding="utf-8")

    payload = module.generate_ideas(
        legacy_root=legacy,
        max_ideas_per_file=10,
        offset=0,
        limit=None,
        max_file_bytes=2048,
    )

    assert payload["processed_file_count"] == 1
    assert payload["idea_count"] == 10
    assert all(item["source_file"] == "src/app.py" for item in payload["ideas"])


def test_generated_idea_contains_template_sections(tmp_path: Path) -> None:
    module = _load_module()
    legacy = tmp_path / "legacy"
    (legacy / "docs").mkdir(parents=True)
    (legacy / "docs" / "guide.md").write_text("# guide\n\nTODO: improve\n", encoding="utf-8")

    payload = module.generate_ideas(
        legacy_root=legacy,
        max_ideas_per_file=3,
        offset=0,
        limit=1,
        max_file_bytes=2048,
    )

    assert payload["idea_count"] == 3
    sample = payload["ideas"][0]["template_markdown"]
    assert "## Problem statement" in sample
    assert "## Validation commands" in sample
    assert "## Readiness status" in sample
    assert "## Source references" in sample


def test_batch_window_controls_file_selection(tmp_path: Path) -> None:
    module = _load_module()
    legacy = tmp_path / "legacy"
    (legacy / "src").mkdir(parents=True)

    for idx in range(5):
        (legacy / "src" / f"file_{idx}.py").write_text("def x():\n    return 1\n", encoding="utf-8")

    payload = module.generate_ideas(
        legacy_root=legacy,
        max_ideas_per_file=2,
        offset=1,
        limit=2,
        max_file_bytes=2048,
    )

    assert payload["available_file_count"] == 5
    assert payload["processed_file_count"] == 2
    assert payload["idea_count"] == 4


def test_write_jsonl_split_creates_one_file_per_source(tmp_path: Path) -> None:
    module = _load_module()
    legacy = tmp_path / "legacy"
    (legacy / "src" / "sub").mkdir(parents=True)

    (legacy / "src" / "alpha.py").write_text("def a(): pass\n", encoding="utf-8")
    (legacy / "src" / "sub" / "beta.py").write_text("def b(): pass\n", encoding="utf-8")

    payload = module.generate_ideas(
        legacy_root=legacy,
        max_ideas_per_file=2,
        offset=0,
        limit=None,
        max_file_bytes=1024,
    )

    output_dir = tmp_path / "split_out"
    written = module._write_jsonl_split(output_dir, payload)

    # One output file per unique source_file
    assert len(written) == 2

    alpha_out = output_dir / "src" / "alpha.jsonl"
    beta_out = output_dir / "src" / "sub" / "beta.jsonl"
    assert alpha_out.exists()
    assert beta_out.exists()

    # Each file only contains ideas for its source
    import json as _json

    alpha_ideas = [_json.loads(line) for line in alpha_out.read_text(encoding="utf-8").splitlines()]
    beta_ideas = [_json.loads(line) for line in beta_out.read_text(encoding="utf-8").splitlines()]
    assert all(item["source_file"] == "src/alpha.py" for item in alpha_ideas)
    assert all(item["source_file"] == "src/sub/beta.py" for item in beta_ideas)


def test_write_manifest_includes_split_metadata(tmp_path: Path) -> None:
    module = _load_module()
    legacy = tmp_path / "legacy"
    (legacy / "src").mkdir(parents=True)
    (legacy / "src" / "foo.py").write_text("def foo(): pass\n", encoding="utf-8")

    payload = module.generate_ideas(
        legacy_root=legacy,
        max_ideas_per_file=1,
        offset=0,
        limit=None,
        max_file_bytes=1024,
    )

    import json as _json

    output_dir = tmp_path / "split_out"
    written = module._write_jsonl_split(output_dir, payload)

    manifest_path = tmp_path / "manifest.json"
    module._write_manifest(manifest_path, payload, split_files=written)

    manifest = _json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "split_output_file_count" in manifest
    assert manifest["split_output_file_count"] == 1
    assert "split_output_files" in manifest
    assert len(manifest["split_output_files"]) == 1
