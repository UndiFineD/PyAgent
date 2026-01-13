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
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# limitations under the License.

"""Agent specializing in Markdown documentation."""

from __future__ import annotations
from src.core.base.version import VERSION
from src.logic.agents.development.CoderAgent import CoderAgent
from src.core.base.utilities import create_main_function
from src.logic.agents.cognitive.KnowledgeAgent import KnowledgeAgent
import re
import yaml

__version__ = VERSION

class MarkdownAgent(CoderAgent):
    """Agent for Markdown documentation improvement."""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self._language = "markdown"
        self._knowledge_agent = KnowledgeAgent(file_path)
        self._system_prompt = (
            "You are a Technical Writer and Obsidian Markdown Expert. "
            "Focus on clear structure, readable formatting, and consistent style. "
            "Follow Obsidian-specific Markdown conventions:\n"
            "1. Use Wikilinks [[Page Name]] for internal links and ![[Page Name]] for embedding content.\n"
            "2. Support Obsidian Callouts: > [!INFO], > [!WARNING], > [!TIP], > [!ABSTRACT], > [!TODO], > [!QUOTE], etc.\n"
            "3. Maintain and organize YAML Frontmatter (Properties) at the top of files.\n"
            "4. Support Obsidian-style tags (#tag).\n"
            "5. Support Mermaid diagrams for flowcharts, sequences, and charts.\n"
            "6. Use block references (^block-id) for granular linking and #^block-id for referencing them.\n"
            "7. Support Dataview queries (e.g., ```dataview\\nLIST FROM #tag\\n```) for dynamic content.\n"
            "8. Ensure compatibility with GitHub Flavored Markdown while prioritizing Obsidian's enhanced features."
        )

    def _get_default_content(self) -> str:
        return "---\ntags: []\n---\n# New Document\n\nStarting point for documentation.\n"

    def convert_to_wikilinks(self, content: str) -> str:
        """Converts [Text](Link.md) to [[Link|Text]] or [[Link]] if text matches."""
        # Simple regex for markdown links
        pattern = r"\[([^\]]+)\]\(([^)]+)\.md\)"
        def replace(match) -> str:
            text, link = match.groups()
            if text == link:
                return f"[[{link}]]"
            return f"[[{link}|{text}]]"
        return re.sub(pattern, replace, content)

    def format_as_callout(self, content: str, callout_type: str = "INFO", title: str = "") -> str:
        """Wraps content in an Obsidian callout block."""
        header = f"> [!{callout_type.upper()}]"
        if title:
            header += f" {title}"
        
        lines = content.strip().split("\n")
        callout_lines = [header] + [f"> {line}" for line in lines]
        return "\n".join(callout_lines)

    def ensure_frontmatter(self, content: str, default_props: dict = None) -> str:
        """Ensures the content has a YAML frontmatter block."""
        if content.startswith("---"):
            return content
        
        props = default_props or {"created": None, "tags": []}
        frontmatter = "---\n" + yaml.dump(props, sort_keys=False) + "---\n"
        return frontmatter + content

    def add_mermaid_diagram(self, diagram_type: str, diagram_definition: str) -> str:
        """Creates a Mermaid diagram block."""
        return f"```mermaid\n{diagram_type}\n{diagram_definition}\n```"

    def add_dataview_query(self, query: str) -> str:
        """Creates a Dataview query block."""
        return f"```dataview\n{query}\n```"

    def insert_knowledge_graph(self) -> str:
        """Inserts a Mermaid representation of the workspace knowledge graph."""
        graph = self._knowledge_agent.get_graph_mermaid()
        return f"\n## Workspace Knowledge Graph\n\n" + self.add_mermaid_diagram("", graph)

    def insert_backlinks(self) -> str:
        """Inserts a list of notes linking to this one."""
        backlinks = self._knowledge_agent.find_backlinks(self.file_path.name)
        if not backlinks:
            return ""
        
        links_str = "\n".join([f"- [[{Path(b).stem}]]" for b in backlinks])
        return f"\n## Backlinks\n\n{links_str}\n"

    def convert_to_callouts(self, content: str) -> str:
        """Converts leading lines like 'TODO:' or 'WARNING:' to Obsidian Callouts."""
        # Regex to match leading TODO:, WARNING:, INFO:, TIP: etc.
        pattern = r"^(TODO|WARNING|INFO|TIP|ABSTRACT|QUOTE): (.*)$"
        def replace(match) -> str:
            ctype, ctext = match.groups()
            return self.format_as_callout(ctext, ctype)
        
        # Apply line-by-line
        lines = content.split("\n")
        new_lines = []
        for line in lines:
            new_line = re.sub(pattern, replace, line, flags=re.IGNORECASE)
            new_lines.append(new_line)
        return "\n".join(new_lines)

    def improve_content(self, prompt: str) -> str:
        """Overrides improve_content to ensure Obsidian compatibility is applied."""
        # Check if user specifically wants a graph or backlinks
        enhanced_prompt = prompt
        
        if any(w in prompt.lower() for w in ["graph", "visualize", "relationships"]):
            enhanced_prompt += "\n\nNOTE: You can suggest using a Mermaid graph to visualize relationships."
            
        if "backlink" in prompt.lower():
            enhanced_prompt += "\n\nNOTE: You can suggest adding a Backlinks section."

        # Add Obsidian-specific context to the prompt
        enhanced_prompt += (
            "\n\nREMINDER: Use Obsidian-specific features where appropriate: "
            "[[wikilinks]], > [!CALLOUTS], #tags, and YAML frontmatter."
        )
        result = super().improve_content(enhanced_prompt)
        
        # Post-process to insert actual data if requested by tags in result?
        # For now, let's keep it tool-assisted or manual.
        
        return result

if __name__ == "__main__":
    main = create_main_function(MarkdownAgent, "Markdown Agent", "Path to Markdown file (.md)")
    main()