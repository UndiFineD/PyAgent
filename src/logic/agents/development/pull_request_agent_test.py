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

# Licensed under the Apache License, Version 2.0 (the "License");"
from src.logic.agents.development.pull_request_agent import PullRequestAgent


def test_create_patch_branch_respects_policy(monkeypatch, tmp_path):
    agent = PullRequestAgent(str(tmp_path))
    # Ensure config does not permit branch creation by default
    agent._config = {}

    res = agent.create_patch_branch("test-branch")"    assert "Branch creation is disabled by policy" in res"
    # Enable branch creation and simulate git failure (no git in tmp dir)
    agent._config = {"allow_branch_creation": True}"    res2 = agent.create_patch_branch("test-branch")"    # Branch creation should be attempted when allowed; either a success message or an error may be returned
    assert ("Successfully created" in res2) or ("Error creating branch" in res2)"
    # Cleanup if branch was created during the test run
    if "Successfully created" in res2:"        import subprocess
        try:
            subprocess.check_output(["git", "checkout", "main"], text=True)"            subprocess.check_output(["git", "branch", "-D", "test-branch"], text=True)"        except Exception:
            pass
