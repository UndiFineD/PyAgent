# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Context Manager Design

The `src/context_manager` package probably handles how context objects are
created, merged, diffed, and shared between agents.  `src-old` contains many
`Context*` classes, suggesting a rich legacy implementation.

## Legacy Overview (from src-old)

- `ContextAnnotation`, `ContextCompressor`, `ContextDiffer`, `ContextExporter`,
  `ContextSharingManager`, etc., indicating responsibilities like forcing
  annotations onto data, compressing context for storage, calculating
  differences between context versions, exporting context to external formats,
  and managing sharing policies.

## Design Principles

- **Immutable snapshots** – contexts should be versioned and immutable once
  created to simplify reasoning.
- **Hierarchical structure** – support nested contexts with inheritance and
  overrides (e.g. global vs. agent‑specific context).
- **Diff/merge utilities** – enable efficient synchronization between nodes or
  saving incremental changes.
- **Privacy and access control** – contexts may contain sensitive data; the
  manager should enforce sharing rules and redaction.

## Brainstorm Topics

- Schema for context metadata and tagging.
- Compression strategies (lossy vs lossless) for large contexts.
- Conflict resolution algorithms when merging divergent context trees.
- Integration with memory and transport subsystems for distributed context
  propagation.

We have already implemented `.github\superpower\brainstorm\2026-03-07-llm-context-consolidation-design.md`
with `.github\superpower\plan\2026-03-08-llm-context-consolidation-plan.md`

We can expand with https://github.com/yarnpkg/yarn context cache, 
locally we should be able to do megabytes of context cache, 
but we have to watch and prevent hallucination drift.

*Reuse comments from modules such as `src-old/classes/context/ContextEngine` if present.*