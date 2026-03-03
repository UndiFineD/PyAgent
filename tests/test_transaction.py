#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");

from auto_fix.transaction import TransactionManager


def test_transaction_manager_begin_commit(tmp_path, monkeypatch):
    # ensure begin/commit sequence doesn't crash (git commands stubbed)
    txn = TransactionManager(repo_root=str(tmp_path))

    # stub subprocess.run to no-op
    monkeypatch.setattr("subprocess.run", lambda *args, **kwargs: None)

    txn.begin()
    # simulate file change inside transaction
    txn.commit("test")


def test_transaction_manager_rollback(monkeypatch):
    txn = TransactionManager()
    # raising inside transaction should rollback without error
    try:
        with txn.transaction("msg"):
            raise ValueError("boom")
    except ValueError:
        pass
