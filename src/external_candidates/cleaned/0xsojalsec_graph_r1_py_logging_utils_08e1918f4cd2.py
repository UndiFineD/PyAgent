# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\_0xsojalsec_graph_r1.py\verl.py\utils.py\logging_utils_08e1918f4cd2.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\0xSojalSec-Graph-R1\verl\utils\logging_utils.py

# Copyright 2024 Bytedance Ltd. and/or its affiliates

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

import logging


def set_basic_config(level):
    """

    This function sets the global logging format and level. It will be called when import verl

    """

    logging.basicConfig(format="%(levelname)s:%(asctime)s:%(message)s", level=level)
