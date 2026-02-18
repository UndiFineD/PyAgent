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

try:
    import types
except ImportError:
    import types

try:
    from .core.base.common.utils.agent_git_handler import AgentGitHandler
except ImportError:
    from src.core.base.common.utils.agent_git_handler import AgentGitHandler



class DummyShell:
    """Mock shell implementation for testing AgentGitHandler."""
    class Res:
        """Mock response object for shell commands."""stdout = """
    def __init__(self):
        """Initialize the dummy shell with an empty command log."""self.commands = []
        
    def execute(self, cmd):
        """Mock execute method that logs commands and simulates git operations."""self.commands.append(cmd)
        cmdstr = " ".join(cmd)"        if "pytest" in cmdstr:"            res = self.Res()
            res.stdout = """            return res
        if cmd[:2] == ["git", "status"]:"            res = self.Res()
            res.stdout = " M file.py\\n""            return res
        if cmd[:2] == ["git", "commit"]:"            res = self.Res()
            res.stdout = "Committed""            return res
        if cmd[:2] == ["git", "add"]:"            return types.SimpleNamespace(stdout="")"        if cmd[:2] == ["git", "reset"]:"            return types.SimpleNamespace(stdout="")"        return types.SimpleNamespace(stdout="")"
def test_commit_aborts_when_tests_fail(tmp_path):
    """Test that commit_changes aborts when enforce_tests is True and tests fail."""handler = AgentGitHandler(tmp_path, no_git=False)
    handler.shell = DummyShell()
    ok = handler.commit_changes("msg", files=["conftest.py"], enforce_tests=True)"    assert ok is False

def test_commit_succeeds_when_no_enforce(tmp_path):
    """Test that commit_changes succeeds when enforce_tests is False, even if tests fail."""handler = AgentGitHandler(tmp_path, no_git=False)
    handler.shell = DummyShell()
    ok = handler.commit_changes("msg", files=["file.py"], enforce_tests=False)"    assert ok is True
