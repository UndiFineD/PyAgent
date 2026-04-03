# Current Memory - 3design

## Metadata
- agent: @3design
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-04-03
- rollover: At new project start, append this file's entries to history.3design.memory.md in chronological order, then clear Entries.

## Entries
- task_id: prj0000116-rust-criterion-benchmarks
	state: DONE
	selected_design_path: Option B (minimal Rust Criterion harness plus lightweight CI smoke benchmark)
	assumptions:
		- Initial scope targets one or two bounded pure functions in `rust_core` stats modules.
		- CI benchmark lane is smoke-only in v1 (no regression-threshold enforcement).
		- `cargo bench` remains the canonical command entrypoint for local validation.
	interface_contract_notes:
		- IFACE-BENCH-001 benchmark file and deterministic naming contract.
		- IFACE-BENCH-002 local command entrypoint contract (`cargo bench --bench stats_baseline`).
		- IFACE-BENCH-003 CI smoke command contract (`--noplot`, exit-success gate).
		- IFACE-BENCH-004 artifact contract (`rust_core/target/criterion/**`).
		- IFACE-BENCH-005 minimal scope boundary contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000116-rust-criterion-benchmarks/rust-criterion-benchmarks.design.md
		chunked_artifacts: none
		adr_artifact: none
	lesson:
		Pattern: Benchmark governance lands cleanly when CI introduces harness-health smoke checks before any threshold enforcement.
		Root cause: Immediate threshold gating in early benchmark adoption creates flakiness and slows rollout.
		Prevention: Lock smoke-only pass criteria, explicit naming contracts, and AC/IFACE traceability in the design artifact.
		First seen: 2026-04-03
		Seen in: prj0000116-rust-criterion-benchmarks
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000110-idea000004-quality-workflow-branch-trigger
	state: DONE
	selected_design_path: Option B (targeted project-branch governance gate with main-focused full-suite triggers retained)
	assumptions:
		- Existing `ci.yml` and `security.yml` remain authoritative full-suite workflows centered on `main`.
		- Governance gate reuses canonical policy entrypoints (`scripts/enforce_branch.py` and docs policy pytest selector).
		- This lane stays docs-scoped with no production workflow code edits by `@3design`.
	interface_contract_notes:
		- IFACE-QWB-001 project branch trigger contract.
		- IFACE-QWB-002 governance execution contract.
		- IFACE-QWB-003 docs policy validation contract.
		- IFACE-QWB-004 required-check identity contract.
		- IFACE-QWB-005 scope boundary contract.
		- IFACE-QWB-006 least-privilege permissions contract.
		- IFACE-QWB-007 downstream handoff traceability contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000110-idea000004-quality-workflow-branch-trigger/idea000004-quality-workflow-branch-trigger.design.md
		chunked_artifacts: none
		adr_artifact: none
	lesson:
		Pattern: Governance-trigger designs stay executable when they separate lightweight branch-policy gates from full quality suites and encode required-check identity as an explicit contract.
		Root cause: Branch-trigger requests can drift into noisy CI expansion when gate scope and required-check semantics are not specified.
		Prevention: Define trigger boundary, fail-closed governance checks, and AC/IFACE traceability before planning.
		First seen: 2026-04-01
		Seen in: prj0000110-idea000004-quality-workflow-branch-trigger
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000109-idea000002-missing-compose-dockerfile
	state: DONE
	selected_design_path: Option B (incremental governance hardening around already-fixed compose Dockerfile path contract)
	assumptions:
		- `deploy/compose.yaml` and `deploy/Dockerfile.pyagent` remain the current runtime contract baseline.
		- This lane remains documentation-and-governance scoped with no deploy runtime edits.
		- Compose topology consolidation is deferred to the dedicated consolidation lane.
	interface_contract_notes:
		- IFACE-DC-001 compose file to Dockerfile path contract.
		- IFACE-DC-002 defect-lane scope guard contract.
		- IFACE-DC-003 regression signal contract.
		- IFACE-DC-004 handoff contract for @4plan traceability.
		- IFACE-DC-005 testability contract for @5test risk mapping.
		- IFACE-DC-006 non-goal boundary contract (no consolidation in this lane).
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000109-idea000002-missing-compose-dockerfile/idea000002-missing-compose-dockerfile.design.md
		chunked_artifacts: none
		adr_artifact: none
	lesson:
		Pattern: Defect-lane design artifacts stay actionable when they explicitly lock non-goals and map interfaces to planned task IDs.
		Root cause: Stale or already-fixed defect lanes can drift into unnecessary implementation scope without explicit boundary contracts.
		Prevention: Encode non-goal boundaries, AC IDs, and interface-to-task traceability directly in the canonical design artifact before handoff.
		First seen: 2026-03-31
		Seen in: prj0000109-idea000002-missing-compose-dockerfile
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000108-idea000019-crdt-python-ffi-bindings
	state: DONE
	selected_design_path: Option B (integrate CRDT FFI into existing rust_core PyO3 module with migration fallback gate)
	assumptions:
		- Existing rust_core PyO3/maturin path remains the canonical extension delivery channel.
		- Python merge facade in src/core/crdt_bridge.py remains contract-stable through migration.
		- Subprocess path is temporary fallback only and removed after parity/performance gates pass.
	interface_contract_notes:
		- IFACE-CRDT-001 stable Python merge facade and routing gate contract.
		- IFACE-CRDT-002 PyO3 boundary validation and typed response contract.
		- IFACE-CRDT-003 canonical payload codec round-trip equivalence contract.
		- IFACE-CRDT-004 deterministic CRDT merge engine contract.
		- IFACE-CRDT-005 Rust-to-Python error taxonomy mapping contract.
		- IFACE-CRDT-006 redacted observability contract for parity/latency outcomes.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000108-idea000019-crdt-python-ffi-bindings/idea000019-crdt-python-ffi-bindings.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0006-crdt-python-ffi-in-rust-core.md
	lesson:
		Pattern: FFI migration designs stay implementable when boundary contracts and parity rollback gates are defined before planning.
		Root cause: CRDT subprocess integrations accumulate latency and reliability risk when boundary contracts are implicit.
		Prevention: Lock Python facade, PyO3 boundary, codec, error taxonomy, and parity gates with AC IDs prior to @4plan handoff.
		First seen: 2026-03-31
		Seen in: prj0000108-idea000019-crdt-python-ffi-bindings
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000107-idea000015-specialized-agent-library
	state: DONE
	selected_design_path: Option B (hybrid specialization manifests + runtime adapters over universal shell)
	assumptions:
		- Specialization manifests are the authoritative source for adapter input contracts.
		- Runtime orchestration remains shell-driven while domain logic is bound through explicit `*Core` interfaces.
		- Policy allowlist and fail-closed fallback are mandatory release gates for specialization execution.
	interface_contract_notes:
		- IFACE-SAL-001 specialization registry schema/version resolution contract.
		- IFACE-SAL-002 deterministic manifest-to-shell adapter mapping contract.
		- IFACE-SAL-003 deny-by-default capability authorization contract.
		- IFACE-SAL-004 specialization-to-core binding contract.
		- IFACE-SAL-005 deterministic fail-closed fallback contract.
		- IFACE-SAL-006 redacted specialization telemetry contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000107-idea000015-specialized-agent-library/idea000015-specialized-agent-library.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0005-specialized-agent-library-hybrid-adapter-runtime.md
	lesson:
		Pattern: Hybrid specialization designs stay actionable when adapter contracts, policy gates, and parity hooks are defined together.
		Root cause: Specialized-agent intent can stall when manifests and runtime orchestration are not connected by explicit interface contracts.
		Prevention: Lock adapter, policy, and fallback interfaces with AC IDs and interface-to-task traceability before @4plan handoff.
		First seen: 2026-03-30
		Seen in: prj0000107-idea000015-specialized-agent-library
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000106-idea000080-smart-prompt-routing-system
	state: DONE
	selected_design_path: Option B (hybrid guardrails + semantic classifier + bounded deterministic tie-break)
	assumptions:
		- Deterministic guardrails retain absolute precedence over classifier/tie-break outcomes.
		- Route decisions are promoted from shadow to active mode only after parity and latency gates pass.
		- Existing deterministic path remains available as operational fallback.
	interface_contract_notes:
		- IFACE-SPR-001 routing facade contract for total decision coverage.
		- IFACE-SPR-002 guardrail precedence invariant.
		- IFACE-SPR-003 classifier confidence + schema contract.
		- IFACE-SPR-004 deterministic tie-break + timeout contract.
		- IFACE-SPR-005 fail-closed fallback contract.
		- IFACE-SPR-006 redacted provenance telemetry contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000106-idea000080-smart-prompt-routing-system/idea000080-smart-prompt-routing-system.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0004-smart-prompt-routing-hybrid-guardrails.md
	lesson:
		Pattern: Hybrid decision systems need explicit guardrail precedence and deterministic tie-break rules to stay testable.
		Root cause: Ambiguous prompt routing without staged control boundaries causes nondeterministic behavior and weak safety guarantees.
		Prevention: Enforce stage-order invariants, fixed tie-break determinism, and fail-closed fallback with provenance checks.
		First seen: 2026-03-30
		Seen in: prj0000106-idea000080-smart-prompt-routing-system
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000105-idea000016-mixin-architecture-base
	state: DONE
	selected_design_path: Option B (incremental migration with compatibility shims)
	assumptions:
		- Canonical base mixin namespace is introduced before broad host adoption.
		- Legacy shims are explicitly time-boxed to migration waves W1-W3.
		- @4plan will keep decomposition to roughly 10 code files and 10 test files as requested by workflow.
	interface_contract_notes:
		- IFACE-MX-001 canonical export determinism under src/core/base/mixins/.
		- IFACE-MX-002 host protocol requirements and validation hook contract.
		- IFACE-MX-003 legacy compatibility shim contract with deprecation signaling.
		- IFACE-MX-004 behavioral parity contract old vs canonical import paths.
		- IFACE-MX-005 shim expiry fail-closed governance gate.
		- IFACE-MX-006 migration observability event contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000105-idea000016-mixin-architecture-base/idea000016-mixin-architecture-base.design.md
		chunked_artifacts: none
	lesson:
		Pattern: Explicit AC IDs plus interface-to-task traceability in design artifacts reduces @4plan ambiguity and rework.
		Root cause: Prior workflow stalls happen when architecture contracts exist without executable decomposition mapping.
		Prevention: Always include AC table and IFACE-to-task mapping block before @4plan handoff.
		First seen: 2026-03-30
		Seen in: prj0000104-idea000014-processing; prj0000105-idea000016-mixin-architecture-base
		Recurrence count: 2
		Promotion status: Promoted to hard rule

- task_id: prj0000104-idea000014-processing
	state: DONE
	selected_design_path: Option A (`pyproject.toml` canonical + deterministic generated `requirements.txt`)
	assumptions:
		- CI parity gate is authoritative and pre-commit is fast feedback.
		- Existing requirements-based install paths remain supported.
		- Heavy optional dependency extras migration is deferred.
	interface_contract_notes:
		- IFACE-C1 generation contract defined for deterministic output.
		- IFACE-C2 parity check contract defined for local/CI enforcement.
		- IFACE-C3 install compatibility contract preserves existing flows.
		- IFACE-C4 parity test contract covers drift/nondeterminism.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000104-idea000014-processing/idea000014-processing.design.md
		chunked_artifacts: none
	lesson:
		Pattern: Design handoff quality improves when acceptance criteria and interface-to-task traceability are both explicit.
		Root cause: Prior handoffs can stall when interfaces are defined but not mapped to executable plan tasks.
		Prevention: Always include AC table with IDs and explicit IFACE-to-task mapping in the canonical design file.
		First seen: 2026-03-30
		Seen in: prj0000104-idea000014-processing
		Recurrence count: 1
		Promotion status: Candidate

