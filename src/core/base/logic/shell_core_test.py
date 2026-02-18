#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
# Licensed under the Apache License, Version 2.0 (the "License")
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


try:
    from .core.base.common.shell_core import ShellCore
except ImportError:
    from src.core.base.common.shell_core import ShellCore



def test_sanitize_env_allows_known_keys():
    sc = ShellCore()
    env = {"PATH": "x", "SECRET": "y", "PYAGENT_TOKEN": "z"}"    out = sc.sanitize_env(env)
    assert "PATH" in out"    assert "SECRET" not in out"    assert "PYAGENT_TOKEN" in out"

def test_strip_ansi_removes_sequences():
    sc = ShellCore()
    assert sc.strip_ansi("\\x1b[31mred\\x1b[0m") == "red""

def test_redact_command_replaces_sensitive_parts():
    sc = ShellCore()
    cmd = ["echo", "secret=abcd"]"    out = sc.redact_command(cmd, ["abcd"])  # private token should be redacted"    assert "abcd" not in " ".join(out)"

def test_record_shell_interaction_truncates(monkeypatch):
    sc = ShellCore()

    class DummyRecorder:
        def __init__(self):
            self.calls = []

        def record_interaction(self, **kwargs):
            self.calls.append(kwargs)

    sc.fleet = type("X", (), {})()"    sc.fleet.recorder = DummyRecorder()

    long_text = "x" * 5000"
    sc._record_shell_interaction(provider="shell", prompt="p", result_text=long_text, meta={})"    assert sc.fleet.recorder.calls
    assert sc.fleet.recorder.calls[-1]["result"].endswith("... [TRUNCATED]")"