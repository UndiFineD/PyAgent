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

"""Red-phase documentation contracts for prj0000118 AMD NPU guidance."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
HARDWARE_ACCELERATION_DOC = REPO_ROOT / "docs/performance/HARDWARE_ACCELERATION.md"


def _read_hardware_doc() -> str:
    """Return the full hardware acceleration document text."""
    return HARDWARE_ACCELERATION_DOC.read_text(encoding="utf-8")


def _normalize(text: str) -> str:
    """Normalize text for stable phrase matching in contract assertions."""
    return " ".join(text.lower().replace("`", "").split())


def test_ac_amd_001_requires_canonical_runtime_guidance_marker() -> None:
    """Assert AC-AMD-001 by requiring an explicit canonical amd_npu guidance marker."""
    raw = _read_hardware_doc()
    normalized = _normalize(raw)

    assert "## canonical amd npu runtime guidance" in normalized
    assert "this section is the canonical runtime guidance location for amd_npu" in normalized


def test_ac_amd_002_requires_feature_off_and_feature_on_command_examples() -> None:
    """Assert AC-AMD-002 by requiring both feature-off and feature-on command forms."""
    raw = _read_hardware_doc()

    assert "cargo run --bin pyagent_cli -- amd-npu-status" in raw
    assert "cargo run --features amd_npu --bin pyagent_cli -- amd-npu-status" in raw


def test_ac_amd_003_requires_unavailable_status_minus_one_semantics() -> None:
    """Assert AC-AMD-003 by requiring explicit -1 unavailable fallback semantics."""
    normalized = _normalize(_read_hardware_doc())

    assert "amd_npu_status_unavailable" in normalized
    assert "-1" in normalized
    assert "safe interpretation" in normalized


def test_ac_amd_004_requires_supported_environment_boundary_and_unsupported_paths() -> None:
    """Assert AC-AMD-004 by requiring explicit supported and unsupported environment boundaries."""
    normalized = _normalize(_read_hardware_doc())

    assert "windows x86_64" in normalized
    assert "amd ryzen ai sdk" in normalized
    assert "unsupported paths" in normalized


def test_ac_amd_005_requires_mandatory_evidence_schema_fields() -> None:
    """Assert AC-AMD-005 by requiring mandatory validation evidence schema fields."""
    normalized = _normalize(_read_hardware_doc())

    required_fields = [
        "evidence schema",
        "command",
        "exit status",
        "observed outcome",
        "runner context",
        "all fields are mandatory",
    ]
    for field in required_fields:
        assert field in normalized, f"Missing mandatory evidence field phrase: {field}"


def test_ac_amd_006_requires_non_goals_and_ci_defer_contract() -> None:
    """Assert AC-AMD-006 by requiring explicit non-goals and CI defer contract text."""
    normalized = _normalize(_read_hardware_doc())

    assert "non-goals" in normalized
    assert "ci defer contract" in normalized
    assert "deferred from ci automation" in normalized
