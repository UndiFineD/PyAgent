# Concurrency Standard: Async-First

## Overview
PyAgent is designed to operate as a high-performance asynchronous swarm.

## 1. Mandatory `asyncio`
- **Standard**: All I/O, network requests, and subprocess executions must use `asyncio`.
- **Requirement**: Use `aiohttp` for networking and `aiofiles` for filesystem operations.
- **Async Subsytems**: Modules in `src/infrastructure/voyager/` and `src/core/base/shell.py` are the primary executors of this pattern.

## 2. Non-Blocking Execution
- **Task Management**: Agents should yield control frequently to ensure the event loop remains responsive.
- **Preemption**: High-priority tasks (e.g., `CRITICAL` signals) can preempt long-running async tasks via the `FleetExecutionCore`.

## 3. Worker Offloading
- If a task is CPU-bound and not yet implemented in `rust_core/`, use `asyncio.to_thread()` or `ProcessPoolExecutor` to avoid blocking the main event loop.

---
*Maintained under Voyager Stability Guidelines.*
