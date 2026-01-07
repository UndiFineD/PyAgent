#!/usr/bin/env python3

"""Auto-extracted class from agent_context.py"""

from __future__ import annotations

from .ContextAnnotation import ContextAnnotation
from .ContextPriority import ContextPriority
from .ContextTag import ContextTag
from .ContextTemplate import ContextTemplate
from .ContextVersion import ContextVersion
from .FileCategory import FileCategory
from .ValidationRule import ValidationRule

from src.classes.base_agent import BaseAgent
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import hashlib
import json
import logging
import re
import zlib

# Default templates for common file types
DEFAULT_TEMPLATES: Dict[str, ContextTemplate] = {
    "python": ContextTemplate(
        name="Python Module",
        file_type=".py",
        sections=["Purpose", "Classes", "Functions", "Dependencies", "Usage"],
        template_content="""# Description: `{filename}`

## Purpose
[Describe the module's purpose]

## Classes
[List and describe classes]

## Functions
[List and describe key functions]

## Dependencies
[List required packages and modules]

## Usage
```python
# Example usage
```
""",
        required_fields=["Purpose"]
    ),
    "javascript": ContextTemplate(
        name="JavaScript Module",
        file_type=".js",
        sections=["Purpose", "Exports", "Dependencies", "Usage"],
        template_content="""# Description: `{filename}`

## Purpose
[Describe the module's purpose]

## Exports
[List exported functions, classes, constants]

## Dependencies
[List npm packages and local imports]

## Usage
```javascript
// Example usage
```
""",
        required_fields=["Purpose"]
    ),
    "shell": ContextTemplate(
        name="Shell Script",
        file_type=".sh",
        sections=["Purpose", "Usage", "Arguments", "Environment Variables"],
        template_content="""# Description: `{filename}`

## Purpose
[Describe the script's purpose]

## Usage
```bash
./script.sh [options]
```

## Arguments
| Argument | Description | Required |
|----------|-------------|----------|
| -h       | Show help   | No       |

## Environment Variables
[List required environment variables]
""",
        required_fields=["Purpose", "Usage"]
    ),
    "config": ContextTemplate(
        name="Configuration File",
        file_type=".json/.yaml/.toml",
        sections=["Purpose", "Schema", "Options"],
        template_content="""# Description: `{filename}`

## Purpose
[Describe the configuration's purpose]

## Schema
[Describe the configuration structure]

## Options
| Option | Type | Default | Description |
|--------|------|---------|-------------|
|        |      |         |             |
""",
        required_fields=["Purpose"]
    ),
    "test": ContextTemplate(
        name="Test File",
        file_type="_test.py / test_.py",
        sections=["Purpose", "Test Cases", "Fixtures", "Coverage"],
        template_content="""# Description: `{filename}`

## Purpose
[Describe what this test file covers]

## Test Cases
[List test cases and their purposes]

## Fixtures
[Describe test fixtures used]

## Coverage
[Note which modules / functions are tested]
""",
        required_fields=["Purpose", "Test Cases"]
    ),
}

# Default validation rules
DEFAULT_VALIDATION_RULES: List[ValidationRule] = [
    ValidationRule(
        name="has_purpose",
        pattern=r"##\s*Purpose\b",
        message="Context should have a Purpose section",
        severity="error",
        required=True
    ),
    ValidationRule(
        name="no_empty_sections",
        pattern=r"##\s*\w+\s*\n\s*\n##",
        message="Empty section detected",
        severity="warning"
    ),
    ValidationRule(
        name="valid_code_blocks",
        pattern=r"```\w*\n[\s\S]*?```",
        message="Code blocks should have language identifier",
        severity="info"
    ),
]

class ContextAgent(BaseAgent):
    """Updates code file context descriptions using AI assistance."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        
        # Configuration
        self.config = {
            "extensions": [
                '.py', '.js', '.ts', '.go', '.rs', '.java', '.sh',
                '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg',
                '.md', '.rst', '.txt'
            ]
        }
        
        self._validate_file_extension()
        self.source_path = self._derive_source_path()

        # New features
        self._templates: Dict[str, ContextTemplate] = dict(DEFAULT_TEMPLATES)
        self._tags: Dict[str, ContextTag] = {}
        self._versions: List[ContextVersion] = []
        self._validation_rules: List[ValidationRule] = list(DEFAULT_VALIDATION_RULES)
        self._annotations: List[ContextAnnotation] = []
        self._priority: ContextPriority = ContextPriority.MEDIUM
        self._category: FileCategory = FileCategory.OTHER
        self._compressed_content: Optional[bytes] = None
        self._metadata: Dict[str, Any] = {}

    def _validate_file_extension(self) -> None:
        """Validate that the file has the correct extension."""
        if not self.file_path.name.endswith('.description.md'):
             logging.warning(f"File {self.file_path.name} does not end with .description.md. " 
                             "Context operations may be limited.")

    def _derive_source_path(self) -> Optional[Path]:
        """Derive source file path from .description.md filename."""
        if self.file_path.name.endswith('.description.md'):
            stem = self.file_path.name.replace('.description.md', '')
            # Use configurable extensions
            for ext in self.config.get("extensions", []):
                source = self.file_path.parent / f"{stem}{ext}"
                if source.exists():
                    return source
        return None

    # ========== Template Management ==========

    def set_template(self, template_name: str) -> bool:
        """Set the active template by name."""
        if template_name in self._templates:
            logging.info(f"Using template: {template_name}")
            return True
        logging.warning(f"Template '{template_name}' not found")
        return False

    def get_template_by_name(self, template_name: str) -> Optional[ContextTemplate]:
        """Get a template by name."""
        return self._templates.get(template_name.lower())

    def get_template(self, template_name: str) -> Optional[ContextTemplate]:
        """Compatibility alias: get a template by name.

        Tests and older callers use get_template(...); internally this agent
        stores templates in the _templates mapping.
        """
        return self._templates.get(template_name.lower())

    def add_template(self, template: ContextTemplate) -> None:
        """Add a custom template."""
        self._templates[template.name.lower()] = template
        logging.info(f"Added template: {template.name}")

    def get_template_for_file(self) -> Optional[ContextTemplate]:
        """Get the appropriate template for the current file."""
        if not self.source_path:
            return None

        ext = self.source_path.suffix.lower()
        name = self.source_path.name.lower()

        # Check test files first
        if "test" in name or name.startswith("test_"):
            return self._templates.get("test")

        # Match by extension
        ext_mapping = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "javascript",
            ".sh": "shell",
            ".bash": "shell",
            ".json": "config",
            ".yaml": "config",
            ".yml": "config",
            ".toml": "config",
        }

        template_name = ext_mapping.get(ext)
        return self._templates.get(template_name) if template_name else None

    def apply_template(self, template_name: Optional[str] = None) -> str:
        """Apply a template to generate initial content."""
        template = None
        if template_name:
            template = self._templates.get(template_name)
        else:
            template = self.get_template_for_file()

        if not template:
            return self._get_default_content()

        filename = self.file_path.name.replace('.description.md', '')
        return template.template_content.format(filename=filename)

    # ========== Tagging ==========

    def add_tag(self, tag: ContextTag) -> None:
        """Add a tag."""
        self._tags[tag.name] = tag

    def remove_tag(self, tag_name: str) -> bool:
        """Remove a tag."""
        if tag_name in self._tags:
            del self._tags[tag_name]
            return True
        return False

    def get_tags(self) -> List[ContextTag]:
        """Get all tags."""
        return list(self._tags.values())

    def has_tag(self, tag_name: str) -> bool:
        """Check if a tag exists."""
        return tag_name in self._tags

    def get_tags_by_parent(self, parent_name: str) -> List[ContextTag]:
        """Get all tags with a specific parent."""
        return [t for t in self._tags.values() if t.parent == parent_name]

    # ========== Versioning ==========

    def create_version(
        self,
        version: str,
        changes: Optional[List[str]] = None,
        author: str = ""
    ) -> ContextVersion:
        """Create a new version snapshot."""
        content = self.current_content or self.previous_content or ""
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:12]

        version_obj = ContextVersion(
            version=version,
            timestamp=datetime.now().isoformat(),
            content_hash=content_hash,
            changes=changes or [],
            author=author
        )

        self._versions.append(version_obj)
        logging.info(f"Created version {version}")
        return version_obj

    def get_versions(self) -> List[ContextVersion]:
        """Get all versions."""
        return self._versions

    def get_latest_version(self) -> Optional[ContextVersion]:
        """Get the latest version."""
        return self._versions[-1] if self._versions else None

    def get_version_diff(self, v1: str, v2: str) -> Dict[str, Any]:
        """Get diff between two versions."""
        ver1 = next((v for v in self._versions if v.version == v1), None)
        ver2 = next((v for v in self._versions if v.version == v2), None)

        if not ver1 or not ver2:
            return {"error": "Version not found"}

        return {
            "from_version": v1,
            "to_version": v2,
            "from_hash": ver1.content_hash,
            "to_hash": ver2.content_hash,
            "changed": ver1.content_hash != ver2.content_hash,
            "changes_v2": ver2.changes
        }

    # ========== Compression ==========

    def compress_content(self, content: Optional[str] = None) -> bytes:
        """Compress content for storage."""
        if content is None:
            content = self.current_content or self.previous_content or ""

        self._compressed_content = zlib.compress(content.encode(), level=9)
        return self._compressed_content

    def decompress_content(self, compressed: Optional[bytes] = None) -> str:
        """Decompress stored content."""
        if compressed is None:
            compressed = self._compressed_content

        if compressed is None:
            return ""

        return zlib.decompress(compressed).decode()

    def get_compression_ratio(self, content: Optional[str] = None) -> float:
        """Get compression ratio (space savings) for the current/previous content."""
        if content is None:
            content = self.current_content or self.previous_content or ""

        original_size = len(content.encode())
        if original_size == 0:
            return 0.0

        compressed = self._compressed_content
        if compressed is None:
            compressed = self.compress_content(content)
        compressed_size = len(compressed)
        return 1 - (compressed_size / original_size)

    # ========== Validation ==========

    def add_validation_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule."""
        self._validation_rules.append(rule)

    def validate_content(self, content: Optional[str] = None) -> List[Dict[str, Any]]:
        """Validate content against all rules."""
        if content is None:
            content = self.current_content or self.previous_content or ""

        issues: List[Dict[str, Any]] = []

        for rule in self._validation_rules:
            if rule.required:
                # Required patterns must be present
                if not re.search(rule.pattern, content):
                    issues.append({
                        "rule": rule.name,
                        "message": rule.message,
                        "severity": rule.severity,
                        "required": True
                    })
            else:
                # Non - required patterns are warnings when matched
                matches = re.findall(rule.pattern, content)
                if matches and rule.severity != "info":
                    issues.append({
                        "rule": rule.name,
                        "message": rule.message,
                        "severity": rule.severity,
                        "matches": len(matches)
                    })

        return issues

    def is_valid(self, content: Optional[str] = None) -> bool:
        """Check if content passes all required validations."""
        issues = self.validate_content(content)
        return not any(i.get("severity") == "error" for i in issues)

    # ========== Annotations ==========

    def add_annotation(
        self,
        line_number: int,
        content: str,
        author: str = ""
    ) -> ContextAnnotation:
        """Add an annotation to the context."""
        annotation = ContextAnnotation(
            id=hashlib.md5(f"{line_number}:{content}".encode()).hexdigest()[:8],
            line_number=line_number,
            content=content,
            author=author,
            timestamp=datetime.now().isoformat()
        )
        self._annotations.append(annotation)
        return annotation

    def get_annotations(self) -> List[ContextAnnotation]:
        """Get all annotations."""
        return self._annotations

    def get_annotations_for_line(self, line_number: int) -> List[ContextAnnotation]:
        """Get annotations for a specific line."""
        return [a for a in self._annotations if a.line_number == line_number]

    def resolve_annotation(self, annotation_id: str) -> bool:
        """Mark an annotation as resolved."""
        for annotation in self._annotations:
            if annotation.id == annotation_id:
                annotation.resolved = True
                return True
        return False

    def remove_annotation(self, annotation_id: str) -> bool:
        """Remove an annotation."""
        for i, annotation in enumerate(self._annotations):
            if annotation.id == annotation_id:
                del self._annotations[i]
                return True
        return False

    # ========== Priority Scoring ==========

    def set_priority(self, priority: ContextPriority) -> None:
        """Set the priority level."""
        self._priority = priority

    def get_priority(self) -> ContextPriority:
        """Get the priority level."""
        return self._priority

    def calculate_priority_score(self) -> float:
        """Calculate a priority score based on various factors."""
        score = 0.0
        content = self.current_content or self.previous_content or ""

        # Base score from priority level
        score += self._priority.value * 10

        # Add points for content completeness
        sections = ["Purpose", "Usage", "Dependencies", "Examples"]
        for section in sections:
            if f"## {section}" in content:
                score += 5

        # Add points for code examples
        code_blocks = re.findall(r"```\w+", content)
        score += min(len(code_blocks) * 3, 15)

        # Add points for having tags
        score += min(len(self._tags) * 2, 10)

        # Penalize for validation issues
        issues = self.validate_content(content)
        score -= len([i for i in issues if i.get("severity") == "error"]) * 10
        score -= len([i for i in issues if i.get("severity") == "warning"]) * 5

        return max(0, min(100, score))

    # ========== Categorization ==========

    def set_category(self, category: FileCategory) -> None:
        """Set the file category."""
        self._category = category

    def get_category(self) -> FileCategory:
        """Get the file category."""
        return self._category

    def auto_categorize(self) -> FileCategory:
        """Automatically categorize based on file analysis."""
        if not self.source_path:
            return FileCategory.OTHER

        name = self.source_path.name.lower()
        ext = self.source_path.suffix.lower()

        # Test files
        if "test" in name or name.startswith("test_"):
            self._category = FileCategory.TEST
        # Configuration files
        elif ext in [".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"]:
            self._category = FileCategory.CONFIGURATION
        # Build files
        elif name in ["makefile", "dockerfile", "cmakelists.txt"] or ext in [".mk"]:
            self._category = FileCategory.BUILD
        # Documentation
        elif ext in [".md", ".rst", ".txt"]:
            self._category = FileCategory.DOCUMENTATION
        # Data files
        elif ext in [".csv", ".xml", ".sql"]:
            self._category = FileCategory.DATA
        # Code files
        elif ext in [".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c"]:
            self._category = FileCategory.CODE
        else:
            self._category = FileCategory.OTHER

        return self._category

    # ========== Metadata ==========

    def set_metadata(self, key: str, value: Any) -> None:
        """Set a metadata value."""
        self._metadata[key] = value

    def get_metadata(self, key: str) -> Optional[Any]:
        """Get a metadata value."""
        return self._metadata.get(key)

    def get_all_metadata(self) -> Dict[str, Any]:
        """Get all metadata."""
        return dict(self._metadata)

    def export_metadata(self) -> str:
        """Export metadata as JSON."""
        data: Dict[str, Any] = {
            "priority": self._priority.value,
            "category": self._category.value,
            "tags": [t.name for t in self._tags.values()],
            "versions": len(self._versions),
            "annotations": len(self._annotations),
            "custom": self._metadata
        }
        return json.dumps(data, indent=2)

    # ========== Core Methods ==========
    def _get_default_content(self) -> str:
        """Return rich, structured template for new descriptions."""
        self.file_path.name.replace('.description.md', '')
        return """# Description: `{filename}`

## Purpose
[One - line purpose statement]

## Key Features
- [Feature 1]
- [Feature 2]

## Usage
```bash
# Example usage
```
"""

    def _get_fallback_response(self) -> str:
        """Return fallback response when Copilot is unavailable."""
        return ("# AI Improvement Unavailable\n"
                "# GitHub CLI not found. Install from https://cli.github.com/\n\n"
                "# Original content preserved below:\n\n")

    def improve_content(self, prompt: str) -> str:
        """Use AI to improve the context.

        When Copilot CLI is unavailable, BaseAgent keeps the existing file
        content unchanged instead of injecting duplicated placeholder blocks.
        """
        logging.info(f"Improving context for {self.file_path}")
        # Include source code in AI context for accurate descriptions
        if self.source_path and self.source_path.exists():
            logging.debug(f"Using source file: {self.source_path}")
            try:
                # Limit source code to 8000 chars to avoid token limits
                source_code = self.source_path.read_text(encoding='utf-8')[:8000]
                enhanced_prompt = (
                    f"{prompt}\n\n"
                    f"Source code to analyze ({self.source_path.name}):\n"
                    f"```\n{source_code}\n```\n\n"
                    "Based on the source code above, provide a comprehensive description."
                )
                return super().improve_content(enhanced_prompt)
            except (OSError, UnicodeDecodeError):
                pass

        return super().improve_content(prompt)
