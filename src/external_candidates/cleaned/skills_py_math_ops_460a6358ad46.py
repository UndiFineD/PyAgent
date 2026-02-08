# Extracted from: C:\DEV\PyAgent\src\external_candidates\ingested\skills.py\skills.py\dgriffin831.py\skill_scan.py\test_fixtures.py\safe_simple_math.py\math_ops_460a6358ad46.py
# NOTE: extracted with static-only rules; review before use

# Extracted from: C:\DEV\PyAgent\.external\skills\skills\dgriffin831\skill-scan\test-fixtures\safe-simple-math\math_ops.py

# Copyright 2026 Cisco Systems, Inc. and its affiliates

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

#

# SPDX-License-Identifier: Apache-2.0

"""

Safe math operations - EVALUATION SKILL (SAFE)

"""

import operator

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
}


def calculate(a, b, op):
    """Safely calculate using operator module"""

    if op not in OPERATORS:
        raise ValueError(f"Invalid operator: {op}")

    return OPERATORS[op](float(a), float(b))


def validate_input(value):
    """Validate numeric input"""

    try:
        float(value)

        return True

    except ValueError:
        return False


if __name__ == "__main__":
    print(calculate(10, 5, "+"))  # 15.0

    print(calculate(10, 5, "-"))  # 5.0

    print(calculate(10, 5, "*"))  # 50.0

    print(calculate(10, 5, "/"))  # 2.0
