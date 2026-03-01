# PRAgent

**File**: `src\classes\specialized\PRAgent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 9 imports  
**Lines**: 172  
**Complexity**: 9 (moderate)

## Overview

Agent specializing in Git operations, pull request analysis, and code review.
Inspired by PR-Agent and GitHub CLI.

## Classes (1)

### `PRAgent`

**Inherits from**: BaseAgent

Analyzes differences in the codebase and generates summaries or review comments.

**Methods** (9):
- `__init__(self, file_path)`
- `_record(self, action, details, result)`
- `get_diff_summary(self, branch)`
- `analyze_commit_history(self, limit)`
- `create_patch_branch(self, branch_name)`
- `stage_all_and_commit(self, message)`
- `generate_pr_description(self, branch)`
- `review_changes(self)`
- `improve_content(self, prompt)`

## Dependencies

**Imports** (9):
- `__future__.annotations`
- `pathlib.Path`
- `src.core.base.BaseAgent.BaseAgent`
- `src.core.base.utilities.as_tool`
- `src.core.base.version.VERSION`
- `src.infrastructure.backend.LocalContextRecorder.LocalContextRecorder`
- `subprocess`
- `time`
- `typing.Any`

---
*Auto-generated documentation*
