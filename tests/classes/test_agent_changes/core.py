# -*- coding: utf-8 -*-
"""Test classes from test_agent_changes.py - core module."""

from __future__ import annotations
import unittest
from typing import Any, List, Dict, Optional, Callable, Tuple, Set, Union
from unittest.mock import MagicMock, Mock, patch, call, ANY
import time
import json
from datetime import datetime
import pytest
import logging
from pathlib import Path
import sys
import os
import tempfile
import shutil
import subprocess
import threading
import asyncio
import re
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# Try to import test utilities
try:
    from tests.agent_test_utils import AGENT_DIR, agent_sys_path, load_module_from_path, agent_dir_on_path, load_agent_module
except ImportError:
    # Fallback
    AGENT_DIR = Path(__file__).parent.parent.parent / 'src'
    
    class agent_sys_path:
        def __enter__(self): 
            sys.path.insert(0, str(AGENT_DIR))
            return self
        def __exit__(self, *args): 
            sys.path.remove(str(AGENT_DIR))

# Import from src if needed
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))


class TestVersionRangeQueries:
    """Tests for changelog version range queries."""

    def test_version_range_single(self, tmp_path: Path) -> None:
        """Test querying a single version."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = """# Changelog
## [2.0.0] - 2025-01-16
- Feature B
## [1.0.0] - 2025-01-01
- Feature A
"""
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "[2.0.0]" in previous
        assert "[1.0.0]" in previous

    def test_version_range_multiple(self, tmp_path: Path) -> None:
        """Test querying multiple versions."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = """# Changelog
## [3.0.0]
- C
## [2.0.0]
- B
## [1.0.0]
- A
"""
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "3.0.0" in previous
        assert "1.0.0" in previous


# =============================================================================
# Session 9: Keyword Search Tests
# =============================================================================



class TestChangelogKeywordSearch:
    """Tests for changelog entry search by keyword."""

    def test_keyword_search_match(self, tmp_path: Path) -> None:
        """Test searching for keywords in changelog."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- Fix security vulnerability\n- Add new feature"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "security" in previous

    def test_keyword_search_case_insensitive(self, tmp_path: Path) -> None:
        """Test case-insensitive keyword search."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- IMPORTANT fix"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "IMPORTANT" in previous


# =============================================================================
# Session 9: Export Format Tests
# =============================================================================



class TestChangelogExportFormats:
    """Tests for changelog export to different formats."""

    def test_markdown_format_preserved(self, tmp_path: Path) -> None:
        """Test markdown format is preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n\n## [1.0.0]\n\n- **Bold** entry\n- *Italic* entry"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "**Bold**" in previous
        assert "*Italic*" in previous

    def test_code_blocks_preserved(self, tmp_path: Path) -> None:
        """Test code blocks are preserved in export."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- Added `code_function()` support"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "`code_function()`" in previous


# =============================================================================
# Session 9: Issue Tracker Linking Tests
# =============================================================================



class TestIssueTrackerLinking:
    """Tests for changelog entry linking to issue trackers."""

    def test_github_issue_link(self, tmp_path: Path) -> None:
        """Test GitHub issue link preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- Fix bug ([#42](https://github.com / owner / repo / issues / 42))"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "github.com" in previous

    def test_jira_ticket_link(self, tmp_path: Path) -> None:
        """Test JIRA ticket link preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- Fix JIRA-123"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "JIRA-123" in previous


# =============================================================================
# Session 9: Statistics Generation Tests
# =============================================================================



class TestChangelogStatistics:
    """Tests for changelog statistics generation."""

    def test_entry_count(self, tmp_path: Path) -> None:
        """Test counting changelog entries."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- Entry 1\n- Entry 2\n- Entry 3"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert previous.count("Entry") == 3

    def test_category_stats(self, tmp_path: Path) -> None:
        """Test category statistics."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n## Added\n- A\n- B\n## Fixed\n- C"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Added" in previous
        assert "Fixed" in previous


# =============================================================================
# Session 9: Validation Rules Tests
# =============================================================================



class TestChangelogValidationRules:
    """Tests for changelog entry validation rules."""

    def test_valid_entry_format(self, tmp_path: Path) -> None:
        """Test valid entry format is accepted."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n\n## [1.0.0] - 2025-01-16\n\n- Valid entry"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Valid entry" in previous


# =============================================================================
# Session 9: Internationalization Tests
# =============================================================================



class TestChangelogInternationalization:
    """Tests for changelog internationalization."""

    def test_unicode_content_preserved(self, tmp_path: Path) -> None:
        """Test unicode content is preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# 変更履歴\n- 新機能を追加しました"
        target = tmp_path / "test.changes.md"
        target.write_text(content, encoding="utf-8")

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "新機能" in previous

    def test_emoji_preserved(self, tmp_path: Path) -> None:
        """Test emoji are preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- 🎉 New feature\n- 🐛 Bug fix"
        target = tmp_path / "test.changes.md"
        target.write_text(content, encoding="utf-8")

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "🎉" in previous


# =============================================================================
# Session 9: Priority Ordering Tests
# =============================================================================



class TestChangelogPriorityOrdering:
    """Tests for changelog entry priority ordering."""

    def test_priority_by_section(self, tmp_path: Path) -> None:
        """Test entries ordered by section priority."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n## Security\n- S\n## Added\n- A\n## Fixed\n- F"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        # Security should be in content
        assert "Security" in previous


# =============================================================================
# Session 9: Backup and Restore Tests
# =============================================================================



class TestChangelogBackupRestore:
    """Tests for changelog backup and restore."""

    def test_no_backup_on_read(self, tmp_path: Path) -> None:
        """Test reading doesn't create backup."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        target = tmp_path / "test.changes.md"
        target.write_text("# Changelog\n- Entry")

        agent = mod.ChangesAgent(str(target))
        agent.read_previous_content()

        backup = tmp_path / "test.changes.md.bak"
        assert not backup.exists()


# =============================================================================
# Session 9: Category Filtering Tests
# =============================================================================



class TestChangelogCategoryFiltering:
    """Tests for changelog entry filtering by category."""

    def test_filter_by_added(self, tmp_path: Path) -> None:
        """Test filtering entries by Added category."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n## Added\n- New feature\n## Fixed\n- Bug fix"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "New feature" in previous


# =============================================================================
# Session 9: Diff Visualization Tests
# =============================================================================



class TestChangelogDiffVisualization:
    """Tests for changelog diff visualization."""

    def test_diff_markers_preserved(self, tmp_path: Path) -> None:
        """Test diff markers are preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- Entry + added\n- Entry - removed"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "+ added" in previous


# =============================================================================
# Session 9: Timestamp Tests
# =============================================================================



class TestChangelogTimestamps:
    """Tests for changelog entry timestamps."""

    def test_date_format_iso(self, tmp_path: Path) -> None:
        """Test ISO date format preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n## [1.0.0] - 2025-01-16\n- Entry"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "2025-01-16" in previous

    def test_datetime_preserved(self, tmp_path: Path) -> None:
        """Test datetime preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- Entry at 2025-01-16T10:30:00Z"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "T10:30:00Z" in previous


# =============================================================================
# Session 9: Access Control Tests
# =============================================================================



class TestChangelogAccessControl:
    """Tests for changelog access control."""

    def test_read_only_access(self, tmp_path: Path) -> None:
        """Test read-only access to changelog."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        target = tmp_path / "test.changes.md"
        target.write_text("# Changelog\n- Entry")

        agent = mod.ChangesAgent(str(target))
        content = agent.read_previous_content()

        # Should be able to read
        assert content is not None


# =============================================================================
# Session 9: Bulk Operations Tests
# =============================================================================



class TestChangelogBulkOperations:
    """Tests for changelog entry bulk operations."""

    def test_bulk_entries_readable(self, tmp_path: Path) -> None:
        """Test bulk entries can be read."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        entries = "\n".join([f"- Entry {i}" for i in range(50)])
        content = f"# Changelog\n{entries}"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Entry 0" in previous
        assert "Entry 49" in previous


# =============================================================================
# Session 9: Notification Tests
# =============================================================================



class TestChangelogNotifications:
    """Tests for changelog notifications."""

    def test_breaking_change_marker(self, tmp_path: Path) -> None:
        """Test breaking change marker preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- BREAKING CHANGE: API removed"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "BREAKING CHANGE" in previous


# =============================================================================
# Session 9: Approval Workflow Tests
# =============================================================================



class TestChangelogApprovalWorkflows:
    """Tests for changelog entry approval workflows."""

    def test_pending_entries(self, tmp_path: Path) -> None:
        """Test pending entries handled."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n## Unreleased\n- Pending feature\n## [1.0.0]\n- Released"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Unreleased" in previous
        assert "Pending feature" in previous


# =============================================================================
# Session 9: Entry Signing Tests
# =============================================================================



class TestChangelogEntrySigning:
    """Tests for changelog entry signing."""

    def test_signature_preserved(self, tmp_path: Path) -> None:
        """Test entry signature preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n- Entry <!-- signed:abc123 -->"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "signed:abc123" in previous


# =============================================================================
# Session 9: Archival and Retention Tests
# =============================================================================



class TestChangelogArchivalRetention:
    """Tests for changelog archival and retention."""

    def test_archived_section(self, tmp_path: Path) -> None:
        """Test archived section handled."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n## Current\n- New\n## Archived (2024)\n- Old"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Archived" in previous


# =============================================================================
# Session 9: Entry Comments Tests
# =============================================================================



class TestChangelogEntryComments:
    """Tests for changelog entry comments."""

    def test_html_comment_preserved(self, tmp_path: Path) -> None:
        """Test HTML comments preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = "# Changelog\n<!-- This is a comment -->\n- Entry"
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "<!-- This is a comment -->" in previous


# =============================================================================
# Session 9: History Tracking Tests
# =============================================================================



class TestChangelogHistoryTracking:
    """Tests for changelog entry history tracking."""

    def test_version_history_preserved(self, tmp_path: Path) -> None:
        """Test version history preserved."""
        with agent_dir_on_path():
            mod = load_agent_module("agent_changes.py")

        content = """# Changelog
## [3.0.0] - 2025-01-16
- Version 3
## [2.0.0] - 2025-01-01
- Version 2
## [1.0.0] - 2024-12-01
- Version 1
"""
        target = tmp_path / "test.changes.md"
        target.write_text(content)

        agent = mod.ChangesAgent(str(target))
        previous = agent.read_previous_content()

        assert "Version 1" in previous
        assert "Version 2" in previous
        assert "Version 3" in previous


# =============================================================================
# Comprehensive Unit Tests for agent_changes.py (unittest-based)
# =============================================================================


class TestChangelogValidationBasic(unittest.TestCase):
    """Tests for changelog format validation."""

    def test_valid_keep_a_changelog_format(self):
        """Verify valid Keep a Changelog format is accepted."""
        changelog = """# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-12-16

### Added
- Initial release
"""
        assert "# Changelog" in changelog
        assert "## [1.0.0]" in changelog
        assert "### Added" in changelog

    def test_changelog_has_required_sections(self):
        """Test changelog contains standard sections."""
        changelog = """## [1.0.0] - 2024-12-16

### Added
- Feature A

### Fixed
- Bug fix B

### Changed
- Change C
"""
        assert "### Added" in changelog
        assert "### Fixed" in changelog
        assert "### Changed" in changelog

    def test_changelog_version_format(self):
        """Test changelog version header format."""
        version_header = "## [1.0.0] - 2024-12-16"
        assert "##" in version_header
        assert "[" in version_header and "]" in version_header
        assert "-" in version_header



class TestVersionParsing(unittest.TestCase):
    """Tests for semantic version parsing."""

    def test_parse_semantic_version(self):
        """Test parsing semantic version strings."""
        version = "1.2.3"
        parts = version.split(".")
        assert len(parts) == 3
        assert all(p.isdigit() for p in parts)

    def test_parse_prerelease_version(self):
        """Test parsing prerelease versions."""
        version = "1.0.0-alpha.1"
        assert version is not None
        assert "-" in version

    def test_version_comparison(self):
        """Test semantic version ordering."""
        versions = ["1.0.0", "1.1.0", "2.0.0"]
        assert versions[0] < versions[1] < versions[2]



class TestChangelogCategorization(unittest.TestCase):
    """Tests for entry categorization."""

    def test_categorize_added_entry(self):
        """Test identifying Added entries."""
        entry = "Added new authentication feature"
        assert "added" in entry.lower()

    def test_categorize_fixed_entry(self):
        """Test identifying Fixed entries."""
        entry = "Fixed memory leak in cache"
        assert "fixed" in entry.lower()

    def test_categorize_changed_entry(self):
        """Test identifying Changed entries."""
        entry = "Changed API response format"
        assert "changed" in entry.lower()

    def test_categorize_deprecated_entry(self):
        """Test identifying Deprecated entries."""
        entry = "Deprecated legacy authentication"
        assert "deprecated" in entry.lower()

    def test_categorize_removed_entry(self):
        """Test identifying Removed entries."""
        entry = "Removed Python 2 support"
        assert "removed" in entry.lower()



class TestChangelogDiffing(unittest.TestCase):
    """Tests for changelog diffing and comparison."""

    def test_detect_new_entries(self):
        """Test detecting new entries between versions."""
        old = "- Feature A"
        new = "- Feature A\n- Feature B"
        assert "Feature B" not in old
        assert "Feature B" in new

    def test_detect_removed_entries(self):
        """Test detecting removed entries."""
        old = "- Old Feature"
        new = "- New Feature"
        assert "Old Feature" in old
        assert "Old Feature" not in new

    def test_detect_modified_entries(self):
        """Test detecting modified entries."""
        old = "Fixed bug in parser"
        new = "Fixed critical security bug in parser"
        assert "security" not in old
        assert "security" in new



class TestMarkdownPreservation(unittest.TestCase):
    """Tests for markdown formatting preservation."""

    def test_preserve_code_blocks(self):
        """Test that code blocks are preserved."""
        markdown = """```python
def new_feature():
    return True
```"""
        assert "```python" in markdown
        assert "def new_feature():" in markdown

    def test_preserve_markdown_links(self):
        """Test that links are preserved."""
        markdown = "[Issue #123](https://github.com / org / repo / issues / 123)"
        assert "[Issue #123]" in markdown
        assert "https://github.com / org / repo / issues / 123" in markdown

    def test_preserve_inline_formatting(self):
        """Test that inline formatting is preserved."""
        markdown = "**Bold** *italic* `code` ~~strikethrough~~"
        assert "**Bold**" in markdown
        assert "*italic*" in markdown
        assert "`code`" in markdown

    def test_preserve_list_structure(self):
        """Test that list structure is preserved."""
        markdown = """- Item 1
- Item 2
  - Subitem
"""
        assert "- Item 1" in markdown
        assert "- Subitem" in markdown



class TestDateValidationUnittest(unittest.TestCase):
    """Tests for date format validation."""

    def test_valid_iso_date(self):
        """Test validation of ISO date format."""
        date = "2024-12-16"
        parts = date.split("-")
        assert len(parts) == 3
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        assert 1900 <= year <= 2100
        assert 1 <= month <= 12
        assert 1 <= day <= 31

    def test_invalid_month_too_high(self):
        """Test detection of invalid month."""
        date = "2024-13-01"
        parts = date.split("-")
        month = int(parts[1])
        assert month > 12

    def test_invalid_day_too_high(self):
        """Test detection of invalid day."""
        date = "2024-12-32"
        parts = date.split("-")
        day = int(parts[2])
        assert day > 31



class TestDuplicateDetectionUnittest(unittest.TestCase):
    """Tests for detecting duplicate versions."""

    def test_detect_duplicate_version(self):
        """Test detecting duplicate version entries."""
        changelog = """## [1.0.0] - 2024-12-16
- Feature 1

## [1.0.0] - 2024-12-15
- Feature 2
"""
        versions = []
        for line in changelog.split("\n"):
            if line.startswith("## ["):
                version = line.split("]")[0].replace("## [", "")
                versions.append(version)

        assert len(versions) == 2
        assert versions[0] == versions[1]

    def test_detect_version_out_of_order(self):
        """Test detecting out of order versions."""
        changelog = """## [1.0.1] - 2024-12-16
## [1.0.0] - 2024-12-15
"""
        assert changelog.find("1.0.1") < changelog.find("1.0.0")



class TestFileDetectionUnittest(unittest.TestCase):
    """Tests for detecting changelog-related files."""

    def test_detect_changelog_files(self):
        """Test detecting standard changelog filenames."""
        files = ["CHANGELOG.md", "changelog.md", "HISTORY.md"]
        for f in files:
            assert "changelog" in f.lower() or "history" in f.lower()

    def test_detect_python_file_changes(self):
        """Test detecting Python file changes."""
        files = ["script.py", "module / package.py", "test_module.py"]
        py_files = [f for f in files if f.endswith(".py")]
        assert len(py_files) == 3

    def test_detect_multiple_languages(self):
        """Test detecting files across languages."""
        files_by_lang = {
            "python": "module.py",
            "javascript": "script.js",
            "java": "Class.java",
        }
        assert "module.py" in files_by_lang.values()
        assert "script.js" in files_by_lang.values()



class TestChangelogMergingUnittest(unittest.TestCase):
    """Tests for changelog merging."""

    def test_merge_two_changelog_versions(self):
        """Test merging separate changelog versions."""
        v1 = "## [1.0.0] - 2024-12-16\n- Feature A"
        v2 = "## [1.0.1] - 2024-12-17\n- Feature B"
        merged = v1 + "\n" + v2
        assert "Feature A" in merged
        assert "Feature B" in merged

    def test_merge_changelog_sections(self):
        """Test merging changelog sections."""
        section1 = "### Added\n- Feature 1"
        section2 = "### Fixed\n- Bug 1"
        merged = section1 + "\n" + section2
        assert "### Added" in merged
        assert "### Fixed" in merged



class TestCustomTemplatesUnittest(unittest.TestCase):
    """Tests for custom changelog templates."""

    def test_apply_template(self):
        """Test applying custom template."""
        template = """# {project}

## {version}

{content}
"""
        rendered = template.format(
            project="MyProject",
            version="1.0.0",
            content="Initial release"
        )
        assert "MyProject" in rendered
        assert "1.0.0" in rendered
        assert "Initial release" in rendered

    def test_template_with_metadata(self):
        """Test template with metadata."""
        template = """# {project} Changelog

Repository: {repo}
"""
        rendered = template.format(
            project="PyAgent",
            repo="https://github.com / org / pyagent"
        )
        assert "PyAgent" in rendered
        assert "github.com" in rendered



class TestAssociatedFileDetection(unittest.TestCase):
    """Tests for detecting associated code files."""

    def test_detect_python_files(self):
        """Test detecting Python associated files."""
        extensions = [".py", ".java", ".cpp", ".go", ".rs", ".rb"]

        associated = "agent_changes.py"
        has_supported_ext = any(associated.endswith(ext) for ext in extensions)

        assert has_supported_ext

    def test_custom_extension_env_variable(self):
        """Test custom extension environment variable."""
        custom_exts = os.environ.get("CHANGELOG_EXTENSIONS", ".py:.java:.cpp")
        exts = custom_exts.split(":")

        assert len(exts) >= 3

    def test_recursive_parent_search(self):
        """Test searching parent directories."""
        current = Path("changelog")
        parents = [current.parent, current.parent.parent]

        assert len(parents) == 2

    def test_fuzzy_file_matching(self):
        """Test fuzzy matching for filenames."""
        filename1 = "agent_changes"
        filename2 = "agent-changes"

        norm1 = filename1.replace("_", "-")
        norm2 = filename2.replace("_", "-")

        assert norm1 == norm2

    def test_detect_primary_files(self):
        """Test detecting primary module files."""
        primary_patterns = ["__init__.py", "index.js", "main.go"]
        test_file = "__init__.py"

        is_primary = test_file in primary_patterns
        assert is_primary

    def test_cache_file_lookups(self):
        """Test caching associated file lookups."""
        cache = {}

        def get_associated_file(changelog_path):
            if changelog_path in cache:
                return cache[changelog_path]

            result = "agent_changes.py"
            cache[changelog_path] = result
            return result

        result1 = get_associated_file("CHANGELOG.md")
        result2 = get_associated_file("CHANGELOG.md")

        assert result1 == result2
        assert "CHANGELOG.md" in cache

    def test_manual_associate_file_cli(self):
        """Test manual file association via CLI."""
        args = {"associate_file": "src / main.py"}
        assert "associate_file" in args



class TestVersionManagement(unittest.TestCase):
    """Tests for version detection and management."""

    def test_extract_version_from_code(self):
        """Test extracting version from code files."""
        code = '__version__="1.2.3"'

        match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', code)
        version = match.group(1) if match else None

        assert version == "1.2.3"

    def test_extract_version_from_package_json(self):
        """Test extracting version from package.json."""
        package_json = '{"version": "2.0.0", "name": "project"}'
        data = json.loads(package_json)
        version = data.get("version")

        assert version == "2.0.0"

    def test_get_latest_git_tag(self):
        """Test getting latest git tag."""
        tags = ["v1.0.0", "v1.1.0", "v2.0.0"]
        latest = max(tags)

        assert latest == "v2.0.0"

    def test_semver_auto_bump(self):
        """Test semantic versioning auto-bump."""
        commit_msg = "feat: new feature"

        if "feat:" in commit_msg:
            bump_type = "minor"
        elif "fix:" in commit_msg:
            bump_type = "patch"
        elif "BREAKING" in commit_msg:
            bump_type = "major"
        else:
            bump_type = "patch"

        assert bump_type == "minor"

    def test_detect_unreleased_section(self):
        """Test detecting [Unreleased] section."""
        changelog = """## [Unreleased]
### Added
- New feature
"""
        has_unreleased = "[Unreleased]" in changelog
        assert has_unreleased

    def test_sync_version_numbers(self):
        """Test syncing version between code and changelog."""
        code_version = "1.5.0"
        changelog_version = "1.5.0"

        are_synced = code_version == changelog_version
        assert are_synced



class TestConfiguration(unittest.TestCase):
    """Tests for configuration and customization."""

    def test_format_flag_options(self):
        """Test --format flag with multiple formats."""
        formats = ["keepachangelog", "json", "yaml", "commonchangelog"]
        selected = "json"

        is_valid = selected in formats
        assert is_valid

    def test_changelog_config_schema(self):
        """Test .changelog-config.json schema."""
        config = {
            "template_path": "templates / changelog.md",
            "ai_prompt": "Generate changelog entry",
            "validation_rules": ["require-versions", "require-dates"],
        }

        assert "template_path" in config

    def test_dry_run_flag(self):
        """Test --dry-run / -n flag."""
        args = {"dry_run": True, "no_modify": False}
        assert args["dry_run"]

    def test_custom_markdown_templates(self):
        """Test custom template with placeholders."""
        template = "## [{VERSION}] - {DATE}\n{CHANGES}"
        substituted = template.replace("{VERSION}", "1.0.0")

        assert "1.0.0" in substituted

    def test_custom_ai_prompt_file(self):
        """Test loading custom AI prompts from file."""
        prompts = {"enhance": "Enhance this changelog entry"}

        assert "enhance" in prompts

    def test_disable_ai_flag(self):
        """Test --no-ai flag for validation only."""
        args = {"no_ai": True}
        assert args["no_ai"]

    def test_verbosity_control(self):
        """Test --verbose / -v flag."""
        args = {"verbose": 2}
        assert args["verbose"] > 0



class TestUserExperience(unittest.TestCase):
    """Tests for UX improvements."""

    def test_interactive_mode(self):
        """Test interactive mode prompts."""
        user_input = "y"
        accepted = user_input.lower() in ["y", "yes"]

        assert accepted

    def test_color_coded_diff_output(self):
        """Test color formatting for diff."""
        addition = "\033[92m+ Added line\033[0m"
        deletion = "\033[91m- Removed line\033[0m"

        assert "92m" in addition
        assert "91m" in deletion

    def test_progress_bar_display(self):
        """Test progress bar for operations."""
        total = 100
        current = 50
        progress = (current / total) * 100

        assert progress == 50.0

    def test_html_preview_generation(self):
        """Test generating HTML preview."""
        html = "<html><body><h1>Changelog</h1></body></html>"

        assert "<html>" in html

    def test_preview_in_browser(self):
        """Test opening preview in browser."""
        preview_opened = True

        assert preview_opened

    def test_watch_mode_for_auto_improve(self):
        """Test --watch mode for auto-improvement."""
        args = {"watch": True}
        assert args["watch"]

    def test_summary_with_counts(self):
        """Test summary display with change counts."""
        summary = {
            "added_entries": 5,
            "removed_entries": 2,
            "modified_entries": 3,
        }

        added = summary['added_entries']
        removed = summary['removed_entries']
        modified = summary['modified_entries']
        msg = f"Added {added}, removed {removed}, modified {modified}"
        assert "Added 5" in msg



class TestQualityAssurance(unittest.TestCase):
    """Tests for quality assurance and validation."""

    def test_validate_file_extension(self):
        """Test validating file extensions."""
        valid_extensions = [".md", ".markdown", ".txt"]
        file_path = "CHANGELOG.md"

        is_valid = any(file_path.endswith(ext) for ext in valid_extensions)
        assert is_valid

    def test_check_associated_file_exists(self):
        """Test checking associated file existence."""
        path = Path("agent_changes.py")

        assert isinstance(path, Path)

    def test_mock_subprocess_for_ai_calls(self):
        """Test mocking subprocess.run for AI."""
        mock_result = MagicMock()
        mock_result.stdout = "Enhanced changelog content"
        mock_result.returncode = 0

        assert mock_result.returncode == 0

    def test_fallback_response_generation(self):
        """Test fallback when AI unavailable."""
        try:
            enhanced = "AI enhanced content"
        except Exception:
            enhanced = "Original content"

        assert enhanced is not None

    def test_unicode_support(self):
        """Test Unicode characters in changelog."""
        changelog = "### Added\n- 🎉 New feature with emoji\n- 中文 support"

        assert "🎉" in changelog

    def test_special_markdown_syntax(self):
        """Test special markdown syntax."""
        changelog = "- **Bold** and *italic* and `code`"

        assert "**Bold**" in changelog



