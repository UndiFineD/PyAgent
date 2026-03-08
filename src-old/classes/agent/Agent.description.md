# Agent

**File**: `src\classes\agent\Agent.py`  
**Type**: Python Module  
**Summary**: 1 classes, 0 functions, 46 imports  
**Lines**: 1104  
**Complexity**: 62 (very_complex)

## Overview

OrchestratorAgent for PyAgent Swarm Management.

This agent acts as the primary coordinator for sub-swarms, managing task delegation,
resource allocation, and final response synthesis. It implements advanced 
self-healing and multi-agent synergy protocols.

## Classes (1)

### `OrchestratorAgent`

Main agent that orchestrates sub-agents for code improvement.

This class has been refactored to delegate logic to specialized managers:
- metrics_manager: Handles tracking and reporting of execution metrics
- file_manager: Handles file discovery, snapshots, and ignore patterns
- git_handler: Handles git operations (commit, branch)
- command_handler: Handles subprocess execution and sub-agent orchestration
- core: Pure logic and parsing (Rust-ready component)

**Methods** (62):
- `__init__(self, repo_root, agents_only, max_files, loop, skip_code_update, no_git, dry_run, selective_agents, timeout_per_agent, enable_async, enable_multiprocessing, max_workers, strategy, models_config)`
- `metrics(self)`
- `metrics(self, value)`
- `webhooks(self)`
- `callbacks(self)`
- `process_files_multiprocessing(self, files)`
- `strategy(self)`
- `strategy(self, value)`
- `__enter__(self)`
- `__exit__(self, exc_type, exc_val, exc_tb)`
- ... and 52 more methods

## Dependencies

**Imports** (46):
- `__future__.annotations`
- `asyncio`
- `collections.abc.Callable`
- `concurrent.futures.ProcessPoolExecutor`
- `concurrent.futures.ThreadPoolExecutor`
- `concurrent.futures.TimeoutError`
- `contextlib.contextmanager`
- `importlib.util`
- `logging`
- `pathlib.Path`
- `src.core.base.AgentCommandHandler.AgentCommandHandler`
- `src.core.base.AgentCore.AgentCore`
- `src.core.base.AgentCore.BaseCore`
- `src.core.base.AgentPluginBase.AgentPluginBase`
- `src.core.base.AgentUpdateManager.AgentUpdateManager`
- ... and 31 more

---
*Auto-generated documentation*
