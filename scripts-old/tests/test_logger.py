#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from auto_fix.logger import AutoFixLogger, PlannedChange


def test_logger_records():
    l = AutoFixLogger()
    change = PlannedChange(path="foo.py", description="fix", diff="-a +b")
    l.record(change)
    assert l.changes == [change]


def test_logger_report():
    l = AutoFixLogger()
    l.record(PlannedChange(path="foo.py", description="fix", diff="difftext"))
    out = l.report()
    assert "foo.py" in out and "difftext" in out
