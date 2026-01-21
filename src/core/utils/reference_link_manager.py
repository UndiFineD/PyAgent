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


"""Auto-extracted class from agent_changes.py"""

from __future__ import annotations
from src.core.base.version import VERSION
from src.core.base.types import linked_reference

__version__ = VERSION


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
        self.references: dict[str, list[LinkedReference]] = {}

    def add_commit_reference(
        self, entry_id: str, commit_sha: str, url: str = "", title: str = ""
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
            ref_type="commit", ref_id=commit_sha[:7], url=url, title=title
        )
        if entry_id not in self.references:
            self.references[entry_id] = []
        self.references[entry_id].append(ref)
        return ref

    def add_issue_reference(
        self, entry_id: str, issue_number: str, url: str = "", title: str = ""
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
            ref_type="issue", ref_id=f"#{issue_number}", url=url, title=title
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
        return (
            " ("
            + ", ".join(f"[{r.ref_id}]({r.url})" if r.url else r.ref_id for r in refs)
            + ")"
        )
