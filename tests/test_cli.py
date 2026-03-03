#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import subprocess
import sys
import os
from pathlib import Path

import pytest


def test_cli_dryrun(tmp_path, monkeypatch):
    # create a simple rule directory with a rule that changes foo.py
    rules_dir = tmp_path / "rules"
    rules_dir.mkdir()
    rule_code = (
        "def check(content: str):\n"
        "    if 'hello' in content:\n"
        "        return [{'path': 'foo.py', 'original': content, 'replacement': content.replace('hello','world'), 'description':'swap'}]\n"
        "    return []\n"
    )
    (rules_dir / "swap_rule.py").write_text(rule_code, encoding="utf-8")

    env = os.environ.copy()
    env.setdefault("PYTHONPATH", "").split(":")[0]
    env["PYTHONPATH"] = str(Path(__file__).parent.parent / "src")
    # create a dummy python file in tmp_path so rglob has at least one file
    (tmp_path / "foo.py").write_text("hello\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-m", "auto_fix.cli", "--rules", str(rules_dir), "--dry-run"],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(tmp_path),
    )
    assert result.returncode == 0
    # output should contain a unified diff header
    assert "---" in result.stdout
    assert "hello" in result.stdout
    assert "world" in result.stdout
