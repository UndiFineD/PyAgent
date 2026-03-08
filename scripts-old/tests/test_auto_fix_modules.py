#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

from auto_fix import RuleEngine, TransactionManager, AutoFixLogger


def test_imports_exist():
    # basic sanity checks that components can be instantiated
    engine = RuleEngine([])
    assert engine.rules == []

    txn = TransactionManager()
    assert txn.repo_root is not None

    logger = AutoFixLogger()
    assert logger.changes == []
