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

import json
from typing import List


class PayloadFormatter:
    """Formats parameter lists into various HTTP request body formats."""

    @staticmethod
    def to_json(params: List[str], value: str = "null") -> str:
        return json.dumps({p: value for p in params}, indent=4)

    @staticmethod
    def to_form_urlencoded(params: List[str], value: str = "null") -> str:
        return "&".join([f"{p}={value}" for p in params])

    @staticmethod
    def to_xml(params: List[str], value: str = "null") -> str:
        xml = "<parameters>\n"
        for p in params:
            xml += f"  <{p}>{value}</{p}>\n"
        xml += "</parameters>"
        return xml

    @staticmethod
    def to_multipart(params: List[str], value: str = "null", boundary: str = "PyAgentBoundary") -> str:
        lines = []
        for p in params:
            lines.append(f"--{boundary}")
            lines.append(f'Content-Disposition: form-data; name="{p}"')
            lines.append("")
            lines.append(value)
        lines.append(f"--{boundary}--")
        return "\n".join(lines)
