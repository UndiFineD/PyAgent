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

"""Unit tests for KnowledgeGraph and KnowledgeAgent indexing."""

from typing import List
from src.logic.agents.cognitive.knowledge_agent import KnowledgeAgent
from pathlib import Path
import logging


def test_knowledge_graph() -> None:
    logging.basicConfig(level=logging.INFO)
    # Create some dummy notes for testing links
    note1 = Path("Note1.md")
    note2 = Path("Note2.md")

    note1.write_text("# Note 1\nLink to [[Note2]]", encoding="utf-8")

    note2.write_text("# Note 2\nBacklink here", encoding="utf-8")

    ka = KnowledgeAgent(Path("."))
    ka.build_index()

    backlinks: List[str] = ka.find_backlinks("Note2.md")
    print(f"Backlinks for Note2: {backlinks}")
    assert "Note1.md" in backlinks

    mermaid: str = ka.get_graph_mermaid()
    print(f"Mermaid Graph:\n{mermaid}")
    assert "Note1 --> Note2" in mermaid

    # Cleanup

    note1.unlink()
    note2.unlink()
    if ka.index_file.exists():
        ka.index_file.unlink()


if __name__ == "__main__":
    try:
        test_knowledge_graph()
        print("\nKnowledgeAgent Graph/Backlinks Sanity Check: PASSED")
    except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
        print(f"\nKnowledgeAgent Graph/Backlinks Sanity Check: FAILED: {e}")
        import traceback

        traceback.print_exc()
