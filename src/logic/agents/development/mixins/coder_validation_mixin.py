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
Syntax validation and linting logic for CoderCore.
"""

# pylint: disable=too-many-ancestors

from __future__ import annotations

import ast
import logging
import os
import shutil
import subprocess
import tempfile

from src.core.base.common.types.code_language import CodeLanguage


class CoderValidationMixin:
    """Mixin for validating syntax and linting code."""

    def validate_syntax(self, content: str) -> bool:
        """Validate Python syntax using ast."""
        if self.language != CodeLanguage.PYTHON:
            return True
        try:
            ast.parse(content)
            return True
        except (SyntaxError, RecursionError, MemoryError) as e:
            logging.error(f"Syntax error in generated code: {e}")
            return False

    def validate_flake8(self, content: str) -> bool:
        """Validate Python code using flake8 if available."""
        if self.language != CodeLanguage.PYTHON:
            return True
        if not shutil.which("flake8"):
            logging.warning("flake8 not found, skipping style validation")
            return True
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name
        try:
            # Run flake8 on the temporary file
            command = ["flake8", "--ignore=E501,F401,W291,W293", tmp_path]
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False,
            )

            if hasattr(self, "recorder") and self.recorder:
                output = result.stdout or result.stderr
                self.recorder.record_interaction(
                    provider="python",
                    model="flake8",
                    prompt=" ".join(command),
                    result=output[:2000],
                )

            return result.returncode == 0
        except Exception as e:  # pylint: disable=broad-exception-caught, unused-variable
            logging.error(f"flake8 validation failed: {e}")
            return True
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
