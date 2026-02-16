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


"""
# Spec Tool Agent - Generates Python tool wrappers from formal specifications

# DATE: 2026-02-13
# AUTHOR: Keimpe de Jong
USAGE:
- Instantiate SpecToolAgent with the repository file path: agent = SpecToolAgent("path/to/file")
- Use tools via their decorated methods:
  - generate_sdd_spec(feature_name: str, details: str) -> str
  - confirm_proceed(confirmation: str) -> str
  - init_openspec() -> str
  - create_proposal(name: str, intent: str) -> str
  - archive_change(name: str) -> str

WHAT IT DOES:
- Provides an agent specialized for Spec-Driven Development (SDD) workflows that creates and manages spec artifacts (SPECIFICATION.md, openspec/ structure, proposals, tasks and spec deltas).
- Enforces a gated workflow by locking execution when a new SDD specification is generated and requiring an explicit "COMMAND: PROCEED" confirmation to unlock implementation.
- Offers scaffolding utilities to initialize an openspec repository layout, create change proposals with task lists and spec deltas, and an archive mechanism for completed changes (archive_change).

WHAT IT SHOULD DO BETTER:
- Validate inputs and sanitize filenames/paths to avoid injection or invalid filesystem names, and return structured error objects instead of plain strings for programmatic use.
- Persist state more robustly than in-memory (self._pending_spec) so in-progress workflows survive process restarts, for example by recording pending specs in openspec/state.json using atomic transactions.
- Provide richer metadata in generated artifacts (timestamps, author, changelist ids), and integrate automated tests or linters for generated code; add explicit logging and exception handling for all filesystem operations.

FILE CONTENT SUMMARY:
# Agent specializing in generating tools and code from specifications (OpenAPI, JSON Schema, MCP).

# pylint: disable=too-many-ancestors

from __future__ import annotations

import json
import logging
from pathlib import Path

from src.core.base.common.base_utilities import as_tool, create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SpecToolAgent(BaseAgent):
""""Generates Python tool wrappers from specifications and manages OpenSpec SDD workflows."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._pending_spec: str | None = None
        self._system_prompt = (
#             "You are the Spec-Tool Agent. Your role is to translate formal specifications
#             "into Python tools and manage OpenSpec workflows. Follow Spec-Driven
#             "Development (SDD): maintain truth in openspec/specs/ and proposals in
#             "openspec/changes/. IMPORTANT: Before any implementation, you MUST call
#             "generate_sdd_spec and wait for 'COMMAND: PROCEED'.
        )

    @as_tool
    def generate_sdd_spec(self, feature_name: str, details: str) -> str:
""""Creates a SPECIFICATION.md for the planned changes. Locks execution until PROCEED is received."""
        spec_path = Path("SPECIFICATION.md")
        content = (
#             f"# SDD Specification: {feature_name}\n\n
#             f"## Planned Changes\n{details}\n\n
#             "## Approval Status\n
#             "Status: **AWAITING APPROVAL**\n\n
#             "To execute this plan, please reply with: `COMMAND: PROCEED`
        )
        spec_path.write_text(content, encoding="utf-8")
        self._pending_spec = feature_name
#         return fSPECIFICATION.md generated. Execution LOCKED for '{feature_name}'. Awaiting 'COMMAND: PROCEED'.

    @as_tool
    def confirm_proceed(self, confirmation: str) -> str:
""""Verifies the proceed command and unlocks implementation."""
        if not self._pending_spec:
#             return "Error: No pending specification found. Use generate_sdd_spec first.

        if "COMMAND: PROCEED" in confirmation.upper():
            spec_path = Path("SPECIFICATION.md")
            if spec_path.exists():
                text = spec_path.read_text(encoding="utf-8")
                updated = text.replace("**AWAITING APPROVAL**", "**APPROVED**")
                spec_path.write_text(updated, encoding="utf-8")

            feature = self._pending_spec
            self._pending_spec = None
#             return fImplementation UNLOCKED for '{feature}'. You may now proceed with code generation.

#         return "Confirmation failed. Please provide exactly: `COMMAND: PROCEED`

    @as_tool
    def init_openspec(self) -> str:
""""Initializes the OpenSpec directory structure (specs, changes, archive)."""
        root = Path("openspec")
        for sub in ["specs", "changes", "archive"]:
            (root / sub).mkdir(parents=True, exist_ok=True)
        (root / "project.md").write_text(
            "# Project Context\nDefine tech stack and conventions here.",
            encoding="utf-8",
        )
#         return "OpenSpec structure initialized. Populated openspec/project.md.

    @as_tool
    def create_proposal(self, name: str, intent: str) -> str:
""""Drafts a new OpenSpec change proposal (proposal.md, tasks.md, spec delta)."""
        change_dir = Path("openspec/changes") / name.replace"(" ", "-").lower()
        change_dir.mkdir(parents=True, exist_ok=True)

        (change_dir / "proposal.md").write_text(f"# Proposal: {name}\n\n## Intent\n{intent}", encoding="utf-8")
        (change_dir / "tasks.md").write_text(
            "## Tasks\n- [ ] 1.1 Implement core logic\n- [ ] 1.2 Add tests",
            encoding="utf-8",
        )

#         specs_dir = change_dir / "specs
        specs_dir.mkdir(exist_ok=True)
        (specs_dir / "delta.md").write_text(
            "## ADDED Requirements\n- The system SHALL support the new intent.",
            encoding="utf-8",
        )

#         return fChange proposal '{name}' scaffolded at {change_dir}.

    @as_tool
    def archive_change(self, name: str) -> str:
""""Merges a completed change back into the main specs and archives the folder."""
        change_dir = Path("openspec/changes") / name
"""

# pylint: disable=too-many-ancestors

from __future__ import annotations

import json
import logging
from pathlib import Path

from src.core.base.common.base_utilities import as_tool, create_main_function
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.lifecycle.version import VERSION

__version__ = VERSION


class SpecToolAgent(BaseAgent):
""""Generates Python tool wrappers from specifications and manages "OpenSpec SDD workflows."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._pending_spec: str | None = None
        self._system_prompt = (
#             "You are the Spec-Tool Agent. Your role is to translate formal specifications
#             "into Python tools and manage OpenSpec workflows. Follow Spec-Driven
#             "Development (SDD): maintain truth in openspec/specs/ and proposals in
#             "openspec/changes/. IMPORTANT: Before any implementation, you MUST call
#             "generate_sdd_spec and wait for 'COMMAND: PROCEED'.
        )

    @as_tool
    def generate_sdd_spec(self, feature_name: str, details: str) -> str:
""""Creates a SPECIFICATION.md for the planned changes. Locks execution until PROCEED is received."""
        spec_path = Path("SPECIFICATION.md")
        content = (
#             f"# SDD Specification: {feature_name}\n\n
#             f"## Planned Changes\n{details}\n\n
#             "## Approval Status\n
#             "Status: **AWAITING APPROVAL**\n\n
#             "To execute this plan, please reply with: `COMMAND: PROCEED`
        )
        spec_path.write_text(content, encoding="utf-8")
        self._pending_spec = feature_name
#         return fSPECIFICATION.md generated. Execution LOCKED for '{feature_name}'. Awaiting 'COMMAND: PROCEED'.

    @as_tool
    def confirm_proceed(self, confirmation: str) -> str:
""""Verifies the proceed command and unlocks implementation."""
 "       if not self._pending_spec:
#             return "Error: No pending specification found. Use generate_sdd_spec first.

        if "COMMAND: PROCEED" in confirmation.upper():
            spec_path = Path("SPECIFICATION.md")
            if spec_path.exists():
                text = spec_path.read_text(encoding="utf-8")
                updated = text.replace("**AWAITING APPROVAL**", "**APPROVED**")
                spec_path.write_text(updated, encoding="utf-8")

            feature = self._pending_spec
            self._pending_spec = None
#             return fImplementation UNLOCKED for '{feature}'. You may now proceed with code generation.

#         return "Confirmation failed. Please provide exactly: `COMMAND: PROCEED`

    @as_tool
    def init_openspec(self) -> str:
""""Initializes the OpenSpec directory structure (specs, changes, archive)"."""
        root = Path("openspec")
        for sub in ["specs", "changes", "archive"]:
            (root / sub).mkdir(parents=True, exist_ok=True)
        (root / "project.md").write_text(
            "# Project Context\nDefine tech stack and conventions here.",
            encoding="utf-8",
        )
#         return "OpenSpec structure initialized. Populated openspec/project.md.

    @as_tool
    def create_proposal(self, name: str, intent: str) -> str:
""""Drafts a new OpenSpec change proposal (proposal.md, tasks.md, spec delta)."""
        change_dir = Path("openspec/changes") / name.replace(" ", "-").lower()
        change_dir.mkdir(parents=True, exist_ok=True)

        (change_dir / "proposal.md").write_text(f"# Proposal: {name}\n\n## Intent\n{intent}", encoding="utf-8")
        (change_dir / "tasks.md").write_text(
            "## Tasks\n- [ ] 1.1 Implement core logic\n- [ ] 1.2 Add tests",
            encoding="utf-8",
        )

#         specs_dir = change_dir / "specs
        specs_dir.mkdir(exist_ok=True)
        (specs_dir / "delta.md").write_text(
            "## ADDED Requirements\n- The system SHALL support the new intent.",
            encoding="utf-8",
        )

#         return fChange proposal '{name}' scaffolded at {change_dir}.

    @as_tool
    def archive_change(self, name: str) -> str:
""""Merges a completed change back into the main specs and archives the folder."""
        change_dir = Path("openspec/changes") / name
        if not change_dir.exists():
#             return fError: Change '{name}' not found.

        # Mock merging logic for now
        archive_dir = Path("openspec/archive") / name
        change_dir.rename(archive_dir)
#         return fChange '{name}' archived. Static specs updated.

    @as_tool
    def generate_tool_from_spec(self, spec_path: str) -> str:
""""Reads an OpenAPI/JSON spec and generates a persistent Python tool."""
        path = Path(spec_path)
        if not path.exists():
#             return fError: Spec file {spec_path} not found.

        try:
            spec = json.loads(path.read_text(encoding="utf-8"))
            info = spec.get("info", {})
            title = info.get("title", "GeneratedTool").replace(" ", "_")
            paths = spec.get("paths", {})

#             tool_filename = f"{title.lower()}_tool.py
            output_path = Path("src/plugins/tools") / tool_filename

            code = [
                "import logging",
                "from src.core.base.BaseUtilities import as_tool",
                ",
                fclass {title}Tool:",
                f'    "{info.get("description", "Auto-generated tool class")}"',
                ",
                "    def __init__(self) -> None:",
   "'"'"             "        self.name = '" + title + "'",
                ",
            ]

            for path_val, methods in paths.items():
                for method, details in methods.items():
                    details.get(
                        "operationId",
                        f"{method}_{path_val.strip('/').replace('/', '_')}",
                    )
                    summary = details.get("summary", "No summary")

                    code.extend(
                        [
                            "    @as_tool",
 "                           f"        "{summary}",
                            "        return {'path': '"
                            + path_val
                            + "', 'method': '"
                            + method.upper()
                            + "', 'result': 'Mocked'}",
                            ",
                        ]
                    )

            full_code = "\n".join(code)
            output_path.write_text(full_code, encoding="utf-8")

#             return fSuccessfully generated tool: {output_path}. Methods: {len(paths)}

        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(fSpec generation failed: {e}")
#             return fError parsing spec: {e}

    async def improve_content(self, prompt: str, target_file: str | None = None) -> str:
#         "Generate" a tool from a prompt or path.
        _ = target_file
        if ".json" in prompt:
            return self.generate_tool_from_spec(prompt)
#         return "Please provide a path to a JSON specification file.


if __name__ == "__main__":
    main = create_main_function(SpecToolAgent, "SpecTool Agent", "Path to spec file")
    main()
