# PyAgent — Master Agent Memory

_Last updated: 2026-03-20_

---

## Standing Policy — Branch Isolation

- One `prjNNN` workstream maps to one branch. Project work must not piggyback on the active branch of another project.
- `@0master` assigns or validates the expected branch during project kickoff and ensures `@1project` records that branch, the scope boundary, and the git handoff rule in the project overview.
- `@9git` is expected to reject mixed-project changes, inherited branches, and broad staging guidance for project work.
- When branch hygiene fails, `@0master` owns the correction loop: update the governing guidance, return the task to the agent that owns the project boundary, and do not normalize the failure as an accepted workflow.

## Standing Policy — Project Numbering Ownership

- `@0master` owns `prjNNN` allocation, validation, and continuity tracking.
- Project numbering is part of the project boundary. A project is not fully defined until the assigned `prjNNN`, project folder, and expected branch agree.
- `@1project` must consume the identifier assigned by `@0master`. It must not invent, renumber, or resolve ambiguity on its own.
- Do not reuse old numbers or skip numbers casually. If a number is reserved, retired, skipped, or corrected, record the reason here before downstream handoff.
- If numbering is missing, conflicting, or ambiguous, stop the workflow and send the task back through `@0master` before project setup continues.

## Project Numbering Tracking

- Latest confirmed project folder in `docs/project/`: `prj0000042`.
- Project folder numbering migrated from 3-digit (`prj001`-`prj038`) to 7-digit (`prj0000001`-`prj0000042`).
- Legacy duplicate groups were resolved by assigning unique 7-digit identifiers during migration.
- Next `prjNNN` to allocate: `prj0000043` (validate against `docs/project/` inventory before assignment).

## Learning Loop — Branch Hygiene

- Record branch hygiene failures in `docs/agents/9git.memory.md` with: date, project, observed branch, failure type, and required fix.
- Reflect recurring failures or policy changes here so future coordinators enforce the updated workflow earlier.
- Shared-branch history under unrelated projects is a warning signal, not an exception path.

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
