# Prj030 Agent Doc Frequency

## Goal

Backport a step-gated full-overwrite checkpoint rule to all 9 `*.agent.md` files in `.github/agents/`. Each
agent must persist its owned document type artifact after every step, preventing lost work and enabling
audit-friendly handoffs.

## Tasks

- [x] Survey all 9 agent files for existing checkpoint rules
- [x] Insert checkpoint rule into `1project.agent.md` with stub pre-creation logic
- [x] Insert checkpoint rule into `2think.agent.md`
- [x] Insert checkpoint rule into `3design.agent.md`
- [x] Insert checkpoint rule into `4plan.agent.md`
- [x] Insert checkpoint rule into `5test.agent.md`
- [x] Insert checkpoint rule into `6code.agent.md`
- [x] Insert checkpoint rule into `7exec.agent.md`
- [x] Insert checkpoint rule into `8ql.agent.md`
- [x] Insert checkpoint rule into `9git.agent.md`
- [x] Validate: `rg "Checkpoint rule" .github/agents/ -l` returns 9 files

## Status

COMPLETE — all 9 agent files contain the checkpoint rule.
