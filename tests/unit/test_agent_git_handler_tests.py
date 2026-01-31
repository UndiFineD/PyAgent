#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import subprocess
import types
import pytest

from src.core.base.common.utils.agent_git_handler import AgentGitHandler


class DummyShell:
    def __init__(self):
        # Simulate a small repo state
        self.commands = []

    def execute(self, cmd, check=False):
        self.commands.append(cmd)
        cmdstr = " ".join(cmd)
        # Simulate pytest call
        if "pytest" in cmdstr:
            class Res:
                stdout = ""
            res = Res()
            res.stdout = ""  # empty -> failure simulation
            return res
        if cmd[:2] == ["git", "status"]:
            class Res:
                stdout = " M file.py\n"
            res = Res()
            return res
        if cmd[:2] == ["git", "commit"]:
            class Res:
                stdout = "Committed"
            return Res()
        if cmd[:2] == ["git", "add"]:
            return types.SimpleNamespace(stdout="")
        if cmd[:2] == ["git", "reset"]:
            return types.SimpleNamespace(stdout="")
        return types.SimpleNamespace(stdout="")


def test_commit_aborts_when_tests_fail(monkeypatch, tmp_path):
    handler = AgentGitHandler(tmp_path, no_git=False)
    handler.shell = DummyShell()

    # Simulate files and enforce tests
    ok = handler.commit_changes("msg", files=["file.py"], enforce_tests=True)
    assert ok is False


def test_commit_succeeds_when_no_enforce(monkeypatch, tmp_path):
    handler = AgentGitHandler(tmp_path, no_git=False)
    handler.shell = DummyShell()

    ok = handler.commit_changes("msg", files=["file.py"], enforce_tests=False)
    assert ok is True
