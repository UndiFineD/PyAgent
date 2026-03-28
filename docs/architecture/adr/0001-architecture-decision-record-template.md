# ADR Template

Use this template for all new architecture decisions in `docs/architecture/adr/`.

## File naming

- `NNNN-short-kebab-title.md` (example: `0002-async-runtime-contract.md`)
- `NNNN` increments sequentially.

## Markdown template

```md
# ADR-NNNN - Decision Title

## Status

- Proposed | Accepted | Deprecated | Superseded

## Date

- YYYY-MM-DD

## Owners

- Primary owner(s)
- Reviewers

## Context

Describe the problem, constraints, and why this decision is needed now.

## Decision

State the chosen option clearly and unambiguously.

## Alternatives considered

### Alternative A - Name

- Summary:
- Why not chosen:

### Alternative B - Name

- Summary:
- Why not chosen:

## Consequences

### Positive

- Clear benefit 1
- Clear benefit 2

### Negative / Trade-offs

- Cost or complexity 1
- Risk 1

## Implementation impact

- Affected components:
- Migration/rollout notes:
- Backward compatibility notes:

## Validation and monitoring

- Tests or checks required:
- Runtime signals or metrics to monitor:
- Rollback triggers:

## Related links

- Related project artifact(s):
- Related architecture docs:
- Supersedes/Superseded-by (if any):
```

## Required quality checks

- Decision and alternatives are explicit and testable.
- Consequences include both positive and negative impacts.
- Related project and architecture links are present.
- Validation and rollback expectations are documented.

