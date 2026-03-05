# Copyright 2026 PyAgent Authors
# Assistant for managing the knowledge graph and impact radius.

from typing import Set

class KnowledgeGraphAssistant:
    """Handles backlinks, dependency tracking, and graph visualization."""

    def __init__(self, workspace_root: str):
        self.workspace_root = workspace_root

    def get_impact_radius(self, query: str) -> Set[str]:
        """Calculates which modules might be impacted by a change."""
        return set()

    def find_backlinks(self, target_file: str, index: dict[str, list[str]]) -> list[str]:
        """Finds all files in the index that reference the target_file."""
        backlinks = []
        target_name = target_file.split(".")[0]  # Support WikiStyle [[Note]] matches [[Note.md]]
        for source_file, symbols in index.items():
            for symbol in symbols:
                if symbol == target_file or symbol == target_name:
                    backlinks.append(source_file)
        return backlinks

    def generate_mermaid(self, index: dict[str, list[str]]) -> str:
        """Exports the current knowledge graph as a Mermaid string."""
        from pathlib import Path
        lines = ["graph TD"]
        # Track edge combinations to prevent duplicates
        edges = set()
        for source, targets in index.items():
            s_name = Path(source).stem
            for target in targets:
                t_name = Path(target).stem
                edge = f"  {s_name} --> {t_name}"
                if edge not in edges:
                    lines.append(edge)
                    edges.add(edge)
        return "\n".join(lines)

    def generate_mermaid_graph(self) -> str:
        """Compatibility wrapper."""
        return self.generate_mermaid({})
        """Exports the current knowledge graph as a Mermaid string."""
        return "graph TD\n  A[Workspace] --> B[src]"
