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


"""Agent specializing in automated documentation generation and maintenance."""

from __future__ import annotations
from src.core.base.lifecycle.version import VERSION
import logging
from src.core.base.lifecycle.base_agent import BaseAgent
from src.core.base.common.base_utilities import create_main_function
from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent

__version__ = VERSION


class DocumentationAgent(BaseAgent):
    """Generates technical references and project OVERVIEW documents."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.workspace_root = self.file_path.parent.parent.parent
        self.knowledge = KnowledgeAgent(
            str(self.workspace_root / "src\logic\agents\cognitive\knowledge_agent.py")
        )
        self._system_prompt = (
            "You are the Documentation Agent. "
            "Your role is to maintain clear, accurate technical documentation. "
            "You summarize code structures, explain module relationships, and ensure READMEs are current."
        )

    def _get_default_content(self) -> str:
        return "# Documentation Log\n\n## Summary\nWaiting for update...\n"

    def generate_reference(self) -> str:
        """Generates a technical reference for the src/classes/ directory."""
        self.knowledge.build_index()
        classes_dir = self.workspace_root / "src/classes"

        # Get structural briefs
        py_files = [
            str(p.relative_to(self.workspace_root))
            for p in classes_dir.rglob("*.py")
            if "__init__" not in p.name
        ]
        briefing = self.knowledge.get_compressed_briefing(
            py_files[:10]
        )  # Top 10 for summary

        doc = [
            "# Technical Reference Guide",
            "",
            "## 🏗️ Class Hierarchy & Signatures",
            "This section provides an overview of the core modular classes.",
            "",
            briefing,
            "",
            "## 🔗 Dependency Map",
            "```mermaid",
            self.knowledge.get_graph_mermaid(),
            "```",
            "",
            "---",
            f"*Generated autonomously on {logging.time.strftime('%Y-%m-%d')}*",  # type: ignore[attr-defined]
        ]

        ref_path = self.workspace_root / "docs/TECHNICAL_REFERENCE.md"
        ref_path.parent.mkdir(parents=True, exist_ok=True)
        ref_path.write_text("\n".join(doc), encoding="utf-8")

        return f"Reference documentation updated at: {ref_path}"

    def improve_content(self, prompt: str) -> str:
        """Perform documentation maintenance."""
        return self.generate_reference()


if __name__ == "__main__":
    main = create_main_function(
        DocumentationAgent, "Documentation Agent", "Task (e.g. 'generate')"
    )
    main()
