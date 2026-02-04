#!/usr/bin/env python3
# Copyright 2026 PyAgent Authors

import json
from typing import List, Dict

class PayloadFormatter:
    """ Formats parameter lists into various HTTP request body formats. """

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
