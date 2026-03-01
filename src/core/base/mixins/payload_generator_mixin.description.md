# payload_generator_mixin

**File**: `src\core\base\mixins\payload_generator_mixin.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 8 imports  
**Lines**: 168  
**Complexity**: 9 (moderate)

## Overview

Python module containing implementation for payload_generator_mixin.

## Classes (1)

### `PayloadGeneratorMixin`

Mixin providing payload generation capabilities for various exploits.

Inspired by aem-hacker's hardcoded payloads for SSRF, RCE, XSS, etc.

**Methods** (9):
- `__init__(self)`
- `_load_default_templates(self)`
- `generate_ssrf_rce_payload(self, fake_aem_host)`
- `generate_xss_payload(self, payload_type, index)`
- `generate_deserialization_payload(self, payload_type)`
- `generate_groovy_rce_payload(self, command)`
- `add_payload_template(self, name, template)`
- `get_payload_template(self, name)`
- `list_payload_templates(self)`

## Dependencies

**Imports** (8):
- `base64`
- `json`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `urllib.parse.quote`
- `uuid`

---
*Auto-generated documentation*
