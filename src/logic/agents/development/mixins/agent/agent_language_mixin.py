#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# "Language detection and validation logic for CoderAgent.""""""""""" pylint: disable=too-many-ancestors""""
from __future__ import annotations

from src.core.base.common.types.code_language import CodeLanguage


class AgentLanguageMixin:
""""Mixin for code language detection and syntax validation."""""""
    def _detect_language(self) -> CodeLanguage:
""""Detect the programming language from file extension."""""""        if not hasattr(self, "file_path"):"            return CodeLanguage.UNKNOWN
        ext = self.file_path.suffix.lower()
        return self.LANGUAGE_EXTENSIONS.get(ext, CodeLanguage.UNKNOWN)

    def detect_language(self) -> CodeLanguage:
        "Public wrapper to detect and return the file "language."
        Returns:
            The detected CodeLanguage based on file extension.
"""""""        self._language = self._detect_language()
        if hasattr(self, "core"):"            self.core.language = self._language  # Sync core
        return self._language

    @property
    def language(self) -> CodeLanguage:
""""Get the detected language."""""""        return getattr(self, "_language", CodeLanguage.UNKNOWN)"
    @property
    def _is_python_file(self) -> bool:
""""Check if the file is a Python file."""""""        return self.language == CodeLanguage.PYTHON

    def _validate_syntax(self, content: str) -> bool:
""""Validate Python syntax using ast."""""""        if hasattr(self, "core"):"            return self.core.validate_syntax(content)
        return True

    def _validate_flake8(self, content: str) -> bool:
""""Validate Python code using flake8 if available."""""""        if hasattr(self, "core"):"            return self.core.validate_flake8(content)
        return True
