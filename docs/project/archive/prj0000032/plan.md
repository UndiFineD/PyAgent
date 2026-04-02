# Prj0000032 Agent Quality Framework

_Status: IN_PROGRESS_
_Planner: @4plan | Updated: 2026-06-13_

## Goal

Define and enforce a consistent structure and quality gate for all agents in
PyAgent. Every agent must be stateless, composable, and testable. The CI
pipeline fails if any quality gate is violated.

## Agent Structure

Each agent directory must contain:

| File | Purpose |
|------|---------|
| `__init__.py` | Entry point and metadata (name, version, description) |
| `agent.py` | Core logic: input parsing, decisions, output generation |
| `test_agent.py` | Unit tests with ≥3 meaningful assertions |
| `config.yaml` | Agent-specific configuration (memory, timeout, model) |
| `schema.json` | Input/output schema enforced via validation |

## Quality Gates

| Gate | Description |
|------|-------------|
| Meaningful test coverage | `test_agent.py` has ≥3 real assertions (not `assert True`) |
| Schema validation | `schema.json` validated against actual I/O data |
| No circular dependencies | Agent dependency graph is acyclic |
| Declared dependencies | All imported libraries present in CI requirements |

## Tasks

- [ ] Define `agents/` directory structure and scaffolding template
- [ ] Implement `test_agent_quality.py` self-validation suite
- [ ] Add schema validation helper (`schema.json` against I/O)
- [ ] Add circular dependency detection to CI
- [ ] Document quality gates in `docs/TEST_QUALITY.md`
- [ ] Add agent registry (`data/agent_registry.json`) lifecycle management
- [ ] Add CI step that runs `test_agent_quality.py` on every PR
- [ ] Write onboarding guide `docs/AGENT_DESIGN_GUIDE.md`

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Directory scaffold defined | T1 | NOT_STARTED |
| M2 | Self-validation suite | T2, T3, T4 | NOT_STARTED |
| M3 | Docs and onboarding | T5, T8 | NOT_STARTED |
| M4 | Registry and lifecycle | T6 | NOT_STARTED |
| M5 | CI integrated | T7 | NOT_STARTED |
