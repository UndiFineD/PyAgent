# APKDeepLens

**File**: `src\logic\agents\security\scanners\mobile\apk_deeplens\APKDeepLens.py`  
**Type**: Python Module  
**Summary**: 2 classes, 1 functions, 12 imports  
**Lines**: 363  
**Complexity**: 8 (moderate)

## Overview

Python module containing implementation for APKDeepLens.

## Classes (2)

### `util`

**Inherits from**: util

A static class for which contain some useful variables and methods

**Methods** (2):
- `mod_print(text_output, color)`
- `print_logo()`

### `AutoApkScanner`

**Inherits from**: object

Class AutoApkScanner implementation.

**Methods** (5):
- `__init__(self)`
- `create_dir_to_extract(self, apk_file, extracted_path)`
- `extract_source_code(self, apk_file, target_dir)`
- `return_abs_path(self, path)`
- `apk_exists(self, apk_filename)`

## Functions (1)

### `parse_args()`

Parse command-line arguments.

## Dependencies

**Imports** (12):
- `argparse`
- `logging`
- `os`
- `report_gen.ReportGen`
- `report_gen.util`
- `static_tools.scan_android_manifest`
- `static_tools.sensitive_info_extractor`
- `subprocess`
- `sys`
- `time`
- `traceback`
- `xml.etree.ElementTree`

---
*Auto-generated documentation*
