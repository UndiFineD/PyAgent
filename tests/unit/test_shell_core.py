#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0

from src.core.base.common.shell_core import ShellCore, ShellResult


def test_sanitize_env_allows_known_keys():
    sc = ShellCore()
    env = {"PATH": "x", "SECRET": "y", "PYAGENT_TOKEN": "z"}
    out = sc.sanitize_env(env)
    assert "PATH" in out
    assert "SECRET" not in out
    assert "PYAGENT_TOKEN" in out


def test_strip_ansi_removes_sequences():
    sc = ShellCore()
    assert sc.strip_ansi("\x1b[31mred\x1b[0m") == "red"


def test_redact_command_replaces_sensitive_parts():
    sc = ShellCore()
    cmd = ["echo", "secret=abcd"]
    out = sc.redact_command(cmd, ["abcd"])  # private token should be redacted
    assert "abcd" not in " ".join(out)


def test_record_shell_interaction_truncates(monkeypatch):
    sc = ShellCore()

    class DummyRecorder:
        def __init__(self):
            self.calls = []

        def record_interaction(self, **kwargs):
            self.calls.append(kwargs)

    sc.fleet = type("X", (), {})()
    sc.fleet.recorder = DummyRecorder()

    long_text = "x" * 5000

    sc._record_shell_interaction(provider="shell", prompt="p", result_text=long_text, meta={})
    assert sc.fleet.recorder.calls
    assert sc.fleet.recorder.calls[-1]["result"].endswith("... [TRUNCATED]")
