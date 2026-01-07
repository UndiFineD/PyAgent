#!/usr/bin/env python3

"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations

from .LinkedReference import LinkedReference

from base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, List, Any, Tuple
import hashlib
import json
import logging
import re

class ReferenceLinkManager:
    """Manages links to commits and issues in changelog entries.

    Provides functionality to add, validate, and format references
    to commits and issues.

    Attributes:
        references: Dictionary of references by entry ID.

    Example:
        >>> manager=ReferenceLinkManager()
        >>> manager.add_commit_reference("entry1", "abc123", "https://github.com/...")
    """

    def __init__(self) -> None:
        """Initialize the reference link manager."""
        self.references: Dict[str, List[LinkedReference]] = {}

    def add_commit_reference(
        self,
        entry_id: str,
        commit_sha: str,
        url: str = "",
        title: str = ""
    ) -> LinkedReference:
        """Add a commit reference to an entry.

        Args:
            entry_id: ID of the changelog entry.
            commit_sha: Git commit SHA.
            url: URL to the commit.
            title: Commit message / title.

        Returns:
            The created LinkedReference.
        """
        ref = LinkedReference(
            ref_type="commit",
            ref_id=commit_sha[:7],
            url=url,
            title=title
        )
        if entry_id not in self.references:
            self.references[entry_id] = []
        self.references[entry_id].append(ref)
        return ref

    def add_issue_reference(
        self,
        entry_id: str,
        issue_number: str,
        url: str = "",
        title: str = ""
    ) -> LinkedReference:
        """Add an issue reference to an entry.

        Args:
            entry_id: ID of the changelog entry.
            issue_number: Issue number.
            url: URL to the issue.
            title: Issue title.

        Returns:
            The created LinkedReference.
        """
        ref = LinkedReference(
            ref_type="issue",
            ref_id=f"#{issue_number}",
            url=url,
            title=title
        )
        if entry_id not in self.references:
            self.references[entry_id] = []
        self.references[entry_id].append(ref)
        return ref

    def format_references(self, entry_id: str) -> str:
        """Format references for display.

        Args:
            entry_id: ID of the changelog entry.

        Returns:
            Formatted string of references.
        """
        refs = self.references.get(entry_id, [])
        if not refs:
            return ""
        return " (" + ", ".join(f"[{r.ref_id}]({r.url})" if r.url else r.ref_id for r in refs) + ")"
