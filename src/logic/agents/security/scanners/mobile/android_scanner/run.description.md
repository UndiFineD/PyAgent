# run

**File**: `src\logic\agents\security\scanners\mobile\android_scanner\run.py`  
**Type**: Python Module  
**Summary**: 0 classes, 4 functions, 13 imports  
**Lines**: 103  
**Complexity**: 4 (simple)

## Overview

Python module containing implementation for run.

## Functions (4)

### `get_available_models()`

### `process_file(file_path, code_content, model_key, model_variant, input_dir, output_dir)`

### `process_and_generate_reports(all_pathes, model_key, model_variant, input_dir, output_dir, num_threads)`

### `main()`

## Dependencies

**Imports** (13):
- `argparse`
- `concurrent.futures.ThreadPoolExecutor`
- `concurrent.futures.as_completed`
- `config.Models`
- `config.api_keys`
- `config.instruction`
- `markdown`
- `models.genai_model.scan_code`
- `os`
- `sys`
- `termcolor.colored`
- `utils.extract_apk_helpers.extract_apk_with_jadx`
- `utils.html_helpers.generate_index_html`

---
*Auto-generated documentation*
