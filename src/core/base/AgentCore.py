#!/usr/bin/env python3

"""
AgentCore: Pure logic component for the Agent system.
Handles data transformation, parsing, and decision-making without IO side-effects.
Ready for conversion to a Rust library with strong typing.
"""

import re
from typing import List, Dict, Any, Optional
from src.core.base.core import BaseCore

class AgentCore(BaseCore):
    """Logic-only core for managing improvement tasks and state."""

    def __init__(self, workspace_root: Optional[str] = None, settings: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(workspace_root=workspace_root)
        self.settings = settings or {}

    def parse_improvements_content(self, content: str) -> List[str]:
        """
        Parses the content of an improvement markdown file and returns pending items.
        Side-effect free: takes string, returns list.
        """
        if not content:
            return []
            
        lines = content.splitlines()
        pending: List[str] = []
        
        # Match "1. ", "1) ", "- [ ]", "- ", "* "
        list_pattern = re.compile(r'^(\d+[\.\)]|\*|\-)\s+(\[ \]\s+)?(.*)')

        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue

            # Skip explicitly checked or fixed items
            if '[x]' in stripped or '[Fixed]' in stripped:
                continue

            match = list_pattern.match(stripped)
            if match:
                item_text = match.group(3).strip()
                # Filter out obvious headers or non-tasks
                if item_text.lower().startswith('current strengths'):
                    continue
                if len(item_text) > 5:
                    pending.append(item_text)
                    
        return pending

    def update_fixed_items(self, content: str, fixed_items: List[str]) -> str:
        """
        Calculates the new content for an improvements file with fixed items marked.
        """
        if not content or not fixed_items:
            return content
            
        lines = content.splitlines()
        new_lines: List[str] = []
        
        for line in lines:
            updated = False
            for item in fixed_items:
                if item in line:
                    if '- [ ]' in line:
                        new_lines.append(line.replace('- [ ]', '- [x]'))
                        updated = True
                        break
                    elif '[x]' not in line and '[Fixed]' not in line:
                        new_lines.append(line + " [Fixed]")
                        updated = True
                        break
            if not updated:
                new_lines.append(line)
                
        return '\n'.join(new_lines) + '\n'

    def generate_changelog_entries(self, fixed_items: List[str]) -> str:
        """
        Generates changelog snippet for fixed items.
        """
        if not fixed_items:
            return ""
        return "\n".join([f"- Fixed: {item}" for item in fixed_items])

    def score_improvement_items(self, items: List[str]) -> List[str]:
        """
        Heuristic-based scoring to prioritize items.
        Currently simple FIFO, but can be expanded with complex logic.
        """
        # Example criteria: prioritize 'security', 'bug', 'crash'
        prioritized = []
        remaining = []
        
        for item in items:
            it_low = item.lower()
            if any(word in it_low for word in ['security', 'vulnerability', 'crash', 'critical']):
                prioritized.append(item)
            else:
                remaining.append(item)
                
        return prioritized + remaining

    def get_agent_command(self, python_exe: str, script_name: str, context_file: str, prompt: str, strategy: str) -> List[str]:
        """
        Pure logic for generating agent execution commands.
        """
        import sys
        from pathlib import Path
        
        # Calculate script path logic (pure path manipulation)
        # Note: script_name is like 'agent_errors.py'
        
        # We assume the script is in the root's parent of classes (src/)
        # But since this is pure logic, we just return the calculated list.
        return [
            python_exe,
            script_name,
            '--context', context_file,
            '--prompt', prompt,
            '--strategy', strategy
        ]
