# Async Runtime Rollout
> **2026-03-10:** All synchronous loops have been eliminated; Node.js-like async infrastructure in place.
> See 2026-03-10-async-runtime-plan.md for details.

# FLM (Fastflow Language Model) Implementation Plan

## Goal
Implement FLM integration as a **local OpenAI-compatible Fastflow runtime** (NPU-optimized), matching the real usage contract in `flm-test-llama.py` and the design in `brainstorm.md

## Inputs and Alignment Source
- Design source: `brainstorm.md
- Behavioral source: `flm-test-llama.py`
- Existing runtime assumptions:
  - OpenAI SDK client
  - `base_url="http://127.0.0.1:52625/v1/"`
  - model name e.g. `llama3.2:1b`
  - optional tool-call loop (`assistant -> tool -> assistant`)

## Requirements and Constraints
- **REQ-001**: FLM must be documented and implemented as **Fastflow Language Model**, not “Foundation Language Model”.
- **REQ-002**: Integration must remain OpenAI-compatible (`chat.completions.create`).
- **REQ-003**: Tool-call execution must be deterministic and bounded.
- **REQ-004**: Endpoint and model failures must return actionable diagnostics.
- **CON-001**: Keep local-first runtime behavior; no cloud dependency required for default flow.
- **CON-002**: Preserve current project testing conventions (`pytest`).

## Implementation Phases

### Phase 1 — Documentation and Naming Canonicalization
**Goal:** Ensure all FLM references in this scope consistently mean Fastflow.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-001 | Verify FLM naming in `brainstorm.md is Fastflow and not Foundation | ✅ | 2026-03-08 |
| TASK-002 | Update `plan.md with concrete, executable Fastflow-aligned tasks | ✅ | 2026-03-08 |
| TASK-003 | Scan local FLM docs/config comments for “Foundation Language Model” references and replace with Fastflow wording (if found) | ✅ | 2026-03-08 |

### Phase 2 — Provider Contract Hardening
**Goal:** Define and validate FLM provider configuration contract.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-004 | Add/confirm FLM config schema keys: `base_url`, `default_model`, `timeout`, `max_retries`, optional `health_path`, `chat_path` | ✅ | 2026-03-08 |
| TASK-005 | Add config validation logic with explicit errors for missing required keys and invalid values | ✅ | 2026-03-08 |
| TASK-006 | Add unit tests for schema parsing/validation in `tests/test_flm_provider_config.py` | ✅ | 2026-03-08 |

### Phase 3 — OpenAI-Compatible Chat Adapter
**Goal:** Implement/verify adapter that mirrors `flm-test-llama.py` invocation pattern.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-007 | Create or update FLM provider adapter module under `src/` to call `openai.OpenAI(base_url=...)` | ✅ | 2026-03-08 |
| TASK-008 | Implement `chat.completions.create(...)` request builder with model/messages/max_tokens support | ✅ | 2026-03-08 |
| TASK-009 | Add adapter tests for non-tool terminal response in `tests/test_flm_chat_adapter.py` | ✅ | 2026-03-08 |

### Phase 4 — Deterministic Tool-Call Loop
**Goal:** Standardize tool-call flow with loop guard.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-010 | Implement assistant tool-call capture and canonical message append (assistant + tool) | ✅ | 2026-03-08 |
| TASK-011 | Add bounded loop control (`max_tool_iterations`) and explicit stop conditions | ✅ | 2026-03-08 |
| TASK-012 | Add tests in `tests/test_flm_tool_loop.py` for tool-loop success path and guard-trigger path | ✅ | 2026-03-08 |

### Phase 5 — Reliability and Observability
**Goal:** Provide clear runtime failure handling and diagnostics.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-013 | Implement endpoint reachability and model-availability checks with actionable error text | ✅ | 2026-03-08 |
| TASK-014 | Add structured diagnostics for malformed tool calls and request failures | ✅ | 2026-03-08 |
| TASK-015 | Add tests in `tests/test_flm_runtime_errors.py` for endpoint/model/tool payload failure scenarios | ✅ | 2026-03-08 |

### Phase 6 — Verification and Regression Safety
**Goal:** Confirm FLM path works and does not regress existing suite.

| Task | Description | Completed | Date |
|------|-------------|-----------|------|
| TASK-016 | Run FLM-focused tests: `pytest tests/test_flm_* -q` | ✅ | 2026-03-08 |
| TASK-017 | Run full test suite: `pytest -q` | ✅ | 2026-03-08 |
| TASK-018 | Update plan/design docs with final implementation notes and closure status | ✅ | 2026-03-08 |

## Acceptance Criteria
- **AC-001**: FLM naming is canonicalized to Fastflow in plan/design docs and nearby FLM references.
- **AC-002**: FLM provider config validates required fields with deterministic error messages.
- **AC-003**: Chat completions work with OpenAI SDK against FLM base URL contract.
- **AC-004**: Tool-call loop is deterministic, bounded, and test-covered.
- **AC-005**: Endpoint/model/payload failures are observable and actionable.
- **AC-006**: FLM-focused tests and full project tests pass.

## Risks and Assumptions
- **RISK-001**: Fastflow runtime API compatibility may vary by build/version.
- **RISK-002**: Local NPU runtime startup latency may cause false-negative health checks if timeout too low.
- **ASSUMPTION-001**: FLM runtime exposes OpenAI-compatible `/v1` endpoints.
- **ASSUMPTION-002**: Existing provider infrastructure can host a dedicated FLM adapter without breaking current providers.

## Dependencies
- **DEP-001**: `openai` Python SDK availability in runtime environment.
- **DEP-002**: Local Fastflow service reachable at configured base URL.
- **DEP-003**: Existing project pytest infrastructure for automated verification.

## Future Enhancements
- Add `/models` capability probe and model auto-selection logic.
- Add streaming response handling for long generation flows.
- Add configurable provider fallback chain (FLM -> local alt provider -> cloud).
- Add NPU-focused latency/throughput benchmark harness.