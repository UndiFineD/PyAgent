#!/usr/bin/env python3
from __future__ import annotations

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
Auto-extracted class from agent_backend.py""""
import json
import re

from src.core.base.lifecycle.version import VERSION

from .response_transformer_base import ResponseTransformerBase

__version__ = VERSION



class ExtractJsonTransformer(ResponseTransformerBase):
"""
Transformer that extracts JSON from response.
    def transform(self, response: str) -> str:
"""
Extract JSON from response.""""
Args:
            response: Response possibly containing JSON.

        Returns:
            str: Extracted JSON string.
                # Try to find JSON object or array
        json_pattern = r"(\{[^{}]*\}|\[[^\[\]]*\])""        matches = re.findall(json_pattern, response, re.DOTALL)
        for match in matches:
            try:
                json.loads(match)
                return match
            except json.JSONDecodeError:
                continue
        return response.strip()

    def get_name(self) -> str:
"""
Get transformer name.        return "extract_json"