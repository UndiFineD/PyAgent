# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\aenvironment.py\aenv.py\src.py\cli.py\tests.py\test_cmds_2cdf3dc6e66a.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\AEnvironment\aenv\src\cli\tests\test_cmds.py

# Copyright 2025.

#

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

from cli.cmds import push

from click.testing import CliRunner


class TestCmds:
    def test_push(self):

        runner = CliRunner()

        result = runner.invoke(
            push,
            [
                "--work-dir",
                "/AEnvironment/aenv/examples/mini-swe-env",
            ],
        )

        assert result.exit_code == 0
