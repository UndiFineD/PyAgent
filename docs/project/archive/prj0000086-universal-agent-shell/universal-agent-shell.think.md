# universal-agent-shell - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-27_

## Root Cause Analysis

1. Routing is currently fragmented across multiple surfaces with no single intent-to-core contract:
	- `backend/ws_handler.py` routes websocket actions to handlers.
	- `src/agents/BaseAgent.py` provides generic dispatch semantics.
	- `src/core/agent_registry.py` and `src/swarm/agent_registry.py` expose registries but no intent policy.
2. Prior architecture docs describe a Universal Agent shell, but the repo still depends on specialized agent patterns in practice:
	- `docs/architecture/archive/V4_IMPLEMENTATION_DEEP_DIVE.md`
	- `docs/architecture/archive/DIRECTORY_STRUCTURE.md`
3. Full replacement of specialized agents in one pass is high-risk and out of scope for a safe v1.
4. The minimal safe increment is to add dynamic core resolution by intent while preserving legacy specialized routing as fallback.

## Options

### Option A - Intent Router Shim (No Universal Shell in v1)

**Problem statement**
Add intent classification and routing policy first, but keep all execution on existing specialized handlers and existing agent registration paths.

**Proposed approach**
1. Introduce an intent router contract and mapping table for a narrow set of v1 intents.
2. Route intents to existing specialized handlers only.
3. Keep a no-op placeholder for future core loading, but do not resolve cores in runtime yet.

**Pros**
- Lowest implementation risk and fastest delivery.
- No behavioral change in execution engines.
- Easy rollback by disabling intent mapping.

**Cons**
- Does not deliver true dynamic core resolution in v1.
- Defers universal-shell value to later phases.
- Adds one temporary abstraction that may be reworked.

**Research task coverage**
- Literature review: `docs/architecture/archive/V4_IMPLEMENTATION_DEEP_DIVE.md`, `docs/architecture/archive/DIRECTORY_STRUCTURE.md`
- Alternative enumeration: compared against shell-facade and manifest-plugin strategies.
- Constraint mapping: branch scope, minimal-safe-v1 directive, no full specialized-agent replacement.
- Stakeholder impact: backend websocket flow, agent registry users, specialized agent maintainers.
- Risk enumeration: listed below.

**Workspace evidence**
- `backend/ws_handler.py`
- `src/agents/BaseAgent.py`
- `src/core/agent_registry.py`

**Risks**
| Failure mode | Likelihood | Impact |
|---|---|---|
| Intent labels drift from actual specialized capability boundaries | M | M |
| Added router layer increases latency for no functional gain | L | M |
| Temporary abstraction becomes permanent technical debt | M | M |

### Option B - Universal Shell Facade with Controlled Legacy Fallback (Recommended)

**Problem statement**
Deliver dynamic core resolution by intent in v1 while preventing broad regressions by preserving specialized-agent execution as a fallback path.

**Proposed approach**
1. Add a UniversalAgentShell facade that resolves a core by intent for a small allowlist of intents.
2. For intents not in allowlist or on core failure, immediately fall back to existing specialized routing.
3. Keep legacy dispatch path as default for non-migrated intents.
4. Add observability counters for route decision, fallback reason, and error class.

**Pros**
- Meets v1 objective: dynamic core resolution exists in production path.
- Safe rollout: only selected intents migrate.
- Avoids replacing all specialized agents at once.
- Clear migration runway for @3design and @4plan.

**Cons**
- Two routing paths must coexist temporarily.
- Requires explicit guardrails for fallback loops and timeout boundaries.
- Slightly more complexity than router-shim only.

**Research task coverage**
- Literature review: `docs/architecture/archive/V4_IMPLEMENTATION_DEEP_DIVE.md`, `docs/architecture/archive/agents.md`
- Prior-art search: archived universal-shell notes in `docs/architecture/archive/`.
- Constraint mapping: project scope in `docs/project/prj0000086-universal-agent-shell/universal-agent-shell.project.md`, minimal-safe-v1 requirement.
- Stakeholder impact: @3design, backend websocket handlers, registry consumers, observability owners.
- Risk enumeration: listed below.

**Workspace evidence**
- `src/agents/BaseAgent.py`
- `backend/ws_handler.py`
- `src/core/agent_registry.py`
- `docs/architecture/archive/V4_IMPLEMENTATION_DEEP_DIVE.md`

**Risks**
| Failure mode | Likelihood | Impact |
|---|---|---|
| Core resolver misclassifies intent and chooses wrong core | M | H |
| Fallback path can mask core defects and slow migration | M | M |
| Dual-path routing creates inconsistent telemetry semantics | M | M |

### Option C - Manifest-Driven Plugin Resolver with Shadow Evaluation

**Problem statement**
Implement a more generic manifest/plugin intent resolver that can evaluate multiple candidate cores and support future autonomous expansion.

**Proposed approach**
1. Add manifest schema for intent-to-core policy and plugin metadata.
2. Resolve core candidates by score; run selected path and optionally shadow-evaluate fallback.
3. Keep specialized agents as safety path in v1, but collect quality comparisons for migration.

**Pros**
- Most extensible for long-term ecosystem growth.
- Data-driven policy changes without code edits.
- Strong platform foundation for future auto-routing.

**Cons**
- Highest v1 complexity and slower to stabilize.
- Requires additional policy/versioning mechanics.
- Greater chance of overbuilding for initial release.

**Research task coverage**
- Literature review: `docs/architecture/archive/DIRECTORY_STRUCTURE.md` (manifest + registry direction).
- Alternative enumeration: evaluated against shim and facade options.
- Prior-art search: archived universal-shard and agent-catalog references.
- Constraint mapping: minimal safe v1 and no broad replacement mandate.
- Stakeholder impact: policy owners, runtime team, test/quality owners.
- Risk enumeration: listed below.

**Workspace evidence**
- `docs/architecture/archive/DIRECTORY_STRUCTURE.md`
- `src/swarm/agent_registry.py`
- `docs/project/kanban.md`

**Risks**
| Failure mode | Likelihood | Impact |
|---|---|---|
| Manifest/schema churn blocks implementation progress | M | M |
| Scoring policy introduces non-deterministic routing outcomes | M | H |
| Shadow evaluation overhead affects latency/cost in v1 | L | M |

## Decision Matrix

| Criterion | Option A | Option B | Option C |
|---|---|---|---|
| Delivers dynamic core resolution in v1 | No | Yes | Yes |
| Safety for minimal rollout | High | High | Medium |
| Complexity to implement | Low | Medium | High |
| Reuses current specialized agents safely | High | High | Medium |
| Supports gradual migration | Medium | High | High |
| Time-to-value | High | High | Low |
| Long-term extensibility | Medium | High | High |

## Recommendation

**Option B - Universal Shell Facade with Controlled Legacy Fallback**

Rationale:
1. It is the only option that satisfies the stated target directly: dynamic core resolution by intent in v1.
2. It preserves minimal safety by retaining specialized-agent fallback and limiting migration to an intent allowlist.
3. It provides a clean handoff path for @3design to define contracts without forcing all-agent replacement.

## Integration Points

1. Intent ingress and task envelopes:
	- `backend/ws_handler.py`
2. Agent dispatch lifecycle and concurrency boundaries:
	- `src/agents/BaseAgent.py`
3. Registry and lookup surfaces to align with resolver contract:
	- `src/core/agent_registry.py`
	- `src/swarm/agent_registry.py`
4. Architecture alignment and migration guardrails:
	- `docs/architecture/archive/V4_IMPLEMENTATION_DEEP_DIVE.md`
	- `docs/architecture/archive/DIRECTORY_STRUCTURE.md`
5. Project governance and branch/scope constraints:
	- `docs/project/prj0000086-universal-agent-shell/universal-agent-shell.project.md`

## Open Questions for @3design

1. What is the authoritative intent taxonomy for v1 allowlist, and where is it versioned?
2. What is the core resolver contract signature (inputs, outputs, error model)?
3. Which fallback policy is canonical: per-intent fallback chain or global default specialized route?
4. What are timeout and circuit-break boundaries between core path and legacy path?
5. How do we prevent recursive fallback loops in dual-path routing?
6. What observability schema is required for route decisions and fallback reasons?
7. Should resolver policy live in code, config, or a manifest file in v1?
8. What acceptance gate moves an intent from legacy-only to core-enabled?
