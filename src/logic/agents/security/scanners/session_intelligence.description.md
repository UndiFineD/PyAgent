# session_intelligence

**File**: `src\logic\agents\security\scanners\session_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 12 imports  
**Lines**: 108  
**Complexity**: 3 (simple)

## Overview

Python module containing implementation for session_intelligence.

## Classes (1)

### `SessionIntelligence`

Identifies and analyzes session cookies/tokens for common frameworks.
Refactored from badsecrets.

**Methods** (3):
- `identify_session(cls, cookie_value)`
- `generate_jwt_attacks(token, public_key)`
- `decode_flask_cookie(cls, cookie)`

## Dependencies

**Imports** (12):
- `base64`
- `hashlib`
- `hmac`
- `json`
- `re`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

---
*Auto-generated documentation*
