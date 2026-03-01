# scan_android_manifest

**File**: `src\logic\agents\security\scanners\mobile\apk_deeplens\static_tools\scan_android_manifest.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 4 imports  
**Lines**: 184  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for scan_android_manifest.

## Classes (1)

### `ScanAndroidManifest`

**Inherits from**: object

Class ScanAndroidManifest implementation.

**Methods** (4):
- `__init__(self)`
- `extract_manifest_info(self, extracted_source_path)`
- `is_exported(self, component, ns)`
- `parse_android_manifest(self, manifest_path)`

## Dependencies

**Imports** (4):
- `os`
- `re`
- `static_tools.utility.utility_class.util`
- `xml.etree.ElementTree`

---
*Auto-generated documentation*
