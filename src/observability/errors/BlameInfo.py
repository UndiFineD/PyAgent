#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors
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


"""Auto-extracted class from agent_errors.py"""

from __future__ import annotations
from src.core.base.Version import VERSION
from dataclasses import dataclass

__version__ = VERSION


@dataclass
class BlameInfo:
    """Git blame information for an error.

    Attributes:
        error_id: ID of the error.
        commit_hash: Commit that introduced the error.
        author: Author of the commit.
        commit_date: Date of the commit.
        commit_message: Commit message.
    """

    error_id: str
    commit_hash: str = ""
    author: str = ""
    commit_date: str = ""
    commit_message: str = ""
