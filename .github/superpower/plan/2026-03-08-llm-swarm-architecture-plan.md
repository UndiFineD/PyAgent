# Async Runtime Rollout
> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.
> See 2026-03-10-async-runtime-plan.md for details.

# PyAgent Implementation Plan — LLM Context Consolidation, Plugins, P2P CRDT, and Security

**Goal:** Implement the approved design (LLM context consolidation 
  + hybrid LLM security + P2P CRDT swarm + plugin validation) 
  and migrate the repository layout to a clean modular architecture.

**Architecture:** Layered repo with `core/`, `agents/`, `interfaces/`, `tools/`, `plugins/`, 
  Rust high-performance cores in `rust_core/`, P2P via Rust libp2p + Automerge CRDT, 
  and a Rust `security` module for inline encryption and monthly key rotation.

**Tech stack:**
- Python 3.11+
- pytest for tests
- Rust (existing `rust_core/` → add crates)
- Automerge-rs (or similar) for CRDT
- libp2p Rust crate for P2P
- Rust crypto crates (ring, hpke/age) for key ops

---

## High-level phases (each broken into TDD tasks)

- Phase A — Repo reorganization & scaffolding
- Phase B — LLM context consolidation script
- Phase C — Plugins framework & validator
- Phase D — P2P CRDT Rust integration + Python bridge
- Phase E — Rust Security core (encryption + key rotation) + Python integration
- Phase F — CI, docs, and migration verification

Each task follows the TDD pattern: 
→ write failing test 
→ run test (fail) 
→ implement minimal code 
→ run test (pass). 
Exact file paths, commands, and expected outputs are provided per task.

---

## Phase A — Repo reorganization & scaffolding

Task A1: Add top-level scaffolding for new layout

- Step 1: Write failing test
  - File: `tests/test_repo_layout_scaffold.py`
- Step 2: Run test (expected FAIL)
  - Command: `pytest tests/test_repo_layout_scaffold.py::test_new_layout_dirs_exist -q`
- Step 3: Implement minimal scaffold CLI
  - File: `scripts/scaffold_new_layout.py`
  - Behavior: create directories `core`, `agents`, `interfaces`, `tools`, `plugins` (non-destructive)
- Step 4: Run test expecting PASS after running scaffold
  - Commands:
    ```powershell
    python scripts/scaffold_new_layout.py
    pytest tests/test_repo_layout_scaffold.py::test_new_layout_dirs_exist -q
    ```

Task A2: Dry-run move strategy

- Create `scripts/dryrun_move.py` to list proposed moves (no file changes).
- Test `tests/test_dryrun_lists_moves.py` ensures mapping output exists.

---

## Phase B — LLM context consolidation script

Task B1: Test for consolidation script existence
- File: `tests/test_consolidate_script_exists.py` (initially fails)

Task B2: Implement consolidation script
- File: `scripts/consolidate_llm_context.py`
- Minimal behavior: produce `llms.txt` and `llms-architecture.txt` 
  from `docs/architecture/` files; write `consolidation_report.txt`.

Task B3: Unit test parsing and output
- File: `tests/test_consolidate_parses_architecture.py`

---

## Phase C — Plugins framework & validator

Task C1: Add `BasePlugin` and tests
- File: `plugins/base.py`
- Test: `tests/test_plugins_base.py`

Task C2: Implement `PluginValidatorCore`
- File: `core/plugin_validator.py`
- Test: `tests/test_plugin_validator.py` (verify BasePlugin subclasses accepted/rejected)

Task C3: Security static checks (AST)
- File: `core/plugin_security.py` (AST heuristics)
- Test: `tests/test_plugin_security_ast.py`

Task C4: Dynamic tool wrapping for LLM
- File: `core/tool_wrappers.py`
- Test: `tests/test_plugin_tool_wrap.py`

---

## Phase D — P2P CRDT Rust integration + Python bridge

Task D1: Rust crate for P2P & CRDT
- Path: `rust_core/p2p` (new crate)
- Test: `tests/test_rust_p2p_binary.py` expecting a CLI binary (minimal `--version`)

Task D2: Automerge-backed state in Rust
- Expose a small CLI or FFI that accepts JSON patches and returns merged JSON
- Test: `tests/test_crdt_merge.py` calls binary and checks merge result

Task D3: Python bridge
- File: `core/crdt_bridge.py` which invokes rust binary
- Test: `tests/test_crdt_bridge.py`

---

## Phase E — Rust Security core (encryption + key rotation)

Task E1: Rust security module skeleton
- Path: `rust_core/security`
- Test: `tests/test_rust_security_binary.py` expecting `encrypt`/`decrypt` CLI

Task E2: Key rotation scheduler (monthly)
- Expose `rotate_keys` CLI for tests (simulate rotation)
- Test: `tests/test_key_rotation.py`

Task E3: Integrate with Python `StateTransaction`
- Bridge: `core/security_bridge.py`
- Test: `tests/test_statetransaction_encryption.py` ensures persisted data is encrypted

---

## Phase F — CI, docs, and migration verification

Task F1: CI workflow
- File: `.github/workflows/superpower-plan-check.yml` to run pytest on Windows/Ubuntu

Task F2: Migration dry-run & approval
- Script: `scripts/move_src_and_scripts_dryrun.py` → `migration_plan.json`
- Test: `tests/test_dryrun_outputs_plan.py`

---

## Verification / Acceptance criteria

- All Python tests pass via `pytest -q`.
- `rust_core` crates build with `cargo build`.
- Consolidation script produces `llms.txt` and `llms-architecture.txt` from `docs/architecture/` files.
- Plugin validator rejects a known-bad plugin and accepts a known-good plugin.
- CRDT bridge merges simple concurrent edits in test cases.
- Security core encrypts/decrypts a sample payload and performs a simulated rotation.
- Migration dry-run outputs a precise move mapping; no automatic file moves occur without explicit approval.

## How to run checks locally

1) Run Python tests
```powershell
pip install -r requirements.txt
pytest -q
```

2) Build Rust crates (developer machine)
```powershell
cd rust_core/p2p
cargo build
cd ../security
cargo build
```

3) Run consolidation script manually
```powershell
python scripts/consolidate_llm_context.py
```

---

## Files to be created/edited (when approved to implement)

- plan file: `.github/superpower/plan/2026-03-08-llm-swarm-architecture-plan.md` (this file)
- tests under `tests/` as specified per task
- scripts under `scripts/` (scaffold, dryrun, consolidate, move dryrun)
- new modules under `plugins/`, `core/` (validator, wrappers, crdt_bridge, security_bridge)
- rust crates under `rust_core/p2p` and `rust_core/security`
- CI workflow `.github/workflows/superpower-plan-check.yml`

---

## checklist (status: pending)

- Phase A — Repo reorganization & scaffolding
- Phase B — LLM context consolidation script
- Phase C — Plugins framework & validator
- Phase D — P2P CRDT Rust integration + Python bridge
- Phase E — Rust Security core (encryption + key rotation)
- Phase F — CI, docs, and migration verification
