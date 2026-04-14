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

"""Documentation consistency checks for FLM naming."""

from pathlib import Path


def test_flm_docs_use_fastflow_expansion() -> None:
    """FLM docs in this scope should use Fastflow wording."""
    design_path = Path("docs/project/prj0000041/brainstorm.md")
    plan_path = Path("docs/project/prj0000041/plan.md")

    design = design_path.read_text(encoding="utf-8")
    plan = plan_path.read_text(encoding="utf-8")

    assert "Fastflow Language Model" in design
    assert "Fastflow Language Model" in plan
