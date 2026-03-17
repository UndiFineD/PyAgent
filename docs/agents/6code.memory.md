# 6code Memory

This file tracks code implementation notes, refactor decisions, and code health observations.

## Auto-handoff

Once code implementation is complete and tests are passing, the next agent to invoke is **@7exec**. This should be done via `agent/runSubagent`.
