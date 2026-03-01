# sensitive_info_extractor

**File**: `src\logic\agents\security\scanners\mobile\apk_deeplens\static_tools\sensitive_info_extractor.py`  
**Type**: Python Module  
**Summary**: 2 classes, 0 functions, 3 imports  
**Lines**: 151  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for sensitive_info_extractor.

## Classes (2)

### `bcolors`

Class bcolors implementation.

### `SensitiveInfoExtractor`

**Inherits from**: object

Class SensitiveInfoExtractor implementation.

**Methods** (4):
- `get_all_file_paths(self, file_path)`
- `extract_all_sensitive_info(self, list_of_files, relative_path)`
- `extract_insecure_request_protocol(self, list_of_files)`
- `extract(self, text)`

## Dependencies

**Imports** (3):
- `os`
- `re`
- `utility.utility_class.util`

---
*Auto-generated documentation*
