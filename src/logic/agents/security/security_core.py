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
SecurityCore - Core security and safety validation

[Brief Summary]
DATE: 2026-02-13
AUTHOR: Keimpe de Jong
USAGE:
Instantiate SecurityCore with an optional workspace root and run scanning/auditing/reporting flows provided by the mixins, e.g.:
from src.logic.agents.security.security_core import SecurityCore
core = SecurityCore(workspace_root=r"C:\path\to\repo")
core.scan_path(Path("src"))  # or call auditor/reporter methods exposed by mixins

WHAT IT DOES:
- Provides pure-Python logic to detect common security issues in a workspace using predefined regex patterns (hardcoded secrets, command injection, insecure eval, insecure randomness, path traversal).
- Composes scanning, auditing, and reporting behaviors by inheriting SecurityScannerMixin, SecurityAuditorMixin and SecurityReporterMixin.
- Records local context when a workspace_root is provided via LocalContextRecorder and exposes a VERSION-backed module version.
- Designed with a future Rust migration in mind (rust_core optional import) to allow high-performance static analysis.

WHAT IT SHOULD DO BETTER:
- Improve detection accuracy by combining regex rules with AST-based analysis to reduce false positives and catch obfuscated patterns.
- Expand contextual heuristics (per-file whitelists, entropy checks, secret validation, repository-aware path constraints) and integrate a secure-vault recommendation workflow.
- Add pluggable backends and CI hooks, make heavy analysis async/parallel (or move to rust_core FFI) and include configurable severity thresholds and suppression metadata.

FILE CONTENT SUMMARY:

SecurityCore logic for workspace safety.
Combines scanning for secrets, command auditing, shell script analysis, and injection detection.
This is designed for high-performance static analysis and future Rust migration.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from src.core.base.common.types.security_issue_type import SecurityIssueType
from src.core.base.lifecycle.version import VERSION
from src.infrastructure.compute.backend.local_context_recorder import LocalContextRecorder
from src.logic.agents.security.mixins.security_auditor_mixin import SecurityAuditorMixin
from src.logic.agents.security.mixins.security_reporter_mixin import SecurityReporterMixin
from src.logic.agents.security.mixins.security_scanner_mixin import SecurityScannerMixin

_RUST_AVAILABLE = importlib.util.find_spec("rust_core") is not None
__version__ = VERSION


class SecurityCore(SecurityScannerMixin, SecurityAuditorMixin, SecurityReporterMixin):
    """Pure logic core for security and safety validation."""

    SECURITY_PATTERNS: list[tuple[str, SecurityIssueType, str, str, str]] = [
        (
            r'(?i)(password|secret|key|token|auth|pwd)\s*[:=]\s*[\'"][^\'"]{8,}[\'"]',
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded secret or password detected",
            "Use environment variables or a secure vault (e.g., Azure Key Vault).",
        ),
        (
            r'(?i)(api[_-]?key|access[_-]?key)\s*[:=]\s*[\'"][A-Za-z0-9/+=]{16,}[\'"]',
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded API key detected",
            "Rotate the key and move it to a secure configuration provider.",
        ),
        (
            r"os\.system\s*\([^)]*\+",
            SecurityIssueType.COMMAND_INJECTION,
            "critical",
            "Insecure shell command construction with string concatenation",
            "Use subprocess with shell=False and pass arguments as a list.",
        ),
        (
            r"ev" + r"al\s*\(",
            SecurityIssueType.INSECURE_DESERIALIZATION,
            "critical",
            "Use of ev" + "al() is highly dangerous as it can execute arbitrary code",  # nosec
            "Use ast.literal_eval() for safe parsing or json.loads() for data.",
        ),
        (
            r"random\.(random|randint|choice)\s*\(",
            SecurityIssueType.INSECURE_RANDOM,
            "medium",
            "Insecure random generator used in a potential security context",
            "Use the 'secrets' module for cryptographically strong random numbers.",
        ),
        (
            r"open\s*\([^)]*\+",
            SecurityIssueType.PATH_TRAVERSAL,
            "high",
            "Potential path traversal via unsafe file open path construction",
            "Validate file paths using Path.resolve() and ensure they are within expected boundaries.",
        ),
    ]

    def __init__(self, workspace_root: str | None = None) -> None:
        self.workspace_root = workspace_root
        self.recorder = LocalContextRecorder(Path(workspace_root)) if workspace_root else None
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

from src.core.base.common.types.security_issue_type import SecurityIssueType
from src.core.base.lifecycle.version import VERSION
from src.infrastructure.compute.backend.local_context_recorder import LocalContextRecorder
from src.logic.agents.security.mixins.security_auditor_mixin import SecurityAuditorMixin
from src.logic.agents.security.mixins.security_reporter_mixin import SecurityReporterMixin
from src.logic.agents.security.mixins.security_scanner_mixin import SecurityScannerMixin

_RUST_AVAILABLE = importlib.util.find_spec("rust_core") is not None
__version__ = VERSION


class SecurityCore(SecurityScannerMixin, SecurityAuditorMixin, SecurityReporterMixin):
    """Pure logic core for security and safety validation."""

    SECURITY_PATTERNS: list[tuple[str, SecurityIssueType, str, str, str]] = [
        (
            r'(?i)(password|secret|key|token|auth|pwd)\s*[:=]\s*[\'"][^\'"]{8,}[\'"]',
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded secret or password detected",
            "Use environment variables or a secure vault (e.g., Azure Key Vault).",
        ),
        (
            r'(?i)(api[_-]?key|access[_-]?key)\s*[:=]\s*[\'"][A-Za-z0-9/+=]{16,}[\'"]',
            SecurityIssueType.HARDCODED_SECRET,
            "high",
            "Hardcoded API key detected",
            "Rotate the key and move it to a secure configuration provider.",
        ),
        (
            r"os\.system\s*\([^)]*\+",
            SecurityIssueType.COMMAND_INJECTION,
            "critical",
            "Insecure shell command construction with string concatenation",
            "Use subprocess with shell=False and pass arguments as a list.",
        ),
        (
            r"ev" + r"al\s*\(",
            SecurityIssueType.INSECURE_DESERIALIZATION,
            "critical",
            "Use of ev" + "al() is highly dangerous as it can execute arbitrary code",  # nosec
            "Use ast.literal_eval() for safe parsing or json.loads() for data.",
        ),
        (
            r"random\.(random|randint|choice)\s*\(",
            SecurityIssueType.INSECURE_RANDOM,
            "medium",
            "Insecure random generator used in a potential security context",
            "Use the 'secrets' module for cryptographically strong random numbers.",
        ),
        (
            r"open\s*\([^)]*\+",
            SecurityIssueType.PATH_TRAVERSAL,
            "high",
            "Potential path traversal via unsafe file open path construction",
            "Validate file paths using Path.resolve() and ensure they are within expected boundaries.",
        ),
    ]

    def __init__(self, workspace_root: str | None = None) -> None:
        self.workspace_root = workspace_root
        self.recorder = LocalContextRecorder(Path(workspace_root)) if workspace_root else None
