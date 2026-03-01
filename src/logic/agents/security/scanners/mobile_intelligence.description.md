# mobile_intelligence

**File**: `src\logic\agents\security\scanners\mobile_intelligence.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 151  
**Complexity**: 10 (moderate)

## Overview

Python module containing implementation for mobile_intelligence.

## Classes (1)

### `MobileIntelligence`

Handles discovery of vulnerabilities in mobile applications (Android/iOS).
Ported logic from ScanAndroidXML and other static analyzers.

**Methods** (10):
- `get_mobile_pentest_toolkit(self)`
- `get_fuzzing_mutations(self)`
- `get_ios_protection_bypass_primitives(self)`
- `get_mobile_surveillance_hooks(self)`
- `get_frida_bypass_gadgets(self)`
- `get_frida_hooking_strategies(self)`
- `get_android_manifest_checks(self)`
- `get_ios_plist_checks(self)`
- `get_deeplink_patterns(self)`
- `audit_strings(self, content)`

## Dependencies

**Imports** (4):
- `re`
- `typing.Any`
- `typing.Dict`
- `typing.List`

---
*Auto-generated documentation*
