# CurationCore

**File**: `src\logic\agents\system\core\CurationCore.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 3 imports  
**Lines**: 48  
**Complexity**: 2 (simple)

## Overview

Core logic for Resource Curation (Phase 173).
Handles pruning of temporary directories and old files.

## Classes (1)

### `CurationCore`

Class CurationCore implementation.

**Methods** (2):
- `prune_directory(directory, max_age_days)`
- `deep_clean_pycache(root_dir)`

## Dependencies

**Imports** (3):
- `os`
- `shutil`
- `time`

---
*Auto-generated documentation*
