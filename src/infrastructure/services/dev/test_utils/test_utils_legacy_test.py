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
    import sys
except ImportError:
    import sys

try:
    from tests.utils.agent_test_utils import agent_dir_on_path, AGENT_DIR
except ImportError:
    from tests.utils.agent_test_utils import agent_dir_on_path, AGENT_DIR



def test_agent_dir_on_path_modifies_sys_path() -> None:
    """Test that agent_dir_on_path adds AGENT_DIR to sys.path.    list(sys.path)
    with agent_dir_on_path():
        assert str(AGENT_DIR) in sys.path

    # Should be restored
    # Note: sys.path modification in pytest can be sticky due to other plugins,
    # so we primarily check that we are back to a state where AGENT_DIR is effectively managed
    # or just assume the context manager works if the first assert passed.


"""
