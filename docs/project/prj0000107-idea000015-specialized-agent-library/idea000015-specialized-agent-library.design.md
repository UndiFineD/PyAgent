# idea000015-specialized-agent-library - Design

_Status: DONE_
_Designer: @3design | Updated: 2026-03-30_

## Selected Option
Option B - Hybrid Adapter Layer (manifest-defined specializations + runtime adapters over universal shell primitives).

Rationale:
1. Delivers explicit specialized-agent-library contracts without immediate class proliferation.
2. Reuses existing universal shell/router infrastructure while preserving core-agent separation.
3. Supports incremental rollout with policy and parity gates, minimizing migration blast radius.

Design lock:
- This design locks Option B for v1 implementation.
- Option A (full specialized class library) is deferred until adapter contracts prove stable.
- Option C (universal-only capability packs) is rejected for v1 because it under-serves specialized-library intent.

## Architecture
### High-level flow
1. Capability metadata is loaded from specialization manifests.
2. `SpecializationRegistry` validates and resolves specialization descriptors by policy/version.
3. `SpecializedAgentAdapter` maps descriptor + runtime context into a normalized shell execution request.
4. Universal shell executes orchestration while delegating domain behavior to specialization-bound `*Core` contracts.
5. `CapabilityPolicyEnforcer` validates allowlisted capability and permission boundaries before tool execution.
6. `SpecializationTelemetryBridge` emits redacted provenance and contract-parity telemetry.
7. If manifest/adapter validation fails, `AdapterFallbackPolicy` applies fail-closed deterministic fallback.

### Components and responsibilities
| Component | Responsibility | Inputs | Outputs |
|---|---|---|---|
| `SpecializationRegistry` | Load, validate, and version specialization descriptors | Manifest bundle + policy version | `SpecializationDescriptor` |
| `SpecializedAgentAdapter` | Translate descriptor into runtime orchestration contract | Descriptor + request context | `ShellExecutionRequest` |
| `CapabilityPolicyEnforcer` | Enforce capability allowlist and deny-by-default policy | Shell request + policy matrix | `PolicyDecision` |
| `SpecializedCoreBinding` | Bind adapter request to corresponding `*Core` interface | Shell request + core registry | `CoreInvocationPlan` |
| `AdapterFallbackPolicy` | Fail-closed handling for schema, timeout, or policy violations | Failure reason + context | Safe fallback decision |
| `SpecializationTelemetryBridge` | Emit redacted provenance, parity, and latency signals | Decision record + timing context | Structured telemetry envelope |

### Architecture constraints
1. Agent classes remain orchestration-thin; domain logic stays in `*Core` interfaces.
2. No dynamic capability may execute without explicit policy allowlist match.
3. Adapter contracts are versioned and backward-compatible within one minor version window.
4. Fallback is fail-closed and deterministic for any invalid adapter/manifest state.
5. Every specialization decision path must emit a correlation-linked telemetry record.

## Interfaces & Contracts
### Interface contracts
| Interface ID | Interface | Contract summary | Test hook |
|---|---|---|---|
| IFACE-SAL-001 | `SpecializationRegistry.resolve(specialization_id, policy_version) -> SpecializationDescriptor` | Returns schema-valid descriptor or explicit typed failure with reason code | AC-SAL-001, AC-SAL-007 |
| IFACE-SAL-002 | `SpecializedAgentAdapter.build_request(descriptor, runtime_context) -> ShellExecutionRequest` | Deterministic mapping from manifest descriptor to shell request payload | AC-SAL-002, AC-SAL-008 |
| IFACE-SAL-003 | `CapabilityPolicyEnforcer.authorize(shell_request, actor_context) -> PolicyDecision` | Deny-by-default authorization with immutable policy evidence fields | AC-SAL-003 |
| IFACE-SAL-004 | `SpecializedCoreBinding.plan(shell_request) -> CoreInvocationPlan` | Binds to explicit `*Core` contract and rejects unresolved core targets | AC-SAL-004 |
| IFACE-SAL-005 | `AdapterFallbackPolicy.apply(failure_reason, runtime_context) -> FallbackDecision` | Fail-closed fallback with deterministic route and reason taxonomy | AC-SAL-005 |
| IFACE-SAL-006 | `SpecializationTelemetryBridge.emit(decision_record) -> None` | Emits redacted provenance with correlation and contract-version markers | AC-SAL-006 |

### Data contracts
| Data shape | Required fields | Notes |
|---|---|---|
| `SpecializationDescriptor` | `specialization_id`, `adapter_contract_version`, `core_contract`, `capability_set`, `policy_profile`, `telemetry_profile` | Loaded from validated manifest source only |
| `ShellExecutionRequest` | `request_id`, `specialization_id`, `capability_action`, `core_target`, `policy_profile`, `correlation_id` | Canonical adapter output for shell orchestration |
| `PolicyDecision` | `authorized`, `matched_rules`, `deny_reason`, `policy_version` | `deny_reason` required when `authorized=false` |
| `SpecializationDecisionRecord` | `request_id`, `specialization_id`, `adapter_contract_version`, `final_outcome`, `fallback_used`, `policy_version`, `correlation_id` | Primary provenance payload for audits and parity checks |

### Compatibility and versioning
- Contract version key: `adapter_contract_version` using semantic versioning.
- Breaking adapter changes require ADR update and migration notes before activation.
- Registry must reject descriptors with unsupported major contract versions.

## Non-Functional Requirements
- Performance:
	- Adapter build path p95 <= 25 ms (excluding downstream model/tool execution).
	- Manifest resolution p95 <= 10 ms with warmed cache.
	- Fallback invocation overhead <= 5 ms.
- Security:
	- Capability execution is deny-by-default with explicit allowlist enforcement.
	- Telemetry is redacted and excludes raw prompt/tool secrets.
	- Policy and contract version fields are immutable in emitted provenance.
- Reliability:
	- Unsupported schema/version/policy states fail closed.
	- Deterministic fallback must be available without external dependencies.
- Testability:
	- Each interface has a contract test hook with deterministic fixtures.
	- Adapter parity tests compare manifest intent vs runtime request output.

## Acceptance Criteria
| AC ID | Requirement | Verification hook |
|---|---|---|
| AC-SAL-001 | Registry resolves valid descriptors and rejects invalid schema/version with typed reason | Registry schema and version compatibility tests |
| AC-SAL-002 | Adapter mapping is deterministic for identical descriptor/context input | Deterministic adapter replay tests |
| AC-SAL-003 | Unauthorized capabilities are denied by default with policy evidence fields | Authorization matrix tests (allow + deny) |
| AC-SAL-004 | Core binding rejects unresolved `*Core` targets and accepts valid bindings | Core binding contract tests |
| AC-SAL-005 | Adapter fallback triggers on schema/timeouts/policy faults with fail-closed outcome | Fault-injection fallback tests |
| AC-SAL-006 | Telemetry payload includes required redacted provenance fields and correlation IDs | Telemetry schema + redaction tests |
| AC-SAL-007 | Descriptor major-version incompatibility is blocked before execution | Version gate tests |
| AC-SAL-008 | Manifest intent and built shell request remain parity-consistent across releases | Manifest-to-request parity tests |

## Interface-to-Task Traceability
| Planned Task ID (@4plan) | Interface/Contract | Delivery expectation |
|---|---|---|
| T-SAL-01 | IFACE-SAL-001 | Implement registry loader, schema validator, and version gate logic |
| T-SAL-02 | IFACE-SAL-002 | Implement deterministic adapter request builder |
| T-SAL-03 | IFACE-SAL-003 | Implement capability-policy matrix and deny-by-default enforcement |
| T-SAL-04 | IFACE-SAL-004 | Implement specialization-to-`*Core` binding planner |
| T-SAL-05 | IFACE-SAL-005 | Implement deterministic fail-closed fallback policy |
| T-SAL-06 | IFACE-SAL-006 | Implement specialization telemetry bridge with redaction controls |
| T-SAL-07 | AC-SAL-001, AC-SAL-007 | Build descriptor schema/version compatibility tests |
| T-SAL-08 | AC-SAL-002, AC-SAL-008 | Build adapter determinism and parity test suite |
| T-SAL-09 | AC-SAL-003, AC-SAL-005 | Build policy denial and fallback fault-injection tests |
| T-SAL-10 | NFR performance hooks | Add adapter latency metrics and threshold alert checks |

## ADR Impact
- New ADR required to lock the hybrid adapter architecture and versioned adapter-contract policy.
- ADR target: `docs/architecture/adr/0005-specialized-agent-library-hybrid-adapter-runtime.md`.
- ADR scope includes decision rationale, rejected alternatives, migration constraints, and validation gates.

## Open Questions
Resolved for @4plan handoff readiness:
1. Minimal contract boundary is adapter request schema + policy decision + core binding contract.
2. Source of truth is a versioned specialization manifest registry validated before runtime mapping.
3. Adapter versioning uses semantic contract version with major-version rejection gate.
4. Mandatory telemetry fields are request/specialization IDs, contract/policy versions, outcome, fallback flag, and correlation ID.

No blocking open design questions remain for decomposition.