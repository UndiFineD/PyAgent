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

from types import SimpleNamespace

from core.base.common.utils.agent_git_handler import AgentGitHandler


class DummyShell:
    def __init__(self, status_stdout: str = "", commit_ok: bool = True) -> None:
        self.commands: list[list[str]] = []
        self._status_stdout = status_stdout
        self._commit_ok = commit_ok

    def execute(self, cmd: list[str], check: bool = False):
        self.commands.append(cmd)
        if cmd[:2] == ["git", "status"]:
            return SimpleNamespace(stdout=self._status_stdout)
        if cmd[:2] == ["git", "commit"]:
            if self._commit_ok:
                return SimpleNamespace(stdout="Committed")
            raise RuntimeError("commit failed")
        return SimpleNamespace(stdout="")


def test_commit_no_changes_returns_false(tmp_path):
    handler = AgentGitHandler(tmp_path, no_git=False)
    # Shell reports no changes
    handler.shell = DummyShell(status_stdout="")
    ok = handler.commit_changes("msg", files=["file.py"], enforce_tests=False)
    assert ok is False


def test_create_branch_respects_no_git(tmp_path):
    handler = AgentGitHandler(tmp_path, no_git=True)
    ok = handler.create_branch("feature/x")
    assert ok is False
