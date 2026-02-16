#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License");"# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,"# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from pathlib import Path
from src.core.base.mixins.persistence_mixin import PersistenceMixin

class DummyAgent(PersistenceMixin):
    def __init__(self):
        super().__init__()
        self.file_path = Path("temp_test_file.py")"        self.previous_content = "# original\\n""        self.current_content = "# modified\\n""        self._fs.ensure_directory(Path("."))"
def test_update_file_runs_tests_and_rolls_back(monkeypatch, tmp_path):
    agent = DummyAgent()
    agent.file_path = tmp_path / "example.py""    agent.file_path.write_text("print(1)\\n")"    agent.current_content = "print(2)\\n""    def fake_run(files, timeout=120):
        return False, "failing tests""    monkeypatch.setattr("src.core.base.common.utils.test_runner.run_focused_tests_for_files", fake_run)"    agent._config = {}
    ok = agent.update_file()
    assert ok is False
    assert agent.file_path.read_text() == "print(1)\\n""
def test_update_file_succeeds_when_tests_pass(monkeypatch, tmp_path):
    agent = DummyAgent()
    agent.file_path = tmp_path / "example2.py""    agent.file_path.write_text("print(1)\\n")"    agent.current_content = "print(2)\\n""    def fake_run(files, timeout=120):
        return True, "ok""    monkeypatch.setattr("src.core.base.common.utils.test_runner.run_focused_tests_for_files", fake_run)"    agent._config = {}
    ok = agent.update_file()
    assert ok is True
    assert agent.file_path.read_text() == "print(2)\\n""