#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

import os
import subprocess
import sys
from pathlib import Path


def test_apply_creates_commit(tmp_path):
    """This is a high-level integration test that verifies the CLI can apply a simple rule and create a git commit."""
    # setup a mini repo
    subprocess.run(["git", "init"], cwd=tmp_path, check=True)
    file_path = tmp_path / "foo.py"
    file_path.write_text("print('hello')\n", encoding="utf-8")
    subprocess.run(["git", "add", "foo.py"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=tmp_path, check=True)
    subprocess.run(["git", "config", "user.name", "Tester"], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "initial"], cwd=tmp_path, check=True)

    # create a simple rule that replaces hello with world
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
    env["PYTHONPATH"] = str(Path(__file__).parent.parent / "src")
    # run CLI apply
    result = subprocess.run(
        [sys.executable, "-m", "auto_fix.cli", "--rules", str(rules_dir), "--apply"],
        cwd=str(tmp_path),
        capture_output=True,
        text=True,
        env=env,
    )
    assert result.returncode == 0, result.stderr

    # file should be updated
    content = file_path.read_text(encoding="utf-8")
    assert "world" in content

    # git log should contain commit message
    log = subprocess.run(["git", "log", "--oneline"], cwd=tmp_path, capture_output=True, text=True)
    assert "auto fix" in log.stdout
