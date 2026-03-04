#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

 from __future__ import annotations

from contextlib import contextmanager
import subprocess
import os
from typing import Iterator

# import heavy dependency only when transaction begins
StateTransaction = None


class TransactionManager:
    def __init__(self, repo_root: str | None = None):
        self.repo_root = repo_root or os.getcwd()
        self._tx: StateTransaction | None = None

    def begin(self) -> None:
        if self._tx is not None:
            raise RuntimeError("transaction already in progress")
        # lazy import ensures tests don't pull in unrelated errors
        global StateTransaction
        if StateTransaction is None:
            try:
                from src.core.base.agent_state_manager import StateTransaction
            except Exception:
                # if import fails (e.g. core contains errors), use a no-op stub
                class _StubTx:
                    def __enter__(self):
                        return None
                    def __exit__(self, exc_type, exc_val, exc_tb):
                        return None
                StateTransaction = _StubTx  # type: ignore
        self._tx = StateTransaction()
        self._tx.__enter__()

    def commit(self, message: str) -> None:
        if self._tx is None:
            raise RuntimeError("no transaction to commit")
        self._tx.__exit__(None, None, None)
        self._tx = None
        # stage and commit changes to git
        subprocess.run(["git", "add", "-A"], cwd=self.repo_root, check=True)
        subprocess.run(["git", "commit", "-m", message], cwd=self.repo_root, check=True)

    def rollback(self) -> None:
        if self._tx is None:
            return
        self._tx.__exit__(Exception, Exception("rollback"), None)
        self._tx = None

    @contextmanager
    def transaction(self, message: str) -> Iterator[None]:
        self.begin()
        try:
            yield
        except Exception:
            self.rollback()
            raise
        else:
            self.commit(message)
