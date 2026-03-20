# unified-transaction-manager - Options

_Status: IN_PROGRESS_
_Analyst: @2think | Updated: 2026-03-20_

## Root Cause Analysis
- Transaction behavior is split across file, memory, process, and context paths.
- Rollback semantics are not standardized across all operation types.
- Existing transaction managers are useful but not orchestrated through one contract.

## Options
### Option A - Unified orchestration layer over existing managers
Create one orchestrator API and keep domain managers as adapters.
Pros: low migration risk, preserves current code, incremental rollout.
Cons: temporary dual abstractions during transition.

### Option B - Full replacement manager
Replace all transaction managers with a single new implementation.
Pros: one model, no adapter layer.
Cons: high migration risk, larger regression surface.

### Option C - Keep separate managers + shared utility helpers
Keep architecture mostly unchanged and add common helpers only.
Pros: smallest change.
Cons: inconsistent lifecycle behavior may remain.

## Decision Matrix
| Criterion | Opt A | Opt B | Opt C |
|---|---|---|---|
| Delivery risk | Low | High | Low |
| Consistency gain | High | High | Medium |
| Implementation speed | Medium | Low | High |
| Backward compatibility | High | Low | High |

## Recommendation
**Option A** - A unified orchestration layer provides consistency with manageable risk and aligns with current PyAgent architecture.

## Open Questions
- Should multi-domain transactions be best-effort rollback or strict all-or-nothing?
- Which existing module becomes the single public entry point?
- What telemetry fields are mandatory for transaction auditability?
