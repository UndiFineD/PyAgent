# Migration Guide

This document collects notes and checklists for migrating synchronous
subsystems into the new `runtime` framework.

## Process Overview

1. **Identify candidate module**: look for ``while`` loops or long-running
   background tasks in ``src/``.
2. **Write a simple unit test** that exercises the feature and ensures
   observable behaviour remains the same.
3. **Port to runtime**:
   * Replace blocking ``time.sleep`` loops with ``async def`` loops that use
     ``runtime_py.sleep``.
   * Spawn tasks using ``runtime_py.spawn`` instead of ``asyncio.create_task``
     or manual thread management.
   * Remove the synchronous implementation entirely once the async version is
     verified.
4. **Update tests** and run full suite (`pytest -q`) plus the loop checker to
   confirm no remaining sync loops.
5. **Document change** in `MIGRATION.md` (this file) and, if appropriate,
   add a migration plan entry to ``.github/superpower/plan/2026-03-10-async-runtime-plan.md``
   or a new plan file.
6. **Create GitHub issue/PR** referencing the plan and tests.

## Completed Ports

* `runtime_py` helpers (spawn, event bus, watcher, HTTP server)
* `observability.stats.metrics_engine` proof‑of‑concept
* `observability.stats.legacy_engine` demonstration port 
  – initial sync loop flagged by audit, then rewritten using `runtime_py.spawn` and `sleep`.

## Next Candidates

* [x] `src/core/base/metrics_engine` (full version) when ready – 
  large file migration will follow the same pattern as above.
* Any remaining long-running loops uncovered by the async loop checker (currently none).

The audit script only looks for `while`/`for` loops that could run forever; new
candidates often appear in the following categories:

  * background polling tasks (e.g. HTTP or socket servers, file watchers).
  * custom schedulers or job runners that sleep or wait in a loop.
  * transport/queue processors that spin waiting for messages.
  * legacy utilities (rate limiters, health‑check daemons, etc.) still using
    `time.sleep`.

The following modules are potential migration targets once they surface or are
added to the repo:

* `src/transport/queue_manager.py` – hypothetical message dispatcher that may
  eventually contain a loop.
* `src/validation/rate_limiter.py` – often implemented with a sleeping thread.
* `src/schedulers/*` – any future scheduler implementations belong here.
* `src/core/base/health_monitor.py` – monitor loops that poll dependencies.

(Use `grep -R "while True" src/` and the loop checker regularly.  New
candidates should be added to this list as they are discovered.)

## Notes

As of 2026-03-10 the asynchronous audit script reports zero failing files; the
runtime rollout is effectively complete for existing modules.  Future work may
revisit the large `core/base/metrics_engine` once decomposition yields
manageable components.

## Next Candidates

* [X] Any remaining long-running loops uncovered by the async loop checker.
* [X] ``src/core/base/metrics_engine`` (full version) when ready.
* [X] `src/validation/rate_limiter.py` (hypothetical example)


