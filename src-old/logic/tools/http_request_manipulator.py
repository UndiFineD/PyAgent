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

"""LLM_CONTEXT_START

## Source: src-old/logic/tools/http_request_manipulator.description.md

# http_request_manipulator

**File**: `src\\logic\tools\\http_request_manipulator.py`  
**Type**: Python Module  
**Summary**: 0 classes, 0 functions, 0 imports  
**Lines**: 39  
**Complexity**: 0 (simple)

## Overview

HTTP Request Manipulation Prompts.
Derived from Chatio (0xSojalSec).

---
*Auto-generated documentation*
## Source: src-old/logic/tools/http_request_manipulator.improvements.md

# Improvements for http_request_manipulator

**File**: `src\\logic\tools\\http_request_manipulator.py`  
**Analysis Date**: 2026-03-01 00:18  
**Size**: 39 lines (small)  
**Complexity**: 0 score (simple)

## Suggested Improvements

### Type Annotations
- [OK] Review and add type hints to all functions and methods for better IDE support

### Testing
- [!] **Missing test file** - Create `http_request_manipulator_test.py` with pytest tests

## Best Practices Checklist

- All classes have docstrings
- All public methods have docstrings
- Type hints are present
- pytest tests cover main functionality
- Error handling is robust
- Code follows PEP 8 style guide
- No code duplication
- Proper separation of concerns

---
*Auto-generated improvement suggestions*

LLM_CONTEXT_END
"""

"""
HTTP Request Manipulation Prompts.
Derived from Chatio (0xSojalSec).
"""

HTTP_MANIPULATION_SYSTEM_PROMPT = """You are an expert security testing assistant for HTTP requests.
Analyze the user's natural language command and return ONLY a JSON response with the appropriate action.

Available actions:
- change_method: Change HTTP method (GET, POST, PUT, DELETE, etc.)
- add_header: Add/update a header
- remove_headers: Remove headers (all or specific ones)
- change_body: Modify request body
- remove_body: Remove request body
- add_param: Add URL parameter
- multiple_actions: For complex operations like request smuggling

For security tests like "request smuggling", "SQL injection", create appropriate headers/body modifications.

ALWAYS respond with valid JSON only. No explanations outside JSON.

Examples:
User: "change method to POST" -> {"action":"change_method","method":"POST","message":"Changed to POST"}
User: "add authorization header" -> {"action":"add_header","header":"Authorization","value":"Bearer token_here","message":"Added Authorization header"}
User: "apply request smuggling" -> {"action":"multiple_actions","actions":[{"action":"add_header","header":"Transfer-Encoding","value":"chunked"},{"action":"add_header","header":"Content-Length","value":"0"}],"message":"Applied request smuggling headers"}
"""
