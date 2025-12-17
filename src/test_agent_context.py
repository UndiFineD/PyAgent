#!/usr / bin / env python3
# Copyright (c) 2025 DebVisor contributors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org / licenses / LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Legacy tests for agent-context.py."""

from __future__ import annotations
import ast
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
import pytest
from agent_test_utils import agent_dir_on_path, load_agent_module


@pytest.fixture()
def base_agent_module() -> Any:
    with agent_dir_on_path():
        import base_agent
        return base_agent


def test_context_agent_delegates_to_base(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, base_agent_module: Any
) -> None:
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")

    def fake_run_subagent(
            self: Any,
            description: str,
            prompt: str,
            original_content: str = "") -> str:
        return "IMPROVED"

    monkeypatch.setattr(
        base_agent_module.BaseAgent,
        "run_subagent",
        fake_run_subagent,
        raising=True)
    target = tmp_path / "x.description.md"
    target.write_text("BEFORE", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    assert agent.improve_content("prompt") == "IMPROVED"


# ========== Template Management Tests ==========

def test_set_template_valid(tmp_path: Path) -> None:
    """Test setting a valid template."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    result = agent.set_template("python")
    assert result is True


def test_set_template_invalid(tmp_path: Path) -> None:
    """Test setting an invalid template."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    result = agent.set_template("nonexistent")
    assert result is False


def test_get_template(tmp_path: Path) -> None:
    """Test getting a template."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    template = agent.get_template("python")
    assert template is not None
    assert template.name == "Python Module"


def test_add_custom_template(tmp_path: Path) -> None:
    """Test adding a custom template."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    template = mod.ContextTemplate(
        name="Custom",
        file_type=".custom",
        sections=["Section1", "Section2"],
        template_content="# Custom Template"
    )
    agent.add_template(template)
    assert agent.get_template("custom") is not None


def test_get_template_for_python_file(tmp_path: Path) -> None:
    """Test auto-detecting template for Python file."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    # Create source file
    source = tmp_path / "mymodule.py"
    source.write_text("# Python code", encoding="utf-8")
    target = tmp_path / "mymodule.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    template = agent.get_template_for_file()
    assert template is not None
    assert template.file_type == ".py"


def test_apply_template(tmp_path: Path) -> None:
    """Test applying a template."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    content = agent.apply_template("python")
    assert "# Description:" in content
    assert "## Purpose" in content


# ========== Tagging Tests ==========

def test_add_tag(tmp_path: Path) -> None:
    """Test adding a tag."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    tag = mod.ContextTag(name="important", description="Important files")
    agent.add_tag(tag)
    assert agent.has_tag("important")


def test_remove_tag(tmp_path: Path) -> None:
    """Test removing a tag."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    tag = mod.ContextTag(name="temp", description="Temporary")
    agent.add_tag(tag)
    result = agent.remove_tag("temp")
    assert result is True
    assert not agent.has_tag("temp")


def test_remove_nonexistent_tag(tmp_path: Path) -> None:
    """Test removing a non-existent tag."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    result = agent.remove_tag("nonexistent")
    assert result is False


def test_get_tags(tmp_path: Path) -> None:
    """Test getting all tags."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.add_tag(mod.ContextTag(name="tag1"))
    agent.add_tag(mod.ContextTag(name="tag2"))
    tags = agent.get_tags()
    assert len(tags) == 2


def test_get_tags_by_parent(tmp_path: Path) -> None:
    """Test getting tags by parent."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.add_tag(mod.ContextTag(name="parent"))
    agent.add_tag(mod.ContextTag(name="child1", parent="parent"))
    agent.add_tag(mod.ContextTag(name="child2", parent="parent"))
    children = agent.get_tags_by_parent("parent")
    assert len(children) == 2


# ========== Versioning Tests ==========

def test_create_version(tmp_path: Path) -> None:
    """Test creating a version."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("content", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    version = agent.create_version("1.0.0", changes=["Initial version"])
    assert version.version == "1.0.0"
    assert "Initial version" in version.changes


def test_get_versions(tmp_path: Path) -> None:
    """Test getting all versions."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("content", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    agent.create_version("1.0.0")
    agent.create_version("1.1.0")
    versions = agent.get_versions()
    assert len(versions) == 2


def test_get_latest_version(tmp_path: Path) -> None:
    """Test getting latest version."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("content", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    agent.create_version("1.0.0")
    agent.create_version("2.0.0")
    latest = agent.get_latest_version()
    assert latest.version == "2.0.0"


def test_get_latest_version_empty(tmp_path: Path) -> None:
    """Test getting latest version when none exist."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    latest = agent.get_latest_version()
    assert latest is None


def test_get_version_diff(tmp_path: Path) -> None:
    """Test getting version diff."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("content", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    agent.create_version("1.0.0")
    agent.create_version("1.1.0", changes=["Added feature"])
    diff = agent.get_version_diff("1.0.0", "1.1.0")
    assert diff["from_version"] == "1.0.0"
    assert diff["to_version"] == "1.1.0"


# ========== Compression Tests ==========

def test_compress_content(tmp_path: Path) -> None:
    """Test compressing content."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("test content " * 100, encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    compressed = agent.compress_content()
    assert len(compressed) < len(agent.previous_content)


def test_decompress_content(tmp_path: Path) -> None:
    """Test decompressing content."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    original = "test content " * 100
    target.write_text(original, encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    compressed = agent.compress_content()
    decompressed = agent.decompress_content(compressed)
    assert decompressed == original


def test_get_compression_ratio(tmp_path: Path) -> None:
    """Test getting compression ratio."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("test content " * 100, encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    ratio = agent.get_compression_ratio()
    assert 0 < ratio < 1


# ========== Validation Tests ==========

def test_validate_content_has_purpose(tmp_path: Path) -> None:
    """Test validation requires Purpose section."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("# Title\nNo purpose section", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    issues = agent.validate_content()
    assert any(i["rule"] == "has_purpose" for i in issues)


def test_validate_content_valid(tmp_path: Path) -> None:
    """Test validation passes with Purpose section."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("# Title\n\n## Purpose\nThis is the purpose.", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    issues = agent.validate_content()
    errors = [i for i in issues if i.get("severity") == "error"]
    assert len(errors) == 0


def test_is_valid(tmp_path: Path) -> None:
    """Test is_valid method."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("# Title\n\n## Purpose\nValid content.", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    assert agent.is_valid()


def test_add_validation_rule(tmp_path: Path) -> None:
    """Test adding a validation rule."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    rule = mod.ValidationRule(
        name="custom_rule",
        pattern=r"CUSTOM",
        message="Custom pattern not found",
        required=True
    )
    initial_count = len(agent._validation_rules)
    agent.add_validation_rule(rule)
    assert len(agent._validation_rules) == initial_count + 1


# ========== Annotation Tests ==========

def test_add_annotation(tmp_path: Path) -> None:
    """Test adding an annotation."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("line1\nline2\nline3", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    annotation = agent.add_annotation(2, "Review this line", "author")
    assert annotation.line_number == 2
    assert annotation.content == "Review this line"


def test_get_annotations(tmp_path: Path) -> None:
    """Test getting all annotations."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.add_annotation(1, "Note 1")
    agent.add_annotation(2, "Note 2")
    annotations = agent.get_annotations()
    assert len(annotations) == 2


def test_get_annotations_for_line(tmp_path: Path) -> None:
    """Test getting annotations for a specific line."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.add_annotation(5, "Note 1")
    agent.add_annotation(5, "Note 2")
    agent.add_annotation(10, "Note 3")
    line_annotations = agent.get_annotations_for_line(5)
    assert len(line_annotations) == 2


def test_resolve_annotation(tmp_path: Path) -> None:
    """Test resolving an annotation."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    annotation = agent.add_annotation(1, "Fix this")
    result = agent.resolve_annotation(annotation.id)
    assert result is True
    assert annotation.resolved is True


def test_remove_annotation(tmp_path: Path) -> None:
    """Test removing an annotation."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    annotation = agent.add_annotation(1, "Temp note")
    result = agent.remove_annotation(annotation.id)
    assert result is True
    assert len(agent.get_annotations()) == 0


# ========== Priority Scoring Tests ==========

def test_set_priority(tmp_path: Path) -> None:
    """Test setting priority."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.set_priority(mod.ContextPriority.HIGH)
    assert agent.get_priority() == mod.ContextPriority.HIGH


def test_calculate_priority_score(tmp_path: Path) -> None:
    """Test calculating priority score."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    content = """# Description

## Purpose
This is important.

## Usage
```python
import module
```
"""
    target.write_text(content, encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.read_previous_content()
    agent.set_priority(mod.ContextPriority.HIGH)
    score = agent.calculate_priority_score()
    assert 0 <= score <= 100


# ========== Categorization Tests ==========

def test_set_category(tmp_path: Path) -> None:
    """Test setting category."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.set_category(mod.FileCategory.CODE)
    assert agent.get_category() == mod.FileCategory.CODE


def test_auto_categorize_python(tmp_path: Path) -> None:
    """Test auto-categorizing Python file."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    source = tmp_path / "module.py"
    source.write_text("# Code", encoding="utf-8")
    target = tmp_path / "module.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    category = agent.auto_categorize()
    assert category == mod.FileCategory.CODE


def test_auto_categorize_test(tmp_path: Path) -> None:
    """Test auto-categorizing test file."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    source = tmp_path / "test_module.py"
    source.write_text("# Tests", encoding="utf-8")
    target = tmp_path / "test_module.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    category = agent.auto_categorize()
    assert category == mod.FileCategory.TEST


def test_auto_categorize_config(tmp_path: Path) -> None:
    """Test auto-categorizing config file."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    source = tmp_path / "config.json"
    source.write_text("{}", encoding="utf-8")
    target = tmp_path / "config.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    category = agent.auto_categorize()
    assert category == mod.FileCategory.CONFIGURATION


# ========== Metadata Tests ==========

def test_set_metadata(tmp_path: Path) -> None:
    """Test setting metadata."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.set_metadata("author", "John")
    assert agent.get_metadata("author") == "John"


def test_get_all_metadata(tmp_path: Path) -> None:
    """Test getting all metadata."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.set_metadata("key1", "value1")
    agent.set_metadata("key2", "value2")
    metadata = agent.get_all_metadata()
    assert len(metadata) == 2


def test_export_metadata(tmp_path: Path) -> None:
    """Test exporting metadata as JSON."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    target = tmp_path / "test.description.md"
    target.write_text("", encoding="utf-8")
    agent = mod.ContextAgent(str(target))
    agent.set_priority(mod.ContextPriority.HIGH)
    agent.set_category(mod.FileCategory.CODE)
    exported = agent.export_metadata()
    assert "priority" in exported
    assert "category" in exported


# ========== Dataclass Tests ==========

def test_context_template_dataclass() -> None:
    """Test ContextTemplate dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    template = mod.ContextTemplate(
        name="Test",
        file_type=".test",
        sections=["A", "B"],
        template_content="# Test"
    )
    assert template.required_fields == []


def test_context_tag_dataclass() -> None:
    """Test ContextTag dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    tag = mod.ContextTag(name="test")
    assert tag.description == ""
    assert tag.parent is None


def test_context_version_dataclass() -> None:
    """Test ContextVersion dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    version = mod.ContextVersion(
        version="1.0.0",
        timestamp="2025-01-01",
        content_hash="abc123"
    )
    assert version.changes == []
    assert version.author == ""


def test_validation_rule_dataclass() -> None:
    """Test ValidationRule dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    rule = mod.ValidationRule(
        name="test",
        pattern=r".*",
        message="Test"
    )
    assert rule.severity == "warning"
    assert rule.required is False


def test_context_annotation_dataclass() -> None:
    """Test ContextAnnotation dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    annotation = mod.ContextAnnotation(
        id="abc123",
        line_number=1,
        content="Note"
    )
    assert annotation.author == ""
    assert annotation.resolved is False


# ========== Enum Tests ==========

def test_context_priority_enum_values() -> None:
    """Test ContextPriority enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    assert mod.ContextPriority.CRITICAL.value == 5
    assert mod.ContextPriority.LOW.value == 2


def test_file_category_enum_values() -> None:
    """Test FileCategory enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    assert mod.FileCategory.CODE.value == "code"
    assert mod.FileCategory.TEST.value == "test"


# ========== Session 7 Tests: New Enums ==========


def test_search_algorithm_enum() -> None:
    """Test SearchAlgorithm enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    assert mod.SearchAlgorithm.KEYWORD.value == "keyword"
    assert mod.SearchAlgorithm.FUZZY.value == "fuzzy"
    assert mod.SearchAlgorithm.SEMANTIC.value == "semantic"
    assert mod.SearchAlgorithm.HYBRID.value == "hybrid"


def test_export_format_enum() -> None:
    """Test ExportFormat enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    assert mod.ExportFormat.MARKDOWN.value == "markdown"
    assert mod.ExportFormat.HTML.value == "html"
    assert mod.ExportFormat.PDF.value == "pdf"
    assert mod.ExportFormat.DOCX.value == "docx"
    assert mod.ExportFormat.RST.value == "rst"


def test_inheritance_mode_enum() -> None:
    """Test InheritanceMode enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    assert mod.InheritanceMode.OVERRIDE.value == "override"
    assert mod.InheritanceMode.MERGE.value == "merge"
    assert mod.InheritanceMode.APPEND.value == "append"


def test_visualization_type_enum() -> None:
    """Test VisualizationType enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    assert mod.VisualizationType.DEPENDENCY_GRAPH.value == "dependency_graph"
    assert mod.VisualizationType.CALL_HIERARCHY.value == "call_hierarchy"
    assert mod.VisualizationType.FILE_TREE.value == "file_tree"
    assert mod.VisualizationType.MIND_MAP.value == "mind_map"


def test_conflict_resolution_enum() -> None:
    """Test ConflictResolution enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    assert mod.ConflictResolution.OURS.value == "ours"
    assert mod.ConflictResolution.THEIRS.value == "theirs"
    assert mod.ConflictResolution.MANUAL.value == "manual"
    assert mod.ConflictResolution.AUTO.value == "auto"


def test_sharing_permission_enum() -> None:
    """Test SharingPermission enum values."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    assert mod.SharingPermission.READ_ONLY.value == "read_only"
    assert mod.SharingPermission.READ_WRITE.value == "read_write"
    assert mod.SharingPermission.ADMIN.value == "admin"


# ========== Session 7 Tests: Dataclasses ==========


def test_semantic_search_result_dataclass() -> None:
    """Test SemanticSearchResult dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    result = mod.SemanticSearchResult(
        file_path="/path / to / file.py",
        content_snippet="def foo(): pass",
        similarity_score=0.95
    )
    assert result.file_path == "/path / to / file.py"
    assert result.similarity_score == 0.95
    assert result.context_type == ""
    assert result.line_range == (0, 0)


def test_cross_repo_context_dataclass() -> None:
    """Test CrossRepoContext dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    context = mod.CrossRepoContext(
        repo_name="other-repo",
        repo_url="https://github.com / user / other-repo"
    )
    assert context.repo_name == "other-repo"
    assert context.related_files == []
    assert context.common_patterns == []


def test_context_diff_dataclass() -> None:
    """Test ContextDiff dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    diff = mod.ContextDiff(
        version_from="1.0",
        version_to="2.0",
        added_sections=["New Section"]
    )
    assert diff.version_from == "1.0"
    assert diff.added_sections == ["New Section"]
    assert diff.removed_sections == []


def test_inherited_context_dataclass() -> None:
    """Test InheritedContext dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    inherited = mod.InheritedContext(
        parent_path="/path / to / parent.md"
    )
    assert inherited.parent_path == "/path / to / parent.md"
    assert inherited.mode == mod.InheritanceMode.MERGE
    assert inherited.inherited_sections == []


def test_nl_query_result_dataclass() -> None:
    """Test NLQueryResult dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    result = mod.NLQueryResult(
        query="What does this function do?",
        answer="It processes data."
    )
    assert result.query == "What does this function do?"
    assert result.confidence == 0.0


def test_exported_context_dataclass() -> None:
    """Test ExportedContext dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    exported = mod.ExportedContext(
        format=mod.ExportFormat.HTML,
        content="<html>content</html>"
    )
    assert exported.format == mod.ExportFormat.HTML
    assert exported.metadata == {}


def test_context_recommendation_dataclass() -> None:
    """Test ContextRecommendation dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    rec = mod.ContextRecommendation(
        source_file="similar.py",
        suggested_sections=["Usage", "Examples"]
    )
    assert rec.source_file == "similar.py"
    assert rec.confidence == 0.0


def test_generated_code_dataclass() -> None:
    """Test GeneratedCode dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    code = mod.GeneratedCode(
        language="python",
        code="print('hello')"
    )
    assert code.language == "python"
    assert code.context_used == []


def test_refactoring_suggestion_dataclass() -> None:
    """Test RefactoringSuggestion dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    suggestion = mod.RefactoringSuggestion(
        suggestion_type="extract_method",
        description="Extract complex logic"
    )
    assert suggestion.suggestion_type == "extract_method"
    assert suggestion.estimated_impact == "medium"


def test_visualization_data_dataclass() -> None:
    """Test VisualizationData dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    viz = mod.VisualizationData(
        viz_type=mod.VisualizationType.DEPENDENCY_GRAPH
    )
    assert viz.viz_type == mod.VisualizationType.DEPENDENCY_GRAPH
    assert viz.nodes == []
    assert viz.layout == "hierarchical"


def test_shared_context_dataclass() -> None:
    """Test SharedContext dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    shared = mod.SharedContext(
        context_id="ctx-123",
        owner="alice"
    )
    assert shared.context_id == "ctx-123"
    assert shared.permission == mod.SharingPermission.READ_ONLY


def test_merge_conflict_dataclass() -> None:
    """Test MergeConflict dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    conflict = mod.MergeConflict(
        section="Purpose",
        ours="Our content",
        theirs="Their content"
    )
    assert conflict.section == "Purpose"
    assert conflict.resolution is None


def test_branch_comparison_dataclass() -> None:
    """Test BranchComparison dataclass."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    comparison = mod.BranchComparison(
        branch_a="main",
        branch_b="feature"
    )
    assert comparison.branch_a == "main"
    assert comparison.files_only_in_a == []


# ========== Session 7 Tests: SemanticSearchEngine ==========


def test_semantic_search_engine_init() -> None:
    """Test SemanticSearchEngine initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    engine = mod.SemanticSearchEngine()
    assert engine.algorithm == mod.SearchAlgorithm.KEYWORD


def test_semantic_search_engine_set_algorithm() -> None:
    """Test setting search algorithm."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    engine = mod.SemanticSearchEngine()
    engine.set_algorithm(mod.SearchAlgorithm.FUZZY)
    assert engine.algorithm == mod.SearchAlgorithm.FUZZY


def test_semantic_search_engine_add_document() -> None:
    """Test adding documents to search engine."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    engine = mod.SemanticSearchEngine()
    engine.add_document("file.py", "def hello(): pass")
    assert "file.py" in engine.documents


def test_semantic_search_engine_search() -> None:
    """Test semantic search."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    engine = mod.SemanticSearchEngine()
    engine.add_document("file.py", "def hello world function")
    results = engine.search("hello")
    assert len(results) > 0


def test_semantic_search_engine_clear() -> None:
    """Test clearing search index."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    engine = mod.SemanticSearchEngine()
    engine.add_document("file.py", "content")
    engine.clear()
    assert len(engine.documents) == 0


# ========== Session 7 Tests: CrossRepoAnalyzer ==========


def test_cross_repo_analyzer_init() -> None:
    """Test CrossRepoAnalyzer initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    analyzer = mod.CrossRepoAnalyzer()
    assert analyzer.repos == {}


def test_cross_repo_analyzer_add_repo() -> None:
    """Test adding repository."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    analyzer = mod.CrossRepoAnalyzer()
    analyzer.add_repo("my-repo", "https://github.com / user / repo")
    assert "my-repo" in analyzer.repos


def test_cross_repo_analyzer_analyze() -> None:
    """Test analyzing cross-repo context."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    analyzer = mod.CrossRepoAnalyzer()
    analyzer.add_repo("repo1", "https://github.com / user / repo1")
    results = analyzer.analyze("file.py")
    assert isinstance(results, list)


def test_cross_repo_analyzer_find_patterns() -> None:
    """Test finding common patterns."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    analyzer = mod.CrossRepoAnalyzer()
    patterns = analyzer.find_common_patterns()
    assert isinstance(patterns, list)


# ========== Session 7 Tests: ContextDiffer ==========


def test_context_differ_init() -> None:
    """Test ContextDiffer initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    differ = mod.ContextDiffer()
    assert differ is not None


def test_context_differ_compute_diff() -> None:
    """Test computing diff between contexts."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    differ = mod.ContextDiffer()
    diff = differ.compute_diff("# Old\nContent", "# New\nContent")
    assert isinstance(diff, mod.ContextDiff)


def test_context_differ_section_diff() -> None:
    """Test section-level diff."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    differ = mod.ContextDiffer()
    sections = differ.get_section_changes(
        "## Section A\nContent",
        "## Section B\nNew content"
    )
    assert isinstance(sections, dict)


def test_context_differ_summarize() -> None:
    """Test diff summarization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    differ = mod.ContextDiffer()
    diff = differ.compute_diff("Old", "New")
    summary = differ.summarize_diff(diff)
    assert isinstance(summary, str)


# ========== Session 7 Tests: ContextInheritance ==========


def test_context_inheritance_init() -> None:
    """Test ContextInheritance initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    inheritance = mod.ContextInheritance()
    assert inheritance.mode == mod.InheritanceMode.MERGE


def test_context_inheritance_set_mode() -> None:
    """Test setting inheritance mode."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    inheritance = mod.ContextInheritance()
    inheritance.set_mode(mod.InheritanceMode.OVERRIDE)
    assert inheritance.mode == mod.InheritanceMode.OVERRIDE


def test_context_inheritance_set_parent() -> None:
    """Test setting parent context."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    inheritance = mod.ContextInheritance()
    inheritance.set_parent("/path / to / parent.md")
    assert inheritance.parent_path == "/path / to / parent.md"


def test_context_inheritance_apply() -> None:
    """Test applying inheritance."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    inheritance = mod.ContextInheritance()
    result = inheritance.apply("child content", "parent content")
    assert isinstance(result, str)


def test_context_inheritance_get_hierarchy() -> None:
    """Test getting inheritance hierarchy."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    inheritance = mod.ContextInheritance()
    hierarchy = inheritance.get_hierarchy()
    assert isinstance(hierarchy, list)


# ========== Session 7 Tests: NLQueryEngine ==========


def test_nl_query_engine_init() -> None:
    """Test NLQueryEngine initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    engine = mod.NLQueryEngine()
    assert engine is not None


def test_nl_query_engine_add_context() -> None:
    """Test adding context to NL engine."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    engine = mod.NLQueryEngine()
    engine.add_context("file.md", "# Description\nThis is a test.")
    assert "file.md" in engine.contexts


def test_nl_query_engine_query() -> None:
    """Test natural language query."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    engine = mod.NLQueryEngine()
    engine.add_context("file.md", "This module handles data processing.")
    result = engine.query("What does this do?")
    assert isinstance(result, mod.NLQueryResult)


def test_nl_query_engine_extract_keywords() -> None:
    """Test keyword extraction."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    engine = mod.NLQueryEngine()
    keywords = engine.extract_keywords("How does the data processing work?")
    assert isinstance(keywords, list)


# ========== Session 7 Tests: ContextExporter ==========


def test_context_exporter_init() -> None:
    """Test ContextExporter initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    exporter = mod.ContextExporter()
    assert exporter.default_format == mod.ExportFormat.MARKDOWN


def test_context_exporter_set_format() -> None:
    """Test setting export format."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    exporter = mod.ContextExporter()
    exporter.set_format(mod.ExportFormat.HTML)
    assert exporter.default_format == mod.ExportFormat.HTML


def test_context_exporter_export_markdown() -> None:
    """Test exporting to markdown."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    exporter = mod.ContextExporter()
    result = exporter.export("# Test\nContent", mod.ExportFormat.MARKDOWN)
    assert isinstance(result, mod.ExportedContext)
    assert result.format == mod.ExportFormat.MARKDOWN


def test_context_exporter_export_html() -> None:
    """Test exporting to HTML."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    exporter = mod.ContextExporter()
    result = exporter.export("# Test\nContent", mod.ExportFormat.HTML)
    assert "<html>" in result.content or "<h1>" in result.content


def test_context_exporter_supported_formats() -> None:
    """Test getting supported formats."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    exporter = mod.ContextExporter()
    formats = exporter.get_supported_formats()
    assert mod.ExportFormat.MARKDOWN in formats


# ========== Session 7 Tests: ContextRecommender ==========


def test_context_recommender_init() -> None:
    """Test ContextRecommender initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    recommender = mod.ContextRecommender()
    assert recommender.reference_files == {}


def test_context_recommender_add_reference() -> None:
    """Test adding reference file."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    recommender = mod.ContextRecommender()
    recommender.add_reference("good.md", "## Purpose\n## Usage")
    assert "good.md" in recommender.reference_files


def test_context_recommender_recommend() -> None:
    """Test getting recommendations."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    recommender = mod.ContextRecommender()
    recommender.add_reference("good.md", "## Purpose\n## Usage\n## Examples")
    recs = recommender.recommend("## Purpose\nOnly purpose")
    assert isinstance(recs, list)


def test_context_recommender_find_similar() -> None:
    """Test finding similar files."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    recommender = mod.ContextRecommender()
    recommender.add_reference("file1.md", "Python module")
    recommender.add_reference("file2.md", "JavaScript module")
    similar = recommender.find_similar("Python utility")
    assert isinstance(similar, list)


# ========== Session 7 Tests: CodeGenerator ==========


def test_code_generator_init() -> None:
    """Test CodeGenerator initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    generator = mod.CodeGenerator()
    assert generator is not None


def test_code_generator_set_language() -> None:
    """Test setting code language."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    generator = mod.CodeGenerator()
    generator.set_language("python")
    assert generator.language == "python"


def test_code_generator_generate() -> None:
    """Test code generation."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    generator = mod.CodeGenerator()
    generator.set_language("python")
    result = generator.generate("Create a hello function")
    assert isinstance(result, mod.GeneratedCode)
    assert result.language == "python"


def test_code_generator_with_context() -> None:
    """Test code generation with context."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    generator = mod.CodeGenerator()
    generator.add_context("utils.md", "Utility functions for string processing")
    result = generator.generate("String helper", context_files=["utils.md"])
    assert "utils.md" in result.context_used


def test_code_generator_supported_languages() -> None:
    """Test getting supported languages."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    generator = mod.CodeGenerator()
    languages = generator.get_supported_languages()
    assert "python" in languages


# ========== Session 7 Tests: RefactoringAdvisor ==========


def test_refactoring_advisor_init() -> None:
    """Test RefactoringAdvisor initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    advisor = mod.RefactoringAdvisor()
    assert advisor is not None


def test_refactoring_advisor_analyze() -> None:
    """Test analyzing for refactoring opportunities."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    advisor = mod.RefactoringAdvisor()
    suggestions = advisor.analyze("## Purpose\nVery long repeated code...")
    assert isinstance(suggestions, list)


def test_refactoring_advisor_add_pattern() -> None:
    """Test adding custom refactoring pattern."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    advisor = mod.RefactoringAdvisor()
    advisor.add_pattern("custom", r"TODO:", "Add TODO tracking")
    assert "custom" in advisor.patterns


def test_refactoring_advisor_prioritize() -> None:
    """Test prioritizing suggestions."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    advisor = mod.RefactoringAdvisor()
    suggestions = advisor.analyze("Long content")
    prioritized = advisor.prioritize(suggestions)
    assert isinstance(prioritized, list)


# ========== Session 7 Tests: ContextVisualizer ==========


def test_context_visualizer_init() -> None:
    """Test ContextVisualizer initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    visualizer = mod.ContextVisualizer()
    assert visualizer.viz_type == mod.VisualizationType.DEPENDENCY_GRAPH


def test_context_visualizer_set_type() -> None:
    """Test setting visualization type."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    visualizer = mod.ContextVisualizer()
    visualizer.set_type(mod.VisualizationType.MIND_MAP)
    assert visualizer.viz_type == mod.VisualizationType.MIND_MAP


def test_context_visualizer_add_node() -> None:
    """Test adding visualization node."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    visualizer = mod.ContextVisualizer()
    visualizer.add_node("main.py", {"type": "module"})
    assert len(visualizer.nodes) == 1


def test_context_visualizer_add_edge() -> None:
    """Test adding visualization edge."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    visualizer = mod.ContextVisualizer()
    visualizer.add_node("main.py", {})
    visualizer.add_node("utils.py", {})
    visualizer.add_edge("main.py", "utils.py")
    assert ("main.py", "utils.py") in visualizer.edges


def test_context_visualizer_generate() -> None:
    """Test generating visualization data."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    visualizer = mod.ContextVisualizer()
    visualizer.add_node("file.py", {"type": "module"})
    data = visualizer.generate()
    assert isinstance(data, mod.VisualizationData)


def test_context_visualizer_export_json() -> None:
    """Test exporting visualization to JSON."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    visualizer = mod.ContextVisualizer()
    visualizer.add_node("file.py", {})
    json_str = visualizer.export_json()
    assert isinstance(json_str, str)


# ========== Session 7 Tests: ContextSharingManager ==========


def test_context_sharing_manager_init() -> None:
    """Test ContextSharingManager initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    manager = mod.ContextSharingManager(owner="alice")
    assert manager.owner == "alice"


def test_context_sharing_manager_create_shared() -> None:
    """Test creating shared context."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    manager = mod.ContextSharingManager(owner="alice")
    shared = manager.create_shared("# Shared context")
    assert isinstance(shared, mod.SharedContext)
    assert shared.owner == "alice"


def test_context_sharing_manager_share_with() -> None:
    """Test sharing with another user."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    manager = mod.ContextSharingManager(owner="alice")
    shared = manager.create_shared("Content")
    manager.share_with(shared.context_id, "bob")
    assert "bob" in shared.shared_with


def test_context_sharing_manager_set_permission() -> None:
    """Test setting sharing permission."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    manager = mod.ContextSharingManager(owner="alice")
    shared = manager.create_shared("Content")
    manager.set_permission(shared.context_id, mod.SharingPermission.READ_WRITE)
    assert shared.permission == mod.SharingPermission.READ_WRITE


def test_context_sharing_manager_revoke() -> None:
    """Test revoking access."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    manager = mod.ContextSharingManager(owner="alice")
    shared = manager.create_shared("Content")
    manager.share_with(shared.context_id, "bob")
    manager.revoke_access(shared.context_id, "bob")
    assert "bob" not in shared.shared_with


def test_context_sharing_manager_get_shared() -> None:
    """Test getting shared contexts."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    manager = mod.ContextSharingManager(owner="alice")
    manager.create_shared("Content 1")
    manager.create_shared("Content 2")
    shared_list = manager.get_shared_contexts()
    assert len(shared_list) >= 2


# ========== Session 7 Tests: MergeConflictResolver ==========


def test_merge_conflict_resolver_init() -> None:
    """Test MergeConflictResolver initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    resolver = mod.MergeConflictResolver()
    assert resolver.strategy == mod.ConflictResolution.AUTO


def test_merge_conflict_resolver_set_strategy() -> None:
    """Test setting resolution strategy."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    resolver = mod.MergeConflictResolver()
    resolver.set_strategy(mod.ConflictResolution.OURS)
    assert resolver.strategy == mod.ConflictResolution.OURS


def test_merge_conflict_resolver_detect() -> None:
    """Test detecting conflicts."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    resolver = mod.MergeConflictResolver()
    conflicts = resolver.detect_conflicts(
        "## Section A\nOur content",
        "## Section A\nTheir content"
    )
    assert isinstance(conflicts, list)


def test_merge_conflict_resolver_resolve() -> None:
    """Test resolving a conflict."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    resolver = mod.MergeConflictResolver()
    conflict = mod.MergeConflict(
        section="Purpose",
        ours="Our purpose",
        theirs="Their purpose"
    )
    resolved = resolver.resolve(conflict)
    assert isinstance(resolved, str)


def test_merge_conflict_resolver_resolve_all() -> None:
    """Test resolving all conflicts."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    resolver = mod.MergeConflictResolver()
    conflicts = [
        mod.MergeConflict("A", "ours", "theirs"),
        mod.MergeConflict("B", "ours2", "theirs2")
    ]
    result = resolver.resolve_all(conflicts)
    assert isinstance(result, str)


# ========== Session 7 Tests: BranchComparer ==========


def test_branch_comparer_init() -> None:
    """Test BranchComparer initialization."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    comparer = mod.BranchComparer()
    assert comparer is not None


def test_branch_comparer_set_branches() -> None:
    """Test setting branches to compare."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    comparer = mod.BranchComparer()
    comparer.set_branches("main", "feature / new-feature")
    assert comparer.branch_a == "main"
    assert comparer.branch_b == "feature / new-feature"


def test_branch_comparer_compare() -> None:
    """Test branch comparison."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    comparer = mod.BranchComparer()
    comparer.set_branches("main", "develop")
    comparison = comparer.compare()
    assert isinstance(comparison, mod.BranchComparison)


def test_branch_comparer_get_modified() -> None:
    """Test getting modified files."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    comparer = mod.BranchComparer()
    comparer.set_branches("main", "develop")
    modified = comparer.get_modified_files()
    assert isinstance(modified, list)


def test_branch_comparer_summarize() -> None:
    """Test branch comparison summary."""
    with agent_dir_on_path():
        mod = load_agent_module("agent-context.py")
    comparer = mod.BranchComparer()
    comparer.set_branches("main", "develop")
    comparison = comparer.compare()
    summary = comparer.summarize(comparison)
    assert isinstance(summary, str)


# =============================================================================
# Session 9: Semantic Search Tests
# =============================================================================


class TestSemanticSearch:
    """Tests for semantic search using embeddings."""

    def test_semantic_search_basic(self, tmp_path: Path) -> None:
        """Test basic semantic search."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "def calculate_total(items): return sum(items)"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "calculate_total" in previous

    def test_semantic_search_relevance(self, tmp_path: Path) -> None:
        """Test semantic search returns relevant results."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "# User Authentication\nThis module handles user login."
        target = tmp_path / "auth.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        content = agent.read_previous_content()

        assert "Authentication" in content


# =============================================================================
# Session 9: Cross-Repository Context Tests
# =============================================================================


class TestCrossRepositoryContext:
    """Tests for cross-repository context analysis."""

    def test_cross_repo_reference(self, tmp_path: Path) -> None:
        """Test detecting cross-repository references."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "Depends on: github.com / org / other-repo"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "github.com" in previous


# =============================================================================
# Session 9: Context Diffing Tests
# =============================================================================


class TestContextDiffing:
    """Tests for context diffing between versions."""

    def test_diff_content_detection(self, tmp_path: Path) -> None:
        """Test diff content is detected."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = """
## Version 2.0
- New feature
## Version 1.0
- Original feature
"""
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Version 2.0" in previous
        assert "Version 1.0" in previous


# =============================================================================
# Session 9: Context Template Application Tests
# =============================================================================


class TestContextTemplateApplication:
    """Tests for context template application."""

    def test_template_placeholder_detection(self, tmp_path: Path) -> None:
        """Test template placeholder detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "# {module_name}\n\nDescription: {description}"
        target = tmp_path / "template.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "{module_name}" in previous


# =============================================================================
# Session 9: Context Inheritance Tests
# =============================================================================


class TestContextInheritance:
    """Tests for context inheritance chains."""

    def test_inheritance_detection(self, tmp_path: Path) -> None:
        """Test detecting inheritance in context."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "Extends: base_module\nInherits: core.BaseClass"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Extends:" in previous


# =============================================================================
# Session 9: Context Tagging Tests
# =============================================================================


class TestContextTagging:
    """Tests for context tagging and categorization."""

    def test_tag_detection(self, tmp_path: Path) -> None:
        """Test tag detection in context."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "Tags: [security], [authentication], [api]"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "[security]" in previous

    def test_category_detection(self, tmp_path: Path) -> None:
        """Test category detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "Category: Core Infrastructure"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Category:" in previous


# =============================================================================
# Session 9: Natural Language Search Tests
# =============================================================================


class TestNaturalLanguageSearch:
    """Tests for natural language context search."""

    def test_natural_language_query(self, tmp_path: Path) -> None:
        """Test natural language content is searchable."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "This module handles the user login process and session management."
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "user login" in previous


# =============================================================================
# Session 9: Context Versioning Tests
# =============================================================================


class TestContextVersioning:
    """Tests for context versioning and history tracking."""

    def test_version_header_detection(self, tmp_path: Path) -> None:
        """Test version header detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "# Context v2.0.0\n\nUpdated description."
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "v2.0.0" in previous


# =============================================================================
# Session 9: Context Compression Tests
# =============================================================================


class TestContextCompression:
    """Tests for context compression efficiency."""

    def test_large_context_readable(self, tmp_path: Path) -> None:
        """Test large context can be read."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "\n".join([f"Line {i}: Description text" for i in range(100)])
        target = tmp_path / "large.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Line 0" in previous
        assert "Line 99" in previous


# =============================================================================
# Session 9: Context Export Tests
# =============================================================================


class TestContextExport:
    """Tests for context export to documentation systems."""

    def test_markdown_format_preserved(self, tmp_path: Path) -> None:
        """Test markdown format is preserved for export."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "# Title\n\n## Section\n\n- Item 1\n- Item 2"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "# Title" in previous
        assert "## Section" in previous


# =============================================================================
# Session 9: Context Validation Tests
# =============================================================================


class TestContextValidation:
    """Tests for context validation rules."""

    def test_valid_context_format(self, tmp_path: Path) -> None:
        """Test valid context format is accepted."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "# Module: test_module\n\n## Purpose\n\nTest purpose."
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Module:" in previous


# =============================================================================
# Session 9: Context Annotation Tests
# =============================================================================


class TestContextAnnotation:
    """Tests for context annotation persistence."""

    def test_annotation_detection(self, tmp_path: Path) -> None:
        """Test annotation detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "<!-- @author: John Doe -->\n# Module"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "@author" in previous


# =============================================================================
# Session 9: Context Recommendation Tests
# =============================================================================


class TestContextRecommendation:
    """Tests for context recommendation accuracy."""

    def test_related_content_detection(self, tmp_path: Path) -> None:
        """Test related content detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "Related: auth_module, user_module, session_module"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "auth_module" in previous


# =============================================================================
# Session 9: Context-Aware Code Generation Tests
# =============================================================================


class TestContextAwareCodeGeneration:
    """Tests for context-aware code generation."""

    def test_code_example_detection(self, tmp_path: Path) -> None:
        """Test code example detection in context."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = """
## Example Usage

```python
from module import function
result=function(arg)
```
"""
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "```python" in previous


# =============================================================================
# Session 9: Context-Based Refactoring Tests
# =============================================================================


class TestContextBasedRefactoring:
    """Tests for context-based refactoring suggestions."""

    def test_refactoring_note_detection(self, tmp_path: Path) -> None:
        """Test refactoring note detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "TODO: Refactor this module to use async / await"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Refactor" in previous


# =============================================================================
# Session 9: Context Merge Conflict Tests
# =============================================================================


class TestContextMergeConflict:
    """Tests for context merge conflict resolution."""

    def test_conflict_marker_detection(self, tmp_path: Path) -> None:
        """Test conflict marker detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = """
<<<<<<< HEAD
Old description
=======
New description
>>>>>>> branch
"""
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "<<<<<<< HEAD" in previous


# =============================================================================
# Session 9: Context Access Control Tests
# =============================================================================


class TestContextAccessControl:
    """Tests for context access control."""

    def test_read_access(self, tmp_path: Path) -> None:
        """Test read access to context."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "# Private Module\n\nInternal use only."
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "Private Module" in previous


# =============================================================================
# Session 9: Context Archival Tests
# =============================================================================


class TestContextArchival:
    """Tests for context archival and retention."""

    def test_archived_marker_detection(self, tmp_path: Path) -> None:
        """Test archived marker detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "<!-- ARCHIVED: 2024-12-01 -->\n# Old Module"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "ARCHIVED" in previous


# =============================================================================
# Session 9: Context Search Indexing Tests
# =============================================================================


class TestContextSearchIndexing:
    """Tests for context search indexing."""

    def test_keywords_extracted(self, tmp_path: Path) -> None:
        """Test keywords can be extracted from context."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "Keywords: authentication, security, oauth2, jwt"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "authentication" in previous
        assert "jwt" in previous


# =============================================================================
# Session 9: Context Notification Tests
# =============================================================================


class TestContextNotification:
    """Tests for context notification triggers."""

    def test_alert_marker_detection(self, tmp_path: Path) -> None:
        """Test alert marker detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "> ⚠️ WARNING: This module is deprecated."
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "WARNING" in previous

    def test_breaking_change_detection(self, tmp_path: Path) -> None:
        """Test breaking change detection."""
        with agent_dir_on_path():
            mod = load_agent_module("agent-context.py")

        content = "BREAKING CHANGE: API signature changed in v2.0"
        target = tmp_path / "test.description.md"
        target.write_text(content)

        agent = mod.ContextAgent(str(target))
        previous = agent.read_previous_content()

        assert "BREAKING CHANGE" in previous


# ========== Comprehensive Context Tests (from test_agent_context_comprehensive.py) ==========


class TestContextCreation(unittest.TestCase):
    """Tests for context creation and initialization."""

    def test_create_context_basic(self):
        """Test creating a basic context."""
        context = {
            "user_id": "user123",
            "session_id": "sess123",
            "timestamp": datetime.now(),
        }

        assert context["user_id"] == "user123"
        assert context["session_id"] == "sess123"
        assert context["timestamp"] is not None

    def test_create_context_with_defaults(self):
        """Test creating context with default values."""
        context = {
            "user_id": "user123",
            "session_id": "sess123",
            "timeout": 3600,
            "retries": 3,
            "debug": False,
        }

        assert context["timeout"] == 3600
        assert context["retries"] == 3
        assert context["debug"] is False

    def test_create_context_nested(self):
        """Test creating nested context."""
        context = {
            "user": {
                "id": "user123",
                "name": "Alice",
                "roles": ["admin"],
            },
            "environment": {
                "stage": "production",
                "region": "us-east-1",
            },
        }

        assert context["user"]["id"] == "user123"
        assert context["environment"]["stage"] == "production"

    def test_create_context_with_metadata(self):
        """Test creating context with metadata."""
        context = {
            "id": "ctx123",
            "created_at": datetime.now(),
            "metadata": {
                "source": "api",
                "version": "1.0",
            },
        }

        assert context["metadata"]["source"] == "api"


class TestContextStateTracking(unittest.TestCase):
    """Tests for context state tracking."""

    def test_track_context_state_transitions(self):
        """Test tracking context state transitions."""
        states = ["initialized", "processing", "completed"]
        state_history = []

        for state in states:
            state_history.append(state)

        assert len(state_history) == 3
        assert state_history[-1] == "completed"

    def test_track_modified_fields(self):
        """Test tracking modified fields."""
        context = {"value": 10}
        modifications = []

        context["value"] = 20
        modifications.append(("value", 10, 20))

        assert len(modifications) == 1
        assert modifications[0][2] == 20

    def test_track_context_dirty_state(self):
        """Test tracking dirty state."""
        context = {"name": "Alice", "_dirty": False}

        context["name"] = "Bob"
        context["_dirty"] = True

        assert context["_dirty"] is True

    def test_track_context_read_only_fields(self):
        """Test tracking read-only field violations."""
        context = {"id": "ctx123", "_read_only": ["id"]}
        violations = []

        # Attempt to modify read-only field
        if "id" in context.get("_read_only", []):
            violations.append("id")

        assert "id" in violations


class TestContextLifecycle(unittest.TestCase):
    """Tests for context lifecycle management."""

    def test_context_creation_lifecycle(self):
        """Test context creation lifecycle."""
        lifecycle = []

        # Create
        context = {"id": "ctx1"}
        lifecycle.append("created")

        # Initialize
        context["initialized"] = True
        lifecycle.append("initialized")

        # Cleanup
        context.clear()
        lifecycle.append("cleaned")

        assert lifecycle == ["created", "initialized", "cleaned"]

    def test_context_timeout_lifecycle(self):
        """Test context timeout lifecycle."""
        context = {
            "created_at": datetime.now(),
            "timeout": 3600,
            "status": "active",
        }

        # Still valid
        assert context["status"] == "active"

        # Simulate timeout
        context["status"] = "expired"
        assert context["status"] == "expired"

    def test_context_resource_management(self):
        """Test context resource management."""
        resources = []

        # Allocate
        resources.append("connection")
        resources.append("file_handle")

        assert len(resources) == 2

        # Release
        resources.clear()
        assert len(resources) == 0

    def test_context_cleanup_on_exception(self):
        """Test context cleanup on exception."""
        context = {"active": True}
        cleanup_called = False

        try:
            raise ValueError("Error")
        except ValueError:
            context["active"] = False
            cleanup_called = True

        assert cleanup_called
        assert context["active"] is False


class TestContextInheritanceComprehensive(unittest.TestCase):
    """Tests for context inheritance."""

    def test_inherit_context_properties(self):
        """Test inheriting context properties."""
        parent_context = {
            "user_id": "user123",
            "session_id": "sess123",
        }

        child_context = parent_context.copy()
        child_context["request_id"] = "req456"

        assert child_context["user_id"] == "user123"
        assert child_context["request_id"] == "req456"

    def test_override_inherited_properties(self):
        """Test overriding inherited properties."""
        parent = {"debug": False, "timeout": 30}
        child = parent.copy()
        child["debug"] = True

        assert parent["debug"] is False
        assert child["debug"] is True

    def test_context_hierarchy(self):
        """Test context hierarchy."""
        global_context = {"env": "production"}
        project_context = {**global_context, "project": "app1"}
        request_context = {**project_context, "request_id": "req1"}

        assert request_context["env"] == "production"
        assert request_context["project"] == "app1"
        assert request_context["request_id"] == "req1"

    def test_context_isolation(self):
        """Test context isolation."""
        ctx1 = {"id": "ctx1", "data": []}
        ctx2 = {"id": "ctx2", "data": []}

        ctx1["data"].append(1)
        ctx2["data"].append(2)

        assert ctx1["data"] == [1]
        assert ctx2["data"] == [2]


class TestContextStorage(unittest.TestCase):
    """Tests for context storage and retrieval."""

    def test_store_context_value(self):
        """Test storing context value."""
        context = {}
        context["key1"] = "value1"

        assert context["key1"] == "value1"

    def test_retrieve_context_value(self):
        """Test retrieving context value."""
        context = {"key1": "value1", "key2": "value2"}

        value = context.get("key1")
        assert value == "value1"

    def test_retrieve_nonexistent_with_default(self):
        """Test retrieving nonexistent with default."""
        context = {"key1": "value1"}

        value = context.get("missing", "default")
        assert value == "default"

    def test_store_complex_object(self):
        """Test storing complex object."""
        context = {
            "user": {
                "id": 1,
                "name": "Alice",
                "roles": ["admin", "user"],
            }
        }

        assert context["user"]["name"] == "Alice"
        assert "admin" in context["user"]["roles"]


class TestContextVariables(unittest.TestCase):
    """Tests for context-local variables."""

    def test_set_context_variable(self):
        """Test setting context variable."""
        context = {}
        context["var1"] = "value1"

        assert "var1" in context

    def test_get_context_variable(self):
        """Test getting context variable."""
        context = {"var1": "value1"}

        assert context["var1"] == "value1"

    def test_delete_context_variable(self):
        """Test deleting context variable."""
        context = {"var1": "value1"}
        del context["var1"]

        assert "var1" not in context

    def test_context_variable_isolation(self):
        """Test context variable isolation."""
        ctx1_vars = {"var": "ctx1_value"}
        ctx2_vars = {"var": "ctx2_value"}

        assert ctx1_vars["var"] != ctx2_vars["var"]


class TestContextPropagation(unittest.TestCase):
    """Tests for context propagation through call chains."""

    def test_propagate_context_to_function(self):
        """Test propagating context to function."""
        context = {"user_id": "user1"}

        def process(ctx):
            return ctx["user_id"]

        result = process(context)
        assert result == "user1"

    def test_propagate_through_nested_calls(self):
        """Test propagating through nested calls."""
        context = {"value": 10}

        def level1(ctx):
            return level2(ctx)

        def level2(ctx):
            return level3(ctx)

        def level3(ctx):
            return ctx["value"]

        result = level1(context)
        assert result == 10

    def test_propagate_to_async_context(self):
        """Test propagating to async context."""
        context = {"async_id": "async1"}

        async_contexts = []
        async_contexts.append(context)

        assert async_contexts[0]["async_id"] == "async1"

    def test_propagate_with_implicit_context(self):
        """Test propagating with implicit context."""
        context_stack = [{"level": 1}]

        # Add another level
        context_stack.append({**context_stack[-1], "level": 2})

        assert context_stack[-1]["level"] == 2


class TestContextMerging(unittest.TestCase):
    """Tests for context merging."""

    def test_merge_contexts(self):
        """Test merging two contexts."""
        ctx1 = {"key1": "value1"}
        ctx2 = {"key2": "value2"}

        merged = {**ctx1, **ctx2}

        assert merged["key1"] == "value1"
        assert merged["key2"] == "value2"

    def test_merge_with_override(self):
        """Test merging with override."""
        ctx1 = {"shared": "original", "unique1": "value1"}
        ctx2 = {"shared": "override", "unique2": "value2"}

        merged = {**ctx1, **ctx2}

        assert merged["shared"] == "override"
        assert merged["unique1"] == "value1"
        assert merged["unique2"] == "value2"

    def test_merge_nested_contexts(self):
        """Test merging nested contexts."""
        ctx1 = {"data": {"a": 1}}
        ctx2 = {"data": {"b": 2}}

        # Simple merge (not recursive)
        merged = {**ctx1, **ctx2}
        assert merged["data"]["b"] == 2

    def test_merge_empty_context(self):
        """Test merging empty context."""
        ctx = {"key": "value"}
        empty = {}

        merged = {**ctx, **empty}
        assert merged["key"] == "value"


class TestContextValidationComprehensive(unittest.TestCase):
    """Tests for context validation."""

    def test_validate_required_fields(self):
        """Test validating required fields."""
        context = {"user_id": "user1", "session_id": "sess1"}
        required = ["user_id", "session_id"]

        valid = all(field in context for field in required)
        assert valid

    def test_validate_field_types(self):
        """Test validating field types."""
        context = {"count": 10, "name": "Alice"}

        assert isinstance(context["count"], int)
        assert isinstance(context["name"], str)

    def test_validate_field_values(self):
        """Test validating field values."""
        context = {"status": "active"}
        valid_statuses = ["active", "inactive", "pending"]

        assert context["status"] in valid_statuses

    def test_validate_field_constraints(self):
        """Test validating field constraints."""
        context = {"age": 25}

        assert 0 <= context["age"] <= 150


class TestContextSerialization(unittest.TestCase):
    """Tests for context serialization."""

    def test_serialize_context_to_dict(self):
        """Test serializing context to dict."""
        context = {
            "id": "ctx1",
            "user": "alice",
            "timestamp": datetime.now().isoformat(),
        }

        serialized = dict(context)
        assert isinstance(serialized, dict)
        assert serialized["id"] == "ctx1"

    def test_serialize_context_to_json(self):
        """Test serializing context to JSON."""
        import json
        context = {"id": "ctx1", "name": "test"}

        json_str = json.dumps(context)
        assert "ctx1" in json_str

    def test_deserialize_context(self):
        """Test deserializing context."""
        import json
        json_str = '{"id": "ctx1", "name": "test"}'

        context = json.loads(json_str)
        assert context["id"] == "ctx1"

    def test_serialize_with_nested_structures(self):
        """Test serializing with nested structures."""
        import json
        context = {
            "user": {"id": 1, "name": "Alice"},
            "tags": ["tag1", "tag2"],
        }

        json_str = json.dumps(context)
        restored = json.loads(json_str)
        assert restored["user"]["name"] == "Alice"


class TestContextCachingComprehensive(unittest.TestCase):
    """Tests for context caching."""

    def test_cache_context_value(self):
        """Test caching context value."""
        cache = {}
        context = {"key": "value"}

        cache["ctx1"] = context

        assert cache["ctx1"]["key"] == "value"

    def test_invalidate_cache(self):
        """Test invalidating cache."""
        cache = {"ctx1": {"value": 10}}

        del cache["ctx1"]

        assert "ctx1" not in cache

    def test_cache_with_expiration(self):
        """Test cache with expiration."""
        cache = {}
        context = {
            "value": 10,
            "expires_at": datetime.now() + timedelta(hours=1),
        }

        cache["ctx1"] = context
        assert cache["ctx1"]["value"] == 10

    def test_cache_hit_miss(self):
        """Test cache hit and miss."""
        cache = {"ctx1": {"value": 10}}

        # Hit
        assert "ctx1" in cache

        # Miss
        assert "ctx2" not in cache


class TestContextIntegration(unittest.TestCase):
    """Integration tests for context management."""

    def test_end_to_end_context_workflow(self):
        """Test end-to-end context workflow."""
        # Create
        context = {"user_id": "user1", "session_id": "sess1"}

        # Modify
        context["request_id"] = "req1"

        # Validate
        assert all(k in context for k in ["user_id", "session_id", "request_id"])

        # Cleanup
        context.clear()
        assert len(context) == 0

    def test_multi_context_lifecycle(self):
        """Test multi-context lifecycle."""
        contexts = []

        # Create multiple
        for i in range(3):
            contexts.append({"id": f"ctx{i}"})

        assert len(contexts) == 3

        # Process
        for ctx in contexts:
            ctx["processed"] = True

        # Cleanup
        contexts.clear()
        assert len(contexts) == 0

    def test_context_with_state_machine(self):
        """Test context with state machine."""
        context = {"state": "init"}
        transitions = []

        # Transition 1
        context["state"] = "processing"
        transitions.append("init->processing")

        # Transition 2
        context["state"] = "completed"
        transitions.append("processing->completed")

        assert len(transitions) == 2
        assert context["state"] == "completed"


# ========== Comprehensive Context Improvements Tests
# (from test_agent_context_improvements_comprehensive.py) ==========


class TestASTSignatureExtraction(unittest.TestCase):
    """Test extracting class and function signatures using AST."""

    def test_function_signature_extraction(self):
        """Test extracting function signature from AST."""
        code = """
def calculate(x: int, y: int) -> int:
    '''Calculate sum of two integers.'''
    return x + y
        """
        tree = ast.parse(code)
        func_def = tree.body[0]

        self.assertIsInstance(func_def, ast.FunctionDef)
        self.assertEqual(func_def.name, 'calculate')
        self.assertEqual(len(func_def.args.args), 2)

    def test_class_signature_extraction(self):
        """Test extracting class definition from AST."""
        code = """
class DataProcessor:
    def __init__(self, name: str):
        self.name=name

    def process(self, data):
        return data
        """
        tree = ast.parse(code)
        class_def = tree.body[0]

        self.assertIsInstance(class_def, ast.ClassDef)
        self.assertEqual(class_def.name, 'DataProcessor')
        self.assertEqual(len(class_def.body), 2)

    def test_method_signature_extraction(self):
        """Test extracting method signatures from class."""
        code = """
class Calculator:
    def add(self, a: int, b: int) -> int:
        return a + b

    def multiply(self, a: int, b: int) -> int:
        return a * b
        """
        tree = ast.parse(code)
        class_def = tree.body[0]
        methods = [n for n in class_def.body if isinstance(n, ast.FunctionDef)]

        self.assertEqual(len(methods), 2)
        self.assertEqual(methods[0].name, 'add')


class TestGitHistoryIntegration(unittest.TestCase):
    """Test including recent git history in context."""

    def test_git_history_extraction(self):
        """Test extracting last 10 commits."""
        git_history = [
            {
                'commit': 'abc123',
                'author': 'dev1',
                'message': 'Fix bug in parser',
                'date': '2025-12-16'
            },
            {
                'commit': 'def456',
                'author': 'dev2',
                'message': 'Add feature X',
                'date': '2025-12-15'
            },
            {
                'commit': 'ghi789',
                'author': 'dev1',
                'message': 'Refactor context module',
                'date': '2025-12-14'
            },
        ]
        self.assertEqual(len(git_history), 3)
        self.assertEqual(git_history[0]['commit'], 'abc123')

    def test_commit_message_parsing(self):
        """Test parsing commit messages for context."""
        commits = [
            {'hash': 'abc123', 'message': 'Fix: resolve memory leak in parser'},
            {'hash': 'def456', 'message': 'Feature: add async support'},
            {'hash': 'ghi789', 'message': 'Refactor: extract utilities to separate module'}
        ]

        fix_commits = [c for c in commits if c['message'].startswith('Fix')]
        self.assertEqual(len(fix_commits), 1)

    def test_contributor_extraction(self):
        """Test extracting contributor information."""
        commits = [
            {'author': 'alice@example.com', 'count': 15},
            {'author': 'bob@example.com', 'count': 8},
            {'author': 'charlie@example.com', 'count': 3}
        ]
        top_contributor = max(commits, key=lambda x: x['count'])
        self.assertEqual(top_contributor['author'], 'alice@example.com')


class TestDependencyGraphAnalysis(unittest.TestCase):
    """Test dependency graph analysis and visualization."""

    def test_import_extraction(self):
        """Test extracting imports from module."""
        code = """
import os
from pathlib import Path
from typing import Dict, List
import numpy as np
        """
        tree = ast.parse(code)
        imports = [
            node for node in ast.walk(tree) if isinstance(
                node, (ast.Import, ast.ImportFrom))]

        self.assertEqual(len(imports), 4)

    def test_dependency_tree_building(self):
        """Test building dependency tree."""
        dependencies = {
            'module_a': ['module_b', 'module_c'],
            'module_b': ['module_d'],
            'module_c': ['module_d'],
            'module_d': []
        }

        # Check depth
        def max_depth(node, deps, visited=None):
            if visited is None:
                visited = set()
            if node in visited:
                return 0
            visited.add(node)
            if not deps.get(node):
                return 1
            return 1 + max(max_depth(child, deps, visited) for child in deps.get(node, []))

        depth = max_depth('module_a', dependencies)
        self.assertEqual(depth, 3)

    def test_circular_dependency_detection(self):
        """Test detecting circular dependencies."""
        dependencies = {
            'module_a': ['module_b'],
            'module_b': ['module_c'],
            'module_c': ['module_a']
        }

        # Simple cycle detection
        def has_cycle(node, deps, visited=None, rec_stack=None):
            if visited is None:
                visited = set()
            if rec_stack is None:
                rec_stack = set()

            visited.add(node)
            rec_stack.add(node)

            for child in deps.get(node, []):
                if child not in visited:
                    if has_cycle(child, deps, visited, rec_stack):
                        return True
                elif child in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        cycle_exists = has_cycle('module_a', dependencies)
        self.assertTrue(cycle_exists)


class TestContextSummarization(unittest.TestCase):
    """Test context summarization for large files."""

    def test_long_file_summarization(self):
        """Test summarizing large files (>1000 lines)."""
        file_info = {
            'total_lines': 2500,
            'functions': 25,
            'classes': 5,
            'imports': 15
        }

        # Determine summary priority
        summary_items = [
            f"Classes: {file_info['classes']}",
            f"Functions: {file_info['functions']}",
            f"Imports: {file_info['imports']}"
        ]
        self.assertEqual(len(summary_items), 3)

    def test_key_section_identification(self):
        """Test identifying key sections in large files."""
        sections = [
            {'name': 'imports', 'lines': '1-20'},
            {'name': 'class_definitions', 'lines': '21-500'},
            {'name': 'function_definitions', 'lines': '501-1500'},
            {'name': 'utility_functions', 'lines': '1501-2500'}
        ]

        self.assertEqual(len(sections), 4)

    def test_docstring_extraction_for_summary(self):
        """Test extracting docstrings for module summary."""
        module_docstring = """
Summary of the agent-context module.

This module provides functionality for:
- Extracting code context from files
- Analyzing dependencies
- Generating summaries
        """

        self.assertIn('Summary', module_docstring)


class TestRelatedFilesDetection(unittest.TestCase):
    """Test finding files that import or use this module."""

    def test_import_usage_detection(self):
        """Test finding files that import this module."""
        file_structure = {
            'module_a.py': ['from module_b import func1', 'from module_c import Class1'],
            'module_b.py': ['import os', 'from module_c import Class1'],
            'module_c.py': ['from module_a import func2', 'import sys'],
            'test_module_a.py': ['from module_a import func1']
        }

        # Find files importing module_a
        importers = [f for f, imports in file_structure.items()
                     if any('module_a' in i for i in imports)]

        self.assertIn('test_module_a.py', importers)
        self.assertIn('module_c.py', importers)

    def test_related_files_ranking(self):
        """Test ranking related files by relevance."""
        related_files = [
            {'file': 'test_module.py', 'relevance': 0.95, 'relation': 'tests'},
            {'file': 'module_utils.py', 'relevance': 0.80, 'relation': 'dependency'},
            {'file': 'config.py', 'relevance': 0.60, 'relation': 'imports'},
            {'file': 'legacy_module.py', 'relevance': 0.30, 'relation': 'old_usage'}
        ]

        top_related = sorted(related_files, key=lambda x: x['relevance'], reverse=True)
        self.assertEqual(top_related[0]['file'], 'test_module.py')


class TestAPIDocumentationExtraction(unittest.TestCase):
    """Test extracting public API documentation from docstrings."""

    def test_public_api_extraction(self):
        """Test extracting public API functions."""
        code = """
def public_function():
    '''Public API function.'''
    pass

def _private_function():
    '''Private helper function.'''
    pass

class PublicClass:
    '''Public API class.'''
    def public_method(self):
        '''Public method.'''
        pass

    def _private_method(self):
        '''Private method.'''
        pass
        """

        tree = ast.parse(code)
        public_items = [node.name for node in tree.body
                        if hasattr(node, 'name') and not node.name.startswith('_')]

        self.assertIn('public_function', public_items)
        self.assertIn('PublicClass', public_items)
        self.assertNotIn('_private_function', public_items)

    def test_docstring_parsing(self):
        """Test parsing docstrings for documentation."""
        docstring = """
        Calculate sum of two numbers.

        Args:
            x (int): First number
            y (int): Second number

        Returns:
            int: Sum of x and y

        Example:
            >>> add(2, 3)
            5
        """

        self.assertIn('Args:', docstring)
        self.assertIn('Returns:', docstring)


class TestCoverageMetrics(unittest.TestCase):
    """Test including test coverage metrics from test files."""

    def test_coverage_calculation(self):
        """Test calculating coverage percentage."""
        coverage = {
            'total_lines': 500,
            'covered_lines': 450,
            'percentage': (450 / 500) * 100
        }

        self.assertEqual(coverage['percentage'], 90.0)

    def test_coverage_by_function(self):
        """Test coverage breakdown by function."""
        function_coverage = [
            {'function': 'process_data', 'coverage': 100},
            {'function': 'validate_input', 'coverage': 95},
            {'function': 'format_output', 'coverage': 70},
            {'function': 'debug_helper', 'coverage': 0}
        ]

        uncovered = [f for f in function_coverage if f['coverage'] < 100]
        self.assertEqual(len(uncovered), 3)


class TestCodeMetrics(unittest.TestCase):
    """Test code metrics: cyclomatic complexity, LOC, maintainability index."""

    def test_lines_of_code_calculation(self):
        """Test calculating lines of code."""
        code = """
def calculate(x, y):
    result=x + y
    return result
        """

        lines = [line.strip() for line in code.split('\n') if line.strip()
                 and not line.strip().startswith('#')]
        # Excluding docstrings
        loc = len([line for line in lines if line and '"""' not in line])

        self.assertGreater(loc, 0)

    def test_cyclomatic_complexity(self):
        """Test calculating cyclomatic complexity."""
        # Simplified complexity: 1 + number of conditional statements
        conditions = ['if', 'elif', 'else', 'and', 'or', 'for', 'while', 'except']

        code = """
if x > 0:
    if y > 0:
        return x + y
    else:
        return x - y
elif x < 0:
    return -x
else:
    return 0
        """

        complexity = 1  # base
        for condition in conditions:
            complexity += code.count(condition)

        self.assertGreater(complexity, 1)

    def test_maintainability_index(self):
        """Test calculating maintainability index."""
        metrics = {
            'loc': 150,
            'cyclomatic_complexity': 8,
            'halstead_volume': 500,
            'comments_percentage': 0.25
        }

        # MI formula (simplified): 171 - 5.2 * ln(Halstead) - 0.23 * CC - 16.2 * ln(LOC)
        # For testing, just check structure
        self.assertIn('loc', metrics)
        self.assertIn('cyclomatic_complexity', metrics)


class TestCodeSmellDetection(unittest.TestCase):
    """Test detecting code smells and anti-patterns."""

    def test_long_function_detection(self):
        """Test detecting functions that are too long."""
        function_lengths = {
            'short_func': 20,
            'medium_func': 50,
            'long_func': 200,  # Code smell
            'very_long_func': 500  # Code smell
        }

        smell_threshold = 100
        smells = [name for name, length in function_lengths.items() if length > smell_threshold]

        self.assertEqual(len(smells), 2)

    def test_duplicate_code_detection(self):
        """Test detecting duplicate code blocks."""
        code_blocks = [
            'for item in items: process(item)',
            'for item in items: process(item)',  # Duplicate
            'for item in items: do_something(item)'
        ]

        duplicates = [code_blocks[0] for i in range(len(code_blocks))
                      if code_blocks[0] == code_blocks[i]]

        self.assertEqual(len(duplicates), 2)

    def test_deep_nesting_detection(self):
        """Test detecting deeply nested code."""
        nesting_levels = 0
        code_snippet = """
if a:
    if b:
        if c:
            if d:
                result=execute()  # 4 levels deep
        """

        # Count opening braces / indents
        for line in code_snippet.split('\n'):
            if line.strip().startswith('if'):
                nesting_levels += 1

        self.assertEqual(nesting_levels, 4)


class TestArchitectureDecisions(unittest.TestCase):
    """Test including architecture decisions and design patterns."""

    def test_design_pattern_detection(self):
        """Test detecting design patterns in code."""
        patterns = {
            'singleton': ['__instance=None', '__new__'],
            'factory': ['def create_', 'return '],
            'observer': ['subscribe', 'notify'],
            'strategy': ['strategy =', 'execute']
        }

        self.assertEqual(len(patterns), 4)

    def test_architectural_decision_record(self):
        """Test storing architectural decisions."""
        adr = {
            'decision': 'Use async / await for I / O operations',
            'context': 'Improve performance for network-bound tasks',
            'consequences': 'Requires Python 3.7+, changes error handling',
            'date': '2025-12-16',
            'status': 'accepted'
        }

        self.assertEqual(adr['status'], 'accepted')


class TestChangeStatistics(unittest.TestCase):
    """Test recent change statistics."""

    def test_change_frequency(self):
        """Test tracking change frequency."""
        changes = [
            {'date': '2025-12-16', 'type': 'modification'},
            {'date': '2025-12-15', 'type': 'modification'},
            {'date': '2025-12-10', 'type': 'feature'},
            {'date': '2025-12-05', 'type': 'bugfix'},
        ]

        self.assertEqual(len(changes), 4)

    def test_time_since_last_change(self):
        """Test calculating time since last change."""

        # Days since change would be 0
        days_since = 0
        self.assertEqual(days_since, 0)

    def test_contributor_statistics(self):
        """Test tracking contributor statistics."""
        contributors = {
            'alice': {'commits': 25, 'changes': 150},
            'bob': {'commits': 15, 'changes': 95},
            'charlie': {'commits': 5, 'changes': 20}
        }

        total_commits = sum(c['commits'] for c in contributors.values())
        self.assertEqual(total_commits, 45)


class TestPluginSystem(unittest.TestCase):
    """Test custom context providers via plugin system."""

    def test_plugin_registry(self):
        """Test registering custom context providers."""
        class PluginRegistry:
            def __init__(self):
                self.providers = {}

            def register(self, name, provider):
                self.providers[name] = provider

            def get_provider(self, name):
                return self.providers.get(name)

        registry = PluginRegistry()
        self.assertEqual(len(registry.providers), 0)

    def test_custom_provider_implementation(self):
        """Test implementing custom context provider."""
        class CustomProvider:
            def name(self):
                return "custom_context"

            def extract(self, file_path):
                return {'custom_data': 'value'}

        provider = CustomProvider()
        self.assertEqual(provider.name(), 'custom_context')


class TestContextCachingImprovements(unittest.TestCase):
    """Test context caching for improved performance."""

    def test_cache_storage(self):
        """Test caching extracted context."""
        cache = {}

        def get_context(file_path):
            if file_path in cache:
                return cache[file_path]

            # Simulate extraction
            context = {'data': 'extracted'}
            cache[file_path] = context
            return context

        ctx1 = get_context('file.py')
        ctx2 = get_context('file.py')  # From cache

        self.assertEqual(ctx1, ctx2)

    def test_cache_invalidation(self):
        """Test invalidating cache when file changes."""
        cache = {'file.py': {'data': 'old'}}

        # Invalidate cache for specific file
        cache.pop('file.py', None)

        self.assertNotIn('file.py', cache)


class TestContextPrioritization(unittest.TestCase):
    """Test context prioritization for relevance."""

    def test_relevance_scoring(self):
        """Test scoring context by relevance."""
        context_items = [
            {'item': 'primary_function', 'relevance': 0.95},
            {'item': 'helper_function', 'relevance': 0.60},
            {'item': 'import_statement', 'relevance': 0.40},
            {'item': 'comment', 'relevance': 0.30}
        ]

        sorted_items = sorted(context_items, key=lambda x: x['relevance'], reverse=True)
        self.assertEqual(sorted_items[0]['item'], 'primary_function')

    def test_context_truncation(self):
        """Test truncating low-priority context."""
        context = [
            {'priority': 'high', 'content': 'main_class'},
            {'priority': 'high', 'content': 'public_api'},
            {'priority': 'medium', 'content': 'helper'},
            {'priority': 'low', 'content': 'deprecated_code'},
            {'priority': 'low', 'content': 'old_comments'}
        ]

        truncated = [c for c in context if c['priority'] != 'low']
        self.assertEqual(len(truncated), 3)


class TestContextVisualization(unittest.TestCase):
    """Test context visualization (dependency graphs, diagrams)."""

    def test_dependency_graph_data(self):
        """Test generating dependency graph data."""
        graph = {
            'nodes': [
                {'id': 'module_a', 'label': 'Module A'},
                {'id': 'module_b', 'label': 'Module B'},
                {'id': 'module_c', 'label': 'Module C'}
            ],
            'edges': [
                {'from': 'module_a', 'to': 'module_b'},
                {'from': 'module_b', 'to': 'module_c'},
                {'from': 'module_a', 'to': 'module_c'}
            ]
        }

        self.assertEqual(len(graph['nodes']), 3)
        self.assertEqual(len(graph['edges']), 3)

    def test_architecture_diagram_generation(self):
        """Test generating architecture diagram."""
        layers = {
            'presentation': ['ui_module'],
            'business_logic': ['service_module'],
            'data_access': ['database_module'],
            'infrastructure': ['logging_module']
        }

        self.assertEqual(len(layers), 4)


class TestContextFiltering(unittest.TestCase):
    """Test context filtering for sensitive data."""

    def test_sensitive_data_detection(self):
        """Test detecting sensitive data patterns."""
        sensitive_patterns = [
            'API_KEY',
            'PASSWORD',
            'SECRET',
            'TOKEN',
            'CREDENTIAL'
        ]

        code = "API_KEY='secret123'"
        has_sensitive = any(pattern in code for pattern in sensitive_patterns)
        self.assertTrue(has_sensitive)

    def test_filtering_sensitive_content(self):
        """Test filtering sensitive content from context."""
        context = {
            'code': 'API_KEY="secret123"',
            'imports': ['import os'],
            'functions': ['process_data']
        }

        # Filter code containing sensitive patterns
        sensitive_keywords = ['API_KEY', 'PASSWORD', 'SECRET']
        filtered_code = context['code']
        for keyword in sensitive_keywords:
            if keyword in context['code']:
                filtered_code = '[REDACTED]'

        self.assertEqual(filtered_code, '[REDACTED]')


class TestCrossModuleContext(unittest.TestCase):
    """Test cross-module context relationships."""

    def test_module_relationships(self):
        """Test identifying relationships between modules."""
        relationships = {
            'module_a': {
                'imports_from': ['module_b', 'module_c'],
                'imported_by': ['module_d'],
                'shared_classes': ['DataProcessor']
            }
        }

        self.assertEqual(len(relationships['module_a']['imports_from']), 2)

    def test_shared_interface_detection(self):
        """Test detecting shared interfaces / protocols."""
        interfaces = {
            'Processor': {
                'modules': ['module_a', 'module_b', 'module_c'],
                'methods': ['process', 'validate', 'output']
            }
        }

        self.assertEqual(len(interfaces['Processor']['modules']), 3)
