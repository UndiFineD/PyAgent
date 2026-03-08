# template_collector

**File**: `src\logic\tools\nuclei\template_collector.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 7 imports  
**Lines**: 131  
**Complexity**: 5 (moderate)

## Overview

Python module containing implementation for template_collector.

## Classes (1)

### `NucleiTemplateCollector`

Collects Nuclei templates from various public repositories.
Adapted from AllForOne tool.

**Methods** (5):
- `__init__(self, output_dir)`
- `_git_clone(self, url, destination)`
- `_generate_destination_folder(self, url)`
- `_clone_repository(self, repo)`
- `collect_templates(self, source_url)`

## Dependencies

**Imports** (7):
- `concurrent.futures.ThreadPoolExecutor`
- `concurrent.futures.wait`
- `logging`
- `os`
- `requests`
- `shutil`
- `subprocess`

---
*Auto-generated documentation*
