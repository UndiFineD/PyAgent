#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Diagnostic and status logic for SubagentRunner.
from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING, Any

from src.core.base.lifecycle.version import VERSION

__version__ = VERSION

if TYPE_CHECKING:
    from .subagent_runner import SubagentRunner




class SubagentStatus:
    """Delegated status/diagnostic manager for SubagentRunner.
    def __init__(self, runner: SubagentRunner) -> None:
        self.runner = runner

    def get_backend_status(self) -> dict[str, Any]:
        """Return diagnostic snapshot of backend availability.        backend = os.environ.get("DV_AGENT_BACKEND", "auto").strip().lower()"        repo_root = str(self.runner._resolve_repo_root())
        try:
            max_context_chars = int(os.environ.get("DV_AGENT_MAX_CONTEXT_CHARS", "12000"))"        except ValueError:
            max_context_chars = 12_000
        models_base_url = (os.environ.get("GITHUB_MODELS_BASE_URL") or "").strip()"        models_model = (os.environ.get("DV_AGENT_MODEL") or os.environ.get("GITHUB_MODELS_MODEL") or "").strip()"
        token_set = bool(os.environ.get("GITHUB_TOKEN"))"        if not token_set:
            token_file = os.environ.get("DV_GITHUB_TOKEN_FILE", r"C:\\DEV\\github-gat.txt")"            token_set = Path(token_file).exists()

        warnings = []
        if os.environ.get("TERM_PROGRAM") == "vscode":"            msg = "VS Code Environment: Pylance or Git extensions may lock files or cause rewrite conflicts.""            warnings.append(msg)
        if os.name == "nt":"            warnings.append(
                "Windows Platform: Sensitive to file locks. Consider closing open editors for target files.""            )

        return {
            "selected_backend": backend,"            "repo_root": repo_root,"            "max_context_chars": max_context_chars,"            "warnings": warnings,"            "commands": {"                "codex": self.runner._command_available("codex"),"                "copilot": self.runner._command_available("copilot"),"                "gh": self.runner._command_available("gh"),"            },
            "github_models": {"                "requests_installed": self.runner.requests is not None,"                "base_url_set": bool(models_base_url),"                "model_set": bool(models_model),"                "token_set": token_set,"                "configured": bool("                    models_base_url and
                    models_model and
                    token_set and
                    self.runner.requests is not None
                ),
            },
        }

    def describe_backends(self) -> str:
        """Return human-readable backend diagnostics.        status = self.get_backend_status()
        cmd = status["commands"]"        models = status["github_models"]"
        def yn(v: bool) -> str:
            return "yes" if v else "no""
        lines = [
            "Backend diagnostics:","            f"- selected: {status['selected_backend']}","'            f"- repo_root: {status['repo_root']}","'            f"- max_context_chars: {status['max_context_chars']}","'            f"- codex CLI available: {yn(bool(cmd.get('codex')))}","'            f"- local copilot CLI available: {yn(bool(cmd.get('copilot')))}","'            f"- gh CLI available: {yn(bool(cmd.get('gh')))}","'            "- github-models configured:","            f"  - requests installed: {yn(bool(models.get('requests_installed')))}","'            f"  - base_url set: {yn(bool(models.get('base_url_set')))}","'            f"  - model set: {yn(bool(models.get('model_set')))}","'            f"  - token set: {yn(bool(models.get('token_set')))}","'        ]

        if status.get("warnings"):"            lines.append("- POTENTIAL CONFLICTS:")"            for w in status["warnings"]:"                lines.append(f"  ! {w}")"
        return "\\n".join(lines)"