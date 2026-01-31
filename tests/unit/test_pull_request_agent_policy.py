#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from src.logic.agents.development.pull_request_agent import PullRequestAgent


def test_create_patch_branch_respects_policy(monkeypatch, tmp_path):
    agent = PullRequestAgent(str(tmp_path))
    # Ensure config does not permit branch creation by default
    agent._config = {}

    res = agent.create_patch_branch("test-branch")
    assert "Branch creation is disabled by policy" in res

    # Enable branch creation and simulate git failure (no git in tmp dir)
    agent._config = {"allow_branch_creation": True}
    res2 = agent.create_patch_branch("test-branch")
    # Branch creation should be attempted when allowed; either a success message or an error may be returned
    assert ("Successfully created" in res2) or ("Error creating branch" in res2)

    # Cleanup if branch was created during the test run
    if "Successfully created" in res2:
        import subprocess
        try:
            subprocess.check_output(["git", "checkout", "main"], text=True)
            subprocess.check_output(["git", "branch", "-D", "test-branch"], text=True)
        except Exception:
            pass
