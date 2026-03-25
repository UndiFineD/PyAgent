# 2 — Agent Workflow Phases

This document describes the purpose and key deliverables of each phase in the PyAgent agent
workflow pipeline.

## Standard handoff chain

```
@0master → @1project → @2think → @3design → @4plan → @5test → @6code → @7exec → @8ql → @9git
```

---

## Phase summaries

### Think (`@2think`)
- **Input:** project.md with goal + scope boundary
- **Output:** `<project>.think.md` with ≥3 options, tradeoff matrix, recommended option
- **Key rule:** do not jump to recommendation with < 2 fully analysed options

### Design (`@3design`)
- **Input:** think.md recommendation
- **Output:** `<project>.design.md` with interface contracts, naming conventions, and binding decisions
- **Key rule:** all design decisions must include explicit rationale

### Plan (`@4plan`)
- **Input:** design.md
- **Output:** `<project>.plan.md` with numbered tasks, validation commands, acceptance criteria checklist
- **Key rule:** each task must be independently testable

### Test — Red phase (`@5test`)
- **Input:** plan.md acceptance criteria
- **Output:** failing tests (confirmed failing for the right reason)
- **Key rule:** tests must test real behavior, not just imports or `assert True`

### Code (`@6code`)
- **Input:** failing tests
- **Output:** minimal implementation that makes tests pass; no stubs or TODOs
- **Key rule:** after each code change that affects architecture, update the relevant
  `docs/architecture/N<name>.md` section

### Exec (`@7exec`)
- **Input:** green tests
- **Output:** integration validation results; confirms no runtime regressions
- **Key rule:** run validation commands from plan.md verbatim

### QL (`@8ql`)
- **Input:** implemented code
- **Output:** security review; confirms no OWASP Top-10 violations
- **Key rule:** any finding blocks handoff to @9git

### Git (`@9git`)
- **Input:** ql-cleared code on project branch
- **Output:** narrow-staged commit, push, PR opened; kanban updated
- **Key rule:** branch must match project's expected branch before any staging

---

## Execution model (Rust/Python bridge)

- Rust Tokio scheduler dispatches agent tasks
- Python coroutines implement strategy/prompting logic
- All I/O (file, network, subprocess) is async
- Blocking operations are caught by audit tests (`tests/structure/`)

## Git workflow

- One branch per project: `prjNNNNNNN-<short-name>`
- Commits are narrow (only files in project scope)
- PR targets `main`; squash merge is preferred
- `scripts/enforce_branch.py` is the pre-commit hook
