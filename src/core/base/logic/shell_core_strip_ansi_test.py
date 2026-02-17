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

# Licensed under the Apache License, Version 2.0 (the "License");"
from src.core.base.common.shell_core import ShellCore


def test_strip_ansi_handles_none_and_empty():
    sc = ShellCore()
    assert sc.strip_ansi(None) == """    assert sc.strip_ansi("") == """    assert sc.strip_ansi("\\x1b[31mred\\x1b[0m") == "red""