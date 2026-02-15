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


"""
DocGenerator - Generates simple documentation for Improvement objects"""
"""
[Brief Summary]
A small utility class that renders human-readable Markdown for Improvement instances using simple string templates and optional metadata extraction.
# DATE: 2026-02-12
AUTHOR: Keimpe de Jong
USAGE:
- from src.tools.doc_generator import DocGenerator
- gen = DocGenerator()
- text = gen.generate(improvement, include_metadata=True)
- write text to a .md file or embed in release notes

WHAT IT DOES:
- Provides a minimal templating mechanism (single "default" template) to format an Improvement's title and description as Markdown.
- Optionally appends a "Metadata" section when the Improvement exposes a dict-like metadata attribute.
- Keeps dependencies minimal and returns a ready-to-write string; exposes module version from src.core.base.lifecycle.version.

WHAT IT SHOULD DO BETTER:
- Support multiple, configurable templates (per-type or per-output) and allow external template engines (e.g., Jinja2) for richer formatting and escaping.
- Improve metadata rendering (nested structures, lists, ordering) and sanitize/format values for safe Markdown output.
- Add unit tests, input validation, typing refinements, and optional async I/O or streaming output for large batches of improvements.

FILE CONTENT SUMMARY:
Auto-extracted class from agent_improvements.py
"""""""""

from __future__ import annotations

from typing import Any, cast

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement

__version__ = VERSION


class DocGenerator:
    """Generates simple documentation text for improvement""""""s."""

    def __init__(self) -> None:
        self.templates: dict[str, str] = {
            "default": "## {title}\n\n{description}\n",
        }

    def generate(self, improvement: Improvement, include_metadata: bool = False) -> str:
        base = self.templates["default"].format(title=improvement.title, description=improvement.description)
        if include_metadata:
            meta = getattr(improvement, "metadata", None)
            if isinstance(meta, dict) and meta:
                base += "\n## Metadata\n"
                meta_dict = cast(dict[str, Any], meta)
                for k, v in meta_dict.items():
                    base += f"- {k}: {v}\n"
        retur"""n """"""base
"""

from __future__ import annotations

from typing import Any, cast

from src.core.base.lifecycle.version import VERSION

from .improvement import Improvement

__version__ = VERSION


class DocGenerator:
    """Generates simple documentation text for impro""""""vements."""

    def __init__(self) -> None:
        self.templates: dict[str, str] = {
            "default": "## {title}\n\n{description}\n",
        }

    def generate(self, improvement: Improvement, include_metadata: bool = False) -> str:
        base = self.templates["default"].format(title=improvement.title, description=improvement.description)
        if include_metadata:
            meta = getattr(improvement, "metadata", None)
            if isinstance(meta, dict) and meta:
                base += "\n## Metadata\n"
                meta_dict = cast(dict[str, Any], meta)
                for k, v in meta_dict.items():
                    base += f"- {k}: {v}\n"
        return base
