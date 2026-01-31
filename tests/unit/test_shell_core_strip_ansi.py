#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from src.core.base.common.shell_core import ShellCore


def test_strip_ansi_handles_none_and_empty():
    sc = ShellCore()
    assert sc.strip_ansi(None) == ""
    assert sc.strip_ansi("") == ""
    assert sc.strip_ansi("\x1b[31mred\x1b[0m") == "red"
