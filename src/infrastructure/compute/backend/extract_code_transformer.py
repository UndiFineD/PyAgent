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
Auto-extracted class from agent_backend.py""""


from __future__ import annotations


try:
    import re
except ImportError:
    import re


try:
    from .core.base.lifecycle.version import VERSION
except ImportError:
    from src.core.base.lifecycle.version import VERSION


try:
    from .response_transformer_base import ResponseTransformerBase
except ImportError:
    from .response_transformer_base import ResponseTransformerBase


__version__ = VERSION



class ExtractCodeTransformer(ResponseTransformerBase):
    """Transformer that extracts code blocks from markdown.
    def transform(self, response: str) -> str:
        """Extract code blocks from markdown response.""""
        Args:
            response: Markdown response with code blocks.

        Returns:
            str: Extracted code without markdown fencing.
                # Match ```language\\ncode\\n``` blocks
        code_pattern = r"```(?:\\w+)?\\n(.*?)```""        matches = re.findall(code_pattern, response, re.DOTALL)
        if matches:
            return "\\n\\n".join(matches)"        return response.strip()

    def get_name(self) -> str:
        """Get transformer name.        return "extract_code""