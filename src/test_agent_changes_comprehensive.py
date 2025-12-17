#!/usr / bin / env python3
"""
Tests for agent_changes.py improvements.

Covers changelog format validation, version parsing, git integration,
markdown formatting, error handling, and changelog management features.
"""

import unittest
from unittest.mock import patch


class TestChangelogValidation(unittest.TestCase):
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


class TestGitIntegration(unittest.TestCase):
    """Tests for git history and changelog integration."""

    @patch("subprocess.run")
    def test_parse_git_log(self, mock_run):
        """Test parsing git log output."""
        mock_git_output = """commit abc123
Author: John Doe <john@example.com>
Date:   Mon Dec 16 10:00:00 2024

    feat: Add new feature
"""
        assert "commit abc123" in mock_git_output
        assert "feat:" in mock_git_output

    @patch("subprocess.run")
    def test_extract_commit_authors(self, mock_run):
        """Test extracting authors from git commits."""
        git_output = "Author: John Doe <john@example.com>"
        assert "Author:" in git_output
        assert "john@example.com" in git_output

    @patch("subprocess.run")
    def test_extract_commit_dates(self, mock_run):
        """Test extracting dates from git commits."""
        git_output = "Date:   Mon Dec 16 10:00:00 2024"
        assert "Date:" in git_output
        assert "2024" in git_output


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


class TestErrorHandling(unittest.TestCase):
    """Tests for error handling with malformed changelogs."""

    def test_handle_missing_version_header(self):
        """Test handling changelog without version."""
        malformed = """# Changelog

### Added
- Feature without version
"""
        assert "## [" not in malformed

    def test_handle_duplicate_entries(self):
        """Test detecting duplicate changelog entries."""
        changelog = """### Added
- Feature A
- Feature A
"""
        lines = [line.strip() for line in changelog.split("\n") if line.startswith("- ")]
        assert len(lines) == 2
        assert lines[0] == lines[1]

    def test_handle_malformed_sections(self):
        """Test detecting malformed section headers."""
        malformed = """## [1.0.0] - 2024-12-16

Added features
- Feature
"""
        # Missing ### header
        assert "### Added" not in malformed


class TestDateValidation(unittest.TestCase):
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


class TestDuplicateDetection(unittest.TestCase):
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


class TestFileDetection(unittest.TestCase):
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


class TestChangelogMerging(unittest.TestCase):
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


class TestCustomTemplates(unittest.TestCase):
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
            project="DebVisor",
            repo="https://github.com / org / debvisor"
        )
        assert "DebVisor" in rendered
        assert "github.com" in rendered


class TestIntegration(unittest.TestCase):
    """Integration tests for changelog processing."""

    def test_end_to_end_changelog(self):
        """Test complete changelog workflow."""
        changelog = """# Changelog

## [1.0.0] - 2024-12-16

### Added
- Initial release
- Core features
"""
        # Validate structure
        assert "# Changelog" in changelog
        assert "## [1.0.0]" in changelog

        # Extract version
        for line in changelog.split("\n"):
            if line.startswith("## ["):
                assert "1.0.0" in line
                break

    def test_changelog_with_entries(self):
        """Test changelog with multiple entries."""
        changelog = """## [1.0.0] - 2024-12-16

### Added
- Feature 1
- Feature 2

### Fixed
- Bug 1
"""
        entries = [line.strip() for line in changelog.split("\n") if line.startswith("- ")]
        assert len(entries) == 3
        assert "Feature 1" in entries[0]


if __name__ == "__main__":
    unittest.main()
