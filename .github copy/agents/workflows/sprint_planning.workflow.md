---
title: Sprint Planning Workflow
description: Prepare the backlog for the next sprint
---

# Sprint Planning Workflow

**Description**: Prepare the backlog for the next sprint

## Orchestration Steps

1. @priority: Score and rank tasks in the current backlog.
2. @budget: Review budget constraints and estimated task burn rates.
3. @task_queue: Assign high-priority items into the .github/agents/kanban/kanban.json.
4. @standup: Prepare the kickoff notes for the daily/sprint sync.

## Escalation Path
If any agent fails executing its step, it MUST invoke `@agentwriter` to document the gap or generate a new repair agent.
Errors must be logged into `.github/agents/log/error_signatures.log`.
