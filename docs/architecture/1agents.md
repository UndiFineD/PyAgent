# 1 — Agent System Reference

PyAgent is a **transactional, Rust-accelerated multi-agent system** built for safe, autonomous
code improvement.

## Key Concepts

- **Core/Agent separation**: Agents orchestrate; `*Core` classes contain domain logic.
- **Mixins** provide shared behavior (persistence, memory, identity, auditing) without deep
  inheritance. See `src/core/base/mixins/`.
- **Transactional safety**: all file-system changes are wrapped in `StorageTransaction` /
  `MemoryTransaction` / `ProcessTransaction` and can rollback on failure.
- **Rust acceleration**: `rust_core/` holds performance kernels (diff/patch, metrics, parsing)
  exposed via PyO3.
- **Async runtime**: Agents run in a Tokio-based scheduler (Rust) with Python coroutines;
  blocking loops are prohibited by audit tests.

## Agent Roster

| Agent | Role | Definition file |
|---|---|---|
| `@0master` | Strategic coordinator; owns prjNNNNNNN namespace | `.github/agents/0master.agent.md` |
| `@1project` | Project setup, branch plan, folder creation | `.github/agents/1project.agent.md` |
| `@2think` | Options exploration, tradeoff analysis | `.github/agents/2think.agent.md` |
| `@3design` | Architecture decisions, interface contracts | `.github/agents/3design.agent.md` |
| `@4plan` | Implementation plans, task breakdowns | `.github/agents/4plan.agent.md` |
| `@5test` | TDD red phase, test strategy, green validation | `.github/agents/5test.agent.md` |
| `@6code` | Production code implementation | `.github/agents/6code.agent.md` |
| `@7exec` | Runtime validation, integration checks | `.github/agents/7exec.agent.md` |
| `@8ql` | Security and CodeQL review | `.github/agents/8ql.agent.md` |
| `@9git` | Branch validation, narrow staging, PRs | `.github/agents/9git.agent.md` |

## Agent Memory and Logs

All agent memory and log files live in `.github/agents/`:

| File pattern | Purpose |
|---|---|
| `.github/agents/<N><name>.memory.md` | Persistent memory for each agent |
| `.github/agents/<N><name>.log.md` | Execution log for each agent (readable via API) |

## Primary source paths

| Path | Purpose |
|---|---|
| `src/core/base/` | Transaction managers, mixins, state models |
| `src/logic/agents/` | Agent orchestration |
| `src/logic/` | Reasoning cores and coordination |
| `src/inference/` | LLM connectors, tool loops, streaming |
| `rust_core/` | Rust performance libraries |

## Quick setup (local)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd rust_core
maturin develop --release
```
