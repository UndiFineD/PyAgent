# agent

**File**: `src\classes\base_agent\agent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 1 functions, 60 imports  
**Lines**: 1295  
**Complexity**: 65 (very_complex)

## Overview

BaseAgent main class and core agent logic.

## Classes (1)

### `BaseAgent`

Base class for all AI-powered agents.

Provides common functionality for agents that use AI backends to improve
code files, documentation, tests, and other artifacts. Handles file I/O,
diff generation, and integration with AI services.

Supports context manager protocol for automatic resource cleanup.

Attributes:
    file_path (Path): Path to the file being improved.
    previous_content (str): Original file content before improvements.
    current_content (str): Improved file content after agent processing.

Subclasses:
    - CoderAgent: Improves source code files
    - TestsAgent: Generates and improves test files
    - ChangesAgent: Manages changelog documentation
    - ContextAgent: Manages context/description files
    - ErrorsAgent: Analyzes and documents errors
    - ImprovementsAgent: Suggests code improvements
    - StatsAgent: Collects and reports statistics

Example:
    class MyAgent(BaseAgent):
        def _get_default_content(self) -> bool:
            return "# New File\n"

    with MyAgent('path/to/file.md') as agent:
        agent.improve_content("Make it better")
        agent.update_file()

Note:
    - Automatically detects markdown files for formatting cleanup
    - Provides fallback responses when AI backend unavailable
    - Supports multiple AI backends via execution_engine (Phase 314)
    - Can be used as context manager for automatic cleanup

**Methods** (64):
- `__init__(self, file_path)`
- `_register_capabilities(self)`
- `suspend(self)`
- `resume(self)`
- `get_capabilities(self)`
- `strategy(self)`
- `strategy(self, value)`
- `_run_command(self, cmd, timeout, max_retries)`
- `global_context(self)`
- `global_context(self, value)`
- ... and 54 more methods

## Functions (1)

### `fix_markdown_content(content)`

Fix markdown formatting in content.

## Dependencies

**Imports** (60):
- `__future__.annotations`
- `asyncio`
- `collections.abc.Callable`
- `datetime.datetime`
- `inspect`
- `logging`
- `os`
- `pathlib.Path`
- `requests`
- `src.core.base.AgentCore.BaseCore`
- `src.core.base.BaseAgentCore.BaseAgentCore`
- `src.core.base.ConnectivityManager.ConnectivityManager`
- `src.core.base.IncrementalProcessor.IncrementalProcessor`
- `src.core.base.ShardedKnowledgeCore.ShardedKnowledgeCore`
- `src.core.base.delegation.AgentDelegator`
- ... and 45 more

---
*Auto-generated documentation*
