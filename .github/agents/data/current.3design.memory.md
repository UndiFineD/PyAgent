# Current Memory - 3design

## Metadata
- agent: @3design
- lifecycle: OPEN -> IN_PROGRESS -> DONE|BLOCKED
- updated_at: 2026-04-04
- rollover: At new project start, append this file's entries to history.3design.memory.md in chronological order, then clear Entries.

## Entries
- task_id: prj0000122-jwt-refresh-token-support
	state: DONE
	selected_design_path: Option A (API-key bootstrap + file-backed refresh-session store + opaque rotating refresh tokens + short-lived access JWTs)
	assumptions:
		- Phase one targets the current single-instance backend deployment shape.
		- `PYAGENT_API_KEY` is the only bootstrap credential for managed sessions in this slice.
		- Legacy direct API-key and direct bearer-JWT auth paths remain backward compatible.
	interface_contract_notes:
		- IFACE-JRT-001 bootstrap endpoint contract.
		- IFACE-JRT-002 access JWT claim contract.
		- IFACE-JRT-003 opaque refresh-token hashing contract.
		- IFACE-JRT-004 file-backed persistence contract.
		- IFACE-JRT-005 single-use rotation contract.
		- IFACE-JRT-006 logout revocation contract.
		- IFACE-JRT-007 HTTP compatibility contract.
		- IFACE-JRT-008 WebSocket handshake-only auth contract.
		- IFACE-JRT-009 short-TTL bounded revocation contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0008-backend-managed-refresh-sessions-for-jwt-renewal.md
	lesson:
		Pattern: Backend auth upgrades stay implementation-ready when bootstrap identity and persistence durability are resolved explicitly before planning.
		Root cause: Refresh-token projects stall when teams leave initial session creation or storage durability as follow-up questions.
		Prevention: Lock the bootstrap credential, persistence boundary, revocation semantics, and IFACE-to-task traceability in the canonical design artifact before @4plan handoff.
		First seen: 2026-04-04
		Seen in: prj0000122-jwt-refresh-token-support
		Recurrence count: 1
		Promotion status: Candidate

- task_id: prj0000124-llm-gateway
	state: DONE
	selected_design_path: Option C (Hybrid Split-Plane Gateway: Python control plane + Python-implemented Rust-ready data-plane contracts)
	assumptions:
		- Phase one remains in-process and prioritizes contract stability over deployment topology expansion.
		- Existing provider/routing/resilience/back-end modules are wrapped via explicit gateway interfaces instead of rewritten.
		- Fail-closed behavior is mandatory at policy/auth/budget/tool gates.
	interface_contract_notes:
		- IFACE-GW-001 GatewayCore orchestration contract.
		- IFACE-GW-002 GatewayPolicyEngine pre/post/tool policy contract.
		- IFACE-GW-003 GatewayRouter route-plan contract.
		- IFACE-GW-004 ProviderRuntimeAdapter execution contract.
		- IFACE-GW-005 GatewayBudgetManager reserve/commit contract.
		- IFACE-GW-006 GatewaySemanticCache lookup/write contract.
		- IFACE-GW-007 GatewayFallbackManager fallback-chain contract.
		- IFACE-GW-008 GatewayTelemetryEmitter correlation contract.
		- IFACE-GW-009 ToolSkillCatcher interception contract.
	handoff:
		target_agent: @4plan
		canonical_artifact: docs/project/prj0000124-llm-gateway/llm-gateway.design.md
		chunked_artifacts: none
		adr_artifact: docs/architecture/adr/0009-llm-gateway-hybrid-split-plane.md
	lesson:
		Pattern: Split-plane gateway projects move faster when contracts are pinned to existing integration points and tied to explicit @4plan task IDs.
		Root cause: Planning drift appears when interface contracts are defined without concrete ownership mapping to integration modules.
		Prevention: Require interface-to-task traceability and acceptance-criteria IDs in the canonical design artifact before handoff.
		First seen: 2026-04-04
		Seen in: prj0000124-llm-gateway
		Recurrence count: 1
		Promotion status: Candidate

