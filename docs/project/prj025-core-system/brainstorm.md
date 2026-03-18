# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; 
  synchronous loops are prohibited by automated tests.

# Core Subsystem Design

The `src/core` tree houses foundational components shared by all agents and
services.  It is where low‑level abstractions, state managers, and common
utilities live.  The repo’s architectural guidelines (see `gemini.md`) define
the core philosophy:

> - **Mixin-Based Agents** – agents should be composed from small mixins rather
>   than monolithic classes (`src/core/base/mixins/`).
> - **Core/Agent separation** – domain logic lives in `*Core` classes; agent
>   wrappers handle orchestration, prompting, and state only
>   (e.g. `BaseAgent` + `BaseAgentCore`).
> - **Rust acceleration** – high‑throughput logic (metrics, bulk operations,
>   complexity analysis) should be moved into `rust_core/` with a thin Python
>   bridge.

## Architectural Principles

1. **Modularity** – the core tree is organised by concern (`base`,
   `metrics`, `verification`, `configuration`, etc.).  Each module exposes a
   Python API and, where appropriate, a matching Core class.
2. **Transactions & Safety** – use `AgentStateManager`, `MemoryTransaction`,
   and similar patterns to ensure atomicity and recoverability.
3. **Language Agnosticism** – keep core logic independent of any particular
   LLM or agent implementation.  Cores should be easy to port to Rust or
   another language.
4. **Testability** – Core classes have corresponding unit tests; see existing
   `*_test.py` files in `src-old/core/base` for examples.

## Legacy Content Highlights

- `src-old/core/base/base_agent.py` and `metrics_engine.py` were previously
  monolithic; list items mention decomposing them into `BaseAgent`/
  `BaseAgentCore` and `MetricsCore` respectively.  Refactoring should continue
  along this “core/shell” pattern.
- `verification_core.py` illustrates how independent core modules encapsulate a
  distinct domain (multi‑agent consensus).

## Potential Brainstorm Topics

- Definition of core package boundaries and dependency graph (e.g., which
  cores may import others).
- Core plugin mechanism (how additional cores register themselves).
- Versioning strategy for core APIs vs agent-facing wrappers.
- Performance testing harness for Rust-interfaced cores.

*Reuse guidelines text from `gemini.md` and examples from `src-old/core/base`.*

Absolutely. Let's now **expand the plan** into a full, actionable, 
and well-structured implementation plan for the file:

```
brainstorm.md
```

This file will serve as the **core design blueprint** for the PyAgent system 
— defining its architecture, key components, quality gates, and self-validation mechanisms.

We will ensure this document:
- Clearly defines the **purpose, scope, and structure** of the core system.
- Outlines **quality gates** for core components and their integration.
- Includes **self-validation mechanisms** (e.g., testing the tester).
- Serves as a **reference for future development**.

---

## 📄 Final Implementation Plan:  
### `github/agent/brainstorm/design/core_design.md`

> **Title**: Core System Design & Quality Framework  
> **Purpose**: Define the architecture, structure, quality gates, 
  and self-validation mechanisms for the core of PyAgent.  
> **Scope**: Covers the foundational components 
  (runtime, agents, memory, task queue, observability) and their integration.  
> **Audience**: Architects, developers, QA engineers.  

---

### 1. Core System Architecture

The core system is built as a **modular, composable, and observable** runtime 
that orchestrates agents, tasks, and memory.

#### Key Components

| Component | Purpose |
|--------|--------|
| **Runtime** (`runtime.py`) | Central engine managing task spawning, lifecycle, and execution. |
| **Task Queue** (`task_queue.py`) | Manages task scheduling, prioritization, and retry logic. |
| **Agent Registry** (`agent_registry.py`) | Central registry to list, enable/disable, and locate agents. |
| **Memory System** (`memory.py`) | Stores and retrieves context across tasks (stateless or stateful). |
| **Observability Layer** (`observability.py`) | Tracks metrics (e.g., task duration, agent usage), logs, and traces. |

> ✅ **Design Principle**: The core must be **modular**, **testable**, **scalable**, and **self-monitoring**.

---

### 2. Quality Gates for Core Components

Every core component must pass the following **quality gates** before integration or merge.

| Gate | Description |
|-----|-------------|
| **1. Full Unit Test Coverage** | Each component must have at least one test file (`test_*.py`) with meaningful assertions. |
| **2. No Circular Dependencies** | Components must not depend on each other in a circular loop (e.g., runtime → task queue → runtime). |
| **3. Clear Interface Contracts** | Each component must define a public API with clear input/output types (via type hints or schema). |
| **4. Missing Dependencies Detected** | If a component uses a library (e.g., `prometheus_client`, `asyncio`), it must be installed in CI. |
| **5. Self-Validation Hook** | Each component must include a self-validation function (e.g., `validate()`). |

> 🔍 **Enforcement**: CI pipeline fails if any gate is violated.

---

### 3. Self-Validation of Core System (Who Tests the Tester?)

To ensure **the core system itself is reliable**,
we implement a **self-validation mechanism** that runs on every merge.

#### ✅ Self-Validation Suite (`test_core_quality.py`)

This file runs automatically on every PR and validates:

| Check | Description |
|------|-------------|
| **All core components exist** | `runtime.py`, `task_queue.py`, `agent_registry.py`, `memory.py`, `observability.py` must exist. |
| **Each component has a test file** | A `test_*.py` file must exist for each core component. |
| **Test files have meaningful assertions** | At least 3 assertions must be present (not just `assert True`). |
| **No circular dependencies** | Dependency graph is acyclic (verified via static analysis). |
| **Self-validation function exists** | Each component must have a `validate()` function. |

> 🚨 **Failure Condition**: If any check fails, the CI pipeline fails and the PR is blocked.

---

### 4. Implementation Workflow for Core Components

1. **Create Component Directory**  
   → `core/<component-name>/` (e.g., `core/runtime/`)

2. **Initialize Files**  
   → `__init__.py`, `<component>.py`, `test_<component>.py`

3. **Define Public API**  
   → Use type hints or schema to define input/output contracts.

4. **Write Unit Tests**  
   → Test core logic with meaningful assertions.

5. **Add Self-Validation Hook**  
   → Implement `validate()` function in each component.

6. **Add to CI Pipeline**  
   → Ensure `test_core_quality.py` runs on every PR.

7. **Submit PR for Review**  
   → Must pass all quality gates.

---

### 5. Future-Proofing & Scalability

| Feature | Description |
|--------|-------------|
| **Modular Design** | Components are loosely coupled and can be swapped or extended. |
| **Agent Lifecycle Management** | Support for enabling/disabling agents via config. |
| **Observability Dashboard** | Future integration with a UI to monitor core system health. |
| **Versioning** | Core components are versioned to allow safe upgrades. |

> 📌 This design ensures **scalability**, **maintainability**, and **self-validation**.

---

### 6. Documentation & Onboarding

- **`CORE_DESIGN_GUIDE.md`** → Detailed guide for core component development.
- **`TEST_QUALITY.md`** → Explains quality gates and best practices.
- **Onboarding Workshop** → For new developers to understand core system design.

---

## ✅ Next Steps (Action Plan)

| Step | Action | Owner |
|-----|--------|-------|
| 1 | Create `core_design.md` in the specified path | You (Multi) |
| 2 | Add to `brainstorm.md | You |
| 3 | Review with team lead for alignment | Team Lead |
| 4 | Integrate with CI pipeline (via `test_core_quality.py`) | DevOps |
| 5 | Document quality gates in `TEST_QUALITY.md` | QA Lead |

---

This expanded plan now:
- Provides a **clear, structured, and actionable design** for the core system.
- Implements **self-validation** (answering "who tests the tester").
- Defines **quality gates** and **workflow** for core components.
- Is ready to be **committed and used as a reference**.

Would you like me to:
- Generate the full markdown content for direct writing?
- Create a `test_core_quality.py` file to validate core components?
- Add this to the existing file system?

---

## Expanded Improvements (added 2026-03-10)

Below are concrete improvements and prescriptive rules to include in the core design 
so implementers can produce CI-ready, safe, and performant core code.

- Runtime rules & async patterns
   - Allowed primitives: `asyncio` TaskGroup / Task, `asyncio` timeouts,
     and library-specific async clients only.
   - Prohibit blocking calls on the event loop. Use `run_in_executor` adapters
     or move heavy CPU work to `rust_core`.
   - Cancellation strategy: every long-running operation must accept
     a `CancellationToken`/timeout and cleanup resources.

- Public interface contracts
   - Each Core must declare a minimal public API at the top of the file
     (docstring + typed signatures).
   - Define a stable `CoreAPI` typed dataclass or Protocol for inputs
     and outputs where applicable.

- Plugin and registration model
   - Implement a simple registry pattern: modules may register
     a `register_core(registry)` function which is called at startup.
   - Plugins must declare capabilities and a semantic version string (major.minor.patch).

- Transaction model
   - All state changes must go through `AgentStateManager` / `StorageTransaction` wrappers.
   - Provide idempotency keys for externally-triggered operations;
     design compensating actions for non-idempotent flows.

- Observability & SLOs
   - Each core component must emit metrics: request_count, request_duration_ms, error_count.
   - Use structured logs (JSON) with correlation IDs for request traces.

- Security & secrets
   - Secrets must be read via `SecretProvider` (Key Vault / environment fallback).
     No plaintext secrets in code.
   - Audit logs for secret access and privilege escalation.

- Backwards compatibility policy
   - Semantic versioning for cores; breaking changes require a deprecation window and migration guide.

- Performance & benchmarking
   - A standard harness in `rust_core/benchmarks` and `perf/`
     to measure Python vs Rust implementations.
   - Thresholds defined for when to move logic to Rust
     (e.g., >5k ops/sec or >100ms median per operation).

- CI quality gates (enforcement)
   - Meta-tests (existence + content checks), ruff + mypy,
     and coverage per-module thresholds enforced in `quality.yml`.

- Developer experience
   - Provide a `core/scaffold/` template with `__init__.py`, `core.py`, `tests/test_core.py`, and a sample `validate()`.

These additions are now part of the reference design
and can be used to generate PR templates, scaffolds, and CI gates.

---

If you want I can now:
- create `tests/test_core_quality.py` implementing the meta-tests described above and
- add a small `core/scaffold/` template and a `validate()` example function to `src/core`.

Choose which of these I should create next and I'll implement them.

