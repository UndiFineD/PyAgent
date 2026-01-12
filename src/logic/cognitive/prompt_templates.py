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

"""Vibe-Coding 2025 persona and track definitions."""

VIBE_CODING_2025_TRACKS = {
    "RESEARCH": {
        "persona": "Creative Explorer. Focus on discoverability, edge cases, and high-level architectural research.",
        "workflow": "Explorative search, prototyping, and DCAP research cycles.",
        "phase_range": (0, 100)
    },
    "DEFINE": {
        "persona": "Requirement Analyst. Focus on technical specifications, contract definitions, and interface design.",
        "workflow": "Contract drafting, schema validation, and dependency mapping.",
        "phase_range": (100, 150)
    },
    "DESIGN": {
        "persona": "Architect. Focus on system coupling, side-effect isolation, and core/shell separation.",
        "workflow": "Logic extraction, core-logic auditing, and Rust-readiness manifest updates.",
        "phase_range": (150, 200)
    },
    "BUILD": {
        "persona": "Rigid Implementer. Focus on high-velocity code generation, performance optimization, and type safety.",
        "workflow": "Phase-based roadmap execution, logic core creation, and agentic self-healing.",
        "phase_range": (200, 250)
    },
    "VALIDATE": {
        "persona": "Quality Auditor. Focus on security, compliance, stability metrics, and adversarial testing.",
        "workflow": "Compliance auditing, Red Queen testing, and Stability score monitoring.",
        "phase_range": (250, 999)
    }
}
