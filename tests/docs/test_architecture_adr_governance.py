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

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
ADR_DIR = REPO_ROOT / "docs" / "architecture" / "adr"
TEMPLATE = ADR_DIR / "0001-architecture-decision-record-template.md"
REQUIRED_SECTIONS = [
    "## Status",
    "## Date",
    "## Owners",
    "## Context",
    "## Decision",
    "## Alternatives considered",
    "## Consequences",
    "## Implementation impact",
    "## Validation and monitoring",
    "## Related links",
]


def _adr_files() -> list[Path]:
    return sorted([p for p in ADR_DIR.glob("*.md") if re.match(r"^\d{4}-.+\.md$", p.name)])


def test_adr_directory_and_template_exist() -> None:
    assert ADR_DIR.exists(), f"Missing ADR directory: {ADR_DIR}"
    assert TEMPLATE.exists(), f"Missing ADR template: {TEMPLATE}"


def test_adr_numbering_is_sequential_without_gaps() -> None:
    files = _adr_files()
    numbers = []
    for path in files:
        m = re.match(r"^(\d{4})-", path.name)
        assert m is not None, f"Invalid ADR filename: {path.name}"
        numbers.append(int(m.group(1)))

    assert numbers, "No ADR files found"
    assert min(numbers) == 1, f"ADR sequence must start at 0001, found {min(numbers):04d}"

    for prev, cur in zip(sorted(numbers), sorted(numbers)[1:], strict=False):
        assert cur == prev + 1, f"ADR numbering gap detected: {prev:04d} -> {cur:04d}"


def test_non_template_adrs_have_required_sections() -> None:
    for path in _adr_files():
        if path.name.startswith("0001-"):
            continue
        text = path.read_text(encoding="utf-8")
        for section in REQUIRED_SECTIONS:
            assert section in text, f"{path.name} missing required section: {section}"
