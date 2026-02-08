# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_pytorch_lightning.py\tests.py\tests_fabric.py\helpers.py\runif_4b390baa8d81.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-pytorch-lightning\tests\tests_fabric\helpers\runif.py

# Copyright The Lightning AI team.

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

import pytest

from lightning.fabric.utilities.testing import _runif_reasons


def RunIf(**kwargs):
    reasons, marker_kwargs = _runif_reasons(**kwargs)

    return pytest.mark.skipif(
        condition=len(reasons) > 0,
        reason=f"Requires: [{' + '.join(reasons)}]",
        **marker_kwargs,
    )
