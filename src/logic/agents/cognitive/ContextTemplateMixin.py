#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from __future__ import annotations
import logging
from src.logic.agents.cognitive.context.models.ContextTemplate import ContextTemplate

# Default templates for common file types
DEFAULT_TEMPLATES: dict[str, ContextTemplate] = {
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
        required_fields=["Purpose"],
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
        required_fields=["Purpose"],
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
        required_fields=["Purpose", "Usage"],
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
        required_fields=["Purpose"],
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
        required_fields=["Purpose", "Test Cases"],
    ),
}


class ContextTemplateMixin:
    """Template management methods for ContextAgent."""

    def set_template(self, template_name: str) -> bool:
        """Set the active template by name."""
        if hasattr(self, "_templates") and template_name.lower() in self._templates:
            logging.info(f"Using template: {template_name}")
            return True
        logging.warning(f"Template '{template_name}' not found")
        return False

    def get_template_by_name(self, template_name: str) -> ContextTemplate | None:
        """Get a template by name."""
        return getattr(self, "_templates", {}).get(template_name.lower())

    def get_template(self, template_name: str) -> ContextTemplate | None:
        """Compatibility alias: get a template by name."""
        return getattr(self, "_templates", {}).get(template_name.lower())

    def add_template(self, template: ContextTemplate) -> None:
        """Add a custom template."""
        if not hasattr(self, "_templates"):
            self._templates = dict(DEFAULT_TEMPLATES)
        self._templates[template.name.lower()] = template
        logging.info(f"Added template: {template.name}")

    def get_template_for_file(self) -> ContextTemplate | None:
        """Get the appropriate template for the current file."""
        source_path = getattr(self, "source_path", None)
        if not source_path:
            return None

        ext = source_path.suffix.lower()
        name = source_path.name.lower()

        templates = getattr(self, "_templates", DEFAULT_TEMPLATES)

        # Check test files first
        if "test" in name or name.startswith("test_"):
            return templates.get("test")

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
        return templates.get(template_name) if template_name else None

    def apply_template(self, template_name: str | None = None) -> str:
        """Apply a template to generate initial content."""
        template = None
        templates = getattr(self, "_templates", DEFAULT_TEMPLATES)
        if template_name:
            template = templates.get(template_name.lower())
        else:
            template = self.get_template_for_file()

        if not template:
            return getattr(self, "_get_default_content", lambda: "")()

        filename = self.file_path.name.replace(".description.md", "")
        return template.template_content.format(filename=filename)
