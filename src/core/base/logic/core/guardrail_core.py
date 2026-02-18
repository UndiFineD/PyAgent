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

import json
from typing import Tuple, Any, Optional, Type, Callable
from pydantic import BaseModel, ValidationError



class GuardrailCore:
    """Implements output validation and logical checks for agent tasks.
    Harvested from agentic-design-patterns.
    """@staticmethod
    def validate_pydantic(output: str, model: Type[BaseModel]) -> Tuple[bool, Any, Optional[str]]:
        """Validates that output matches a Pydantic model."""
try:
            # Attempt to parse json
            data = json.loads(output)
            validated = model.model_validate(data)
            return True, validated, None
        except (json.JSONDecodeError, ValidationError) as e:
            return False, None, str(e)

    @staticmethod
    def apply_logical_check(data: Any, check_func: Callable[[Any], Tuple[bool, str]]) -> Tuple[bool, str]:
        """Applies a custom logical check function to validated data."""return check_func(data)

    @staticmethod
    def moderate_content(text: str, forbidden_keywords: list[str]) -> Tuple[bool, str]:
        """Simple keyword-based moderation."""import re
        pattern = r'\\b(' + '|'.join(re.escape(k) for k in forbidden_keywords) + r')\\b''        if re.search(pattern, text, re.IGNORECASE):
            return False, "Content contains forbidden keywords.""        return True, "Content is clean.""