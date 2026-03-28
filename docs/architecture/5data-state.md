# 5 - Data, State, and Memory Architecture

This document defines how PyAgent stores and governs mutable state across runtime, projects, and agent memory.

## Data domains

- Runtime data: active tasks, tool traces, ephemeral execution context.
- Project data: canonical status and lifecycle records.
- Agent memory: persistent learnings and decisions per role.
- Artifact data: generated docs, plans, and validation outputs.

## Source-of-truth files

- docs/project/kanban.md: human-readable lifecycle board.
- data/projects.json: machine-readable project registry.
- .github/agents/data/*.memory.md: role-specific memory state.

## Consistency rules

- kanban.md and projects.json must be updated in the same change set.
- Project identifiers are immutable once assigned.
- Branch plans and project IDs must remain aligned.

## State transition model

Typical project lane progression:

Ideas -> Discovery -> Design -> In Sprint -> Review -> Released -> Archived

Each transition requires:

- explicit actor ownership
- acceptance criteria checkpoint
- audit trail update in project artifacts

## Memory quality rules

- Store concise, decision-relevant facts.
- Record recurrence patterns and promotion-to-rule signals.
- Remove or correct stale guidance when invalidated by new evidence.

## Security and retention

- Do not persist secrets in memory or project artifacts.
- Limit sensitive operational details to least-privilege docs.
- Keep audit-friendly, minimal, and attributable records.
