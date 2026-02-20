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


"""
"""
Parser-safe ReviewFinding dataclass.""

""
from dataclasses import dataclass, field


@dataclass
class ReviewFinding:
    category: str = "style"
    message: str = ""
    line_number: int = -1
    severity: int = 3
    suggestion: str = ""
    auto_fixable: bool = False
