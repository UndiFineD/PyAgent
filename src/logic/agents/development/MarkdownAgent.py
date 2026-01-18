#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Recovered and standardized for Phase 317

"""
The gh-copilot extension has been deprecated in favor of the newer GitHub Copilot CLI.

For more information, visit:
- Copilot CLI: https://github.com/github/copilot-cli
- Deprecation announcement: https://github.blog/changelog/2025-09-25-upcoming-deprecation-of-gh-copilot-cli-extension

No commands will be executed.
"""

from __future__ import annotations
from src.core.base.Version import VERSION
from src.core.base.BaseAgent import BaseAgent
import logging

__version__ = VERSION

class MarkdownAgent(BaseAgent):
    """
    MarkdownAgent specializing in technical documentation and markdown optimization.
    """
    def __init__(self, file_path: str, **kwargs) -> None:
        super().__init__(file_path, **kwargs)
        self._system_prompt = (
            "You are a Markdown specialist. Your goal is to optimize documentation, "
            "ensure technical accuracy, and maintain style consistency in .md files."
        )

    def _get_default_content(self) -> str:
        return "# New Documentation\n\nContent pending..."

