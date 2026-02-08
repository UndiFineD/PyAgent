# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_owl.py\owl.py\camel.py\toolkits.py\base_a7dd6d151fc3.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-owl\owl\camel\toolkits\base.py

# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========

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

# ========= Copyright 2023-2024 @ CAMEL-AI.org. All Rights Reserved. =========

from typing import List

from camel.toolkits import FunctionTool

from camel.utils import AgentOpsMeta


class BaseToolkit(metaclass=AgentOpsMeta):
    r"""Base class for toolkits."""

    def get_tools(self) -> List[FunctionTool]:
        r"""Returns a list of FunctionTool objects representing the

        functions in the toolkit.

        Returns:

            List[FunctionTool]: A list of FunctionTool objects

                representing the functions in the toolkit.

        """

        raise NotImplementedError("Subclasses must implement this method.")
