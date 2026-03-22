# PyAgent — Master Agent Memory

_Last updated: 2026-03-21_

---

## 2026-03-21 Session Summary — Project Governance Closure Wave

All 42 projects have been surveyed and governance PRs created:

| PR | Branch | Projects | Status |
|---|---|---|---|
| #127 | prj037-tools-crdt-security | prj0000042 | open |
| #128 | prj0000002-core-system | prj0000002 | open |
| #129 | prj0000003-hybrid-llm-security | prj0000003 | open |
| #130 | prj0000039-conftest-typing-fixes | prj0000039 | open |
| #131 | prj0000041-flm | prj0000041 | open |
| #132 | prj0000009-community-collaboration | prj009,010,019,020,024,025,027,029,040 | open |
| #133 | prj0000011-core-project-structure | prj011-018,021-023,026,028,030-038 | open |
| #134 | prj0000001-async-runtime | prj0000001 | open |
| #135 | prj0000005-llm-swarm-architecture | prj0000005 | open (IN_PROGRESS: 13/16 tasks) |

**Previously merged:** prj0000004 (#123), prj0000006 (#124), prj0000007 (#125), prj0000008 (#126).

**prj0000005 remaining tasks:**
- `src/swarm/swarm_node.py` — minimal peer with ping/pong
- `tests/test_swarm_node.py`
- `scripts/run_swarm_demo.py`

---

## Standing Policy — Branch Isolation

- One `prjNNNNNNN` workstream maps to one branch. Project work must not piggyback on the active branch of another project.
- `@0master` assigns or validates the expected branch during project kickoff and ensures `@1project` records that branch, the scope boundary, and the git handoff rule in the project overview.
- `@9git` is expected to reject mixed-project changes, inherited branches, and broad staging guidance for project work.
- When branch hygiene fails, `@0master` owns the correction loop: update the governing guidance, return the task to the agent that owns the project boundary, and do not normalize the failure as an accepted workflow.

## Standing Policy — Project Numbering Ownership

- `@0master` owns `prjNNNNNNN` allocation, validation, and continuity tracking.
- Project numbering is part of the project boundary. A project is not fully defined until the assigned `prjNNNNNNN`, project folder, and expected branch agree.
- `@1project` must consume the identifier assigned by `@0master`. It must not invent, renumber, or resolve ambiguity on its own.
- Do not reuse old numbers or skip numbers casually. If a number is reserved, retired, skipped, or corrected, record the reason here before downstream handoff.
- If numbering is missing, conflicting, or ambiguous, stop the workflow and send the task back through `@0master` before project setup continues.

## Project Numbering Tracking

- Latest confirmed project folder in `docs/project/`: `prj0000042`.
- Project folder numbering migrated from 3-digit (`prj001`-`prj038`) to 7-digit (`prj0000001`-`prj0000042`).
- Legacy duplicate groups were resolved by assigning unique 7-digit identifiers during migration.
- `prj0000043` allocated 2026-03-22: `prj0000043-p2p-security-deps` — libp2p 0.49→0.56, 6 Dependabot CVEs. PR open.
- `prj0000044` allocated 2026-03-22: `prj0000044-transaction-managers` — add missing StorageTransaction/ProcessTransaction/ContextTransaction stubs for CI. PR #136 open.
- `prj0000045` allocated 2026-03-22: `prj0000045-transaction-managers-full` — full proper design of all four transaction managers (src/transactions/ package, BaseTransaction ABC, LLM context integration, encrypted storage, remote memory). **COMPLETE** — PR #137 open. 62/62 tests pass: 14 existing (via shims) + 48 new acceptance tests. @8ql: 2 HIGH findings fixed (M-1 false encrypt guarantee → NotImplementedError; M-2 SSRF → URL scheme validation). Next: review + merge PR #137.
- Next `prjNNNNNNN` to allocate: `prj0000046` (validate against `docs/project/` inventory before assignment).

## Branch Registry (all 45 projects)

| Dir | Expected Branch | Status |
|---|---|---|
| prj0000001 | `prj0000001-async-runtime` | pre-existing |
| prj0000002 | `prj0000002-core-system` | assigned 2026-03-21 |
| prj0000003 | `prj0000003-hybrid-llm-security` | assigned 2026-03-21 |
| prj0000004 | `prj0000004-llm-context-consolidation` | assigned 2026-03-21 |
| prj0000005 | `prj0000005-llm-swarm-architecture` | assigned 2026-03-21 |
| prj0000006 | `prj0000006-unified-transaction-manager` | assigned 2026-03-21 |
| prj0000007 | `prj0000007-advanced-research` | assigned 2026-03-21 |
| prj0000008 | `prj0000008-agent-workflow` | assigned 2026-03-21 |
| prj0000009 | `prj0000009-community-collaboration` | assigned 2026-03-21 |
| prj0000010 | `prj0000010-context-management` | assigned 2026-03-21 |
| prj0000011 | `prj0000011-core-project-structure` | assigned 2026-03-21 |
| prj0000012 | `prj0000012-deployment-operations` | assigned 2026-03-21 |
| prj0000013 | `prj0000013-dev-tools-autonomy` | assigned 2026-03-21 |
| prj0000014 | `prj0000014-dev-tools-capabilities` | assigned 2026-03-21 |
| prj0000015 | `prj0000015-dev-tools-implementation` | assigned 2026-03-21 |
| prj0000016 | `prj0000016-dev-tools-structure` | assigned 2026-03-21 |
| prj0000017 | `prj0000017-dev-tools-utilities` | assigned 2026-03-21 |
| prj0000018 | `prj0000018-documentation-assets` | assigned 2026-03-21 |
| prj0000019 | `prj0000019-future-roadmap` | assigned 2026-03-21 |
| prj0000020 | `prj0000020-github-import` | assigned 2026-03-21 |
| prj0000021 | `prj0000021-project-management-governance` | assigned 2026-03-21 |
| prj0000022 | `prj0000022-swarm-architecture` | assigned 2026-03-21 |
| prj0000023 | `prj0000023-testing-infrastructure` | assigned 2026-03-21 |
| prj0000024 | `prj0000024-async-runtime` | assigned 2026-03-21 |
| prj0000025 | `prj0000025-core-system` | assigned 2026-03-21 |
| prj0000026 | `prj0000026-test-coverage-quality` | assigned 2026-03-21 |
| prj0000027 | `prj0000027-encrypted-memory-blocks` | assigned 2026-03-21 |
| prj0000028 | `prj0000028-transport-t1` | assigned 2026-03-21 |
| prj0000029 | `prj0000029-llm-ui-backend-worker` | assigned 2026-03-21 |
| prj0000030 | `prj0000030-agent-doc-frequency` | assigned 2026-03-21 |
| prj0000031 | `prj0000031-streaming-website` | assigned 2026-03-21 |
| prj0000032 | `prj0000032-agents` | assigned 2026-03-21 |
| prj0000033 | `prj0000033-chat` | assigned 2026-03-21 |
| prj0000034 | `prj0000034-context-manager` | assigned 2026-03-21 |
| prj0000035 | `prj0000035-multimodal` | assigned 2026-03-21 |
| prj0000036 | `prj0000036-plugins` | assigned 2026-03-21 |
| prj0000037 | `prj0000037-tools` | assigned 2026-03-21 |
| prj0000038 | `prj0000038-python-function-coverage` | assigned 2026-03-21 |
| prj0000039 | `prj0000039-conftest-typing-fixes` | assigned 2026-03-21 |
| prj0000040 | `prj0000040-core-system` | assigned 2026-03-21 |
| prj0000041 | `prj0000041-flm` | assigned 2026-03-21 |
| prj0000042 | `prj0000042-tools-crdt-security` | pre-existing |
| prj0000043 | `prj0000043-p2p-security-deps` | assigned 2026-03-22 |
| prj0000044 | `prj0000044-transaction-managers` | assigned 2026-03-22 |
| prj0000045 | `prj0000045-transaction-managers-full` | PR #137 open — COMPLETE |

## Learning Loop — Branch Hygiene

- Record branch hygiene failures in `docs/agents/9git.memory.md` with: date, project, observed branch, failure type, and required fix.
- Reflect recurring failures or policy changes here so future coordinators enforce the updated workflow earlier.
- Shared-branch history under unrelated projects is a warning signal, not an exception path.
- 2026-03-20: Added mandatory "Branch gate" preflight to `@2think` through `@8ql` agent definitions.
    Downstream agents must now stop immediately on expected/observed branch mismatch,
    mark their project artifact + memory entry as BLOCKED, and hand back to `@0master`.
- 2026-03-20: Extended branch-gate enforcement to `@1project` and `@0master` delegation preflight.
    Result: branch mismatch is now blocked at project setup, planning/execution, and git handoff layers.

---

## ✅ Completed subsystems (do NOT reimplement)

| Subsystem | Plan file | Notes |
|---|---|---|
| Async Runtime | 2026-03-10-async-runtime-plan.md | 215+ tests passing, zero sync loops |
| FLM / Fastflow integration | 2026-03-08-flm-plan.md | OpenAI adapter, tool-call loop complete |
| Context Manager & Skills Registry | 2026-03-09-context_management-plan.md | Windowing + skill discovery live |
| Advanced Research packages | prj007-advanced_research/ | 5 skeleton packages importable; code/test DONE; exec/ql/git pending |
| Future Roadmap tooling | future-roadmap-plan.md | Vision templates, milestone generator complete |
| Community Chat | community-collaboration-plan.md | FastAPI, MCP tools, GitHub webhooks live |
| Agent Workflow basics | agent-workflow-plan.md | TaskState, Task, TaskQueue, WorkflowEngine, CoRT live |
| GitHub Importer skeleton | github-import-plan.md | Importer skeleton fully implemented |
| Unified Transaction Manager | prj006-unified-transaction-manager/ | Full pipeline DONE (75d5c3e) — 205 tests, 100% coverage |

---

## 🗂️ Implementation Phases

### Phase 1 — Foundation & Infrastructure
**Status:** 🔴 PENDING — BLOCKING all other phases  
**Goal:** Establish stable core infrastructure: 
    CI green, transaction managers unified, project structure clean, LLM context consolidated.

**Subsystems:**
- **Conftest typing fixes** (`conftest-typing-fixes-plan.md`) 
    — URGENT: blocks all CI gates; 6 tasks
- **Unified transaction manager** (`unified-transaction-manager-plan.md`) 
    — 7 tasks; StorageTransaction, MemoryTransaction, ProcessTransaction, ContextTransaction unification
- **Core project structure** (`core-project-structure-plan.md`) 
    — 7 tasks; directory layout, module boundaries, import hygiene
- **LLM context consolidation** (`llm-context-consolidation-plan.md`) 
    — 6 tasks; single ContextWindow, token budget tracking
- **Core system modules** (`core-system-plan.md`) 
    — 8 task groups; runtime bootstrap, observability, error taxonomy
- **Testing infrastructure** (`testing-infrastructure-plan.md`) 
    — CI enforcement, async loop checker, pytest fixtures

**Brainstorm designs to feed into @1think:**
- `docs/project/*/brainstorm.md` files covering: core architecture, 
    transaction design, context management, testing

**Acceptance criteria:**
- All CI pipelines green (pytest, ruff, mypy)
- All four transaction types (Storage/Memory/Process/Context) unified under single interface
- Zero circular imports; `conftest.py` fully typed
- LLM context consolidation: one ContextWindow class in use across codebase

---

### Phase 2 — Core Agent & Swarm Features
**Status:** 🟡 PENDING — unblocked after Phase 1  
**Goal:** Implement full swarm orchestration: agent registry, task scheduler, 
    distributed memory stores, inter-agent communication.

**Subsystems:**
- **Swarm architecture** (`swarm-architecture-plan.md`) 
    — 6+ tasks; AgentRegistry, TaskScheduler, MemoryStore, metrics, inter-agent protocols
- **LLM swarm architecture** (`llm-swarm-architecture-plan.md`) 
    — 6 phases; multi-LLM routing, load balancing, fallback chains
- **Deployment operations** (`deployment-operations-plan.md`) 
    — 7 tasks; Docker Compose, provisioning, health checks
- **Dev tools capabilities** (`dev-tools-capabilities-plan.md`) 
    — 6 tasks; code analysis, metrics, dependency graphs
- **Dev tools autonomy** (`dev-tools-autonomy-plan.md`) 
    — 7 tasks; self-healing, auto-fix pipelines

**Brainstorm designs to feed into @1think:**
- Swarm topology design, LLM router design, agent registry schema, task scheduler algorithm

**Acceptance criteria:**
- AgentRegistry can register/discover/heartbeat agents
- TaskScheduler can assign tasks to agents based on capability and load
- Multi-LLM routing with fallback chains functional
- Docker Compose stack brings up full swarm locally

---

### Phase 3 — Security, Encrypted Memory & Transport
**Status:** 🟡 PENDING — unblocked after Phase 1; partially after Phase 2  
**Goal:** End-to-end encrypted agent communication, Rust-native crypto primitives, and P2P transport layer.

**Subsystems:**
- **Hybrid LLM security** (`hybrid-llm-security-plan.md`) 
    — 14/15 tasks pending; Rust crypto core, key exchange, auth
- **Encrypted memory blocks** (`encrypted-memory-blocks-plan.md`) 
    — 20 tasks; X25519 ECDH + ChaCha20-Poly1305 in Rust, PyO3 bindings
- **Transport T-1** (`transport-t1-plan.md`) 
    — 20 tasks; Ed25519 NodeIdentity, Noise_XX handshake, QUIC scaffold
- **P2P CRDT** (brainstorm) 
    — libp2p + Automerge for distributed agent state

**Brainstorm designs to feed into @1think:**
- Crypto primitive selection, key derivation scheme, Noise protocol integration, QUIC transport design

**Acceptance criteria:**
- All memory reads/writes through EncryptedMemoryBlock with X25519 + ChaCha20-Poly1305
- Ed25519 NodeIdentity: every agent has a keypair; messages are signed
- Noise_XX handshake completes between two agent nodes
- QUIC loopback transport passes integration tests
- All Rust code passes `cargo clippy -D warnings`

---

### Phase 4 — UI, Developer Tools & Polish
**Status:** 🟡 PENDING — unblocked after Phase 2  
**Goal:** Production-quality frontend + backend streaming, developer self-improvement tools, 
    documentation, and governance.

**Subsystems:**
- **LLM UI backend worker** (`llm-ui-backend-worker-plan.md`) 
    — 16 tasks; FastAPI + WebSocket streaming, WebRTC signaling, voice input, AI action control
- **Dev tools structure / utilities / implementation** (`dev-tools-*-plan.md`) 
    — 16 tasks across 3 files
- **Test coverage quality** (`test-coverage-quality-plan.md`) 
    — 8 tasks; mypy strict, ruff full ruleset, coverage thresholds
- **Documentation assets** (`documentation-assets-plan.md`) 
    — 7 tasks; MkDocs, diagrams, changelog
- **Project management governance** (`project-management-governance-plan.md`) 
    — PM dashboards, risk matrix, budget tracking

**Acceptance criteria:**
- WebSocket streaming UI delivers tokens in real-time
- WebRTC signaling scaffold functional
- MkDocs site builds cleanly (`mkdocs build --strict`)
- Coverage ≥ 80% on all `src/` modules
- Governance templates operational (risk matrix, budget tracker)

---

## 🔗 Agent workflow

```
@0master → @1think → @2plan → @3test → @4code → @5exec → @6ql → @7git → @0master
```

## 📁 Key file locations

- Brainstorm designs: `docs/project/*/brainstorm.md`
- Implementation plans: `docs/project/*/plan.md`
- Agent memory files: `docs/agents/<N><name>.memory.md`
- Architecture docs: `docs/architecture/`
- Agent definitions: `.github/agents/`

---

## 🤖 Auto-handoff (agent/runSubagent)

When the master agent sets strategy and delegates work, it should trigger the next agent 
in the pipeline automatically using `agent/runSubagent`.

### Expected automatic handoff chain (primary workflow)
1. **@0master** establishes strategy and delegates to **@1project** via `agent/runSubagent`.
2. **@1project** executes planning and then delegates to **@9git** via `agent/runSubagent`.
3. **@9git** performs git operations (branching, commits, PRs) and, when complete, 
automatically returns control to **@0master** via `agent/runSubagent`.

> This ensures the workflow is self-advancing: the master agent kickstarts the process, 
handoffs are explicit via `agent/runSubagent`, and completion naturally flows back to the master.

### 🧠 MCP Server & Skills Awareness
Agents should be aware of available MCP servers and the skills registered under `.agents/skills`. 
They can reference or invoke these skills as part of their workflow 
(e.g., using `agent/runSubagent` or tool-call patterns) to reuse existing capabilities 
instead of reimplementing logic.
