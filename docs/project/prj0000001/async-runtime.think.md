# async-runtime - Options

_Status: DONE_
_Analyst: @2think | Updated: 2026-03-20_

## Root Cause Analysis
Async execution behavior had to remain stable across environments where Rust runtime bindings may be present or absent.

## Options
### Option A - Rust-first with Python fallback
Use Rust acceleration as preferred path while preserving parity through Python fallback wrappers.

### Option B - Python-only runtime
Keep implementation fully in asyncio with no native acceleration.

## Decision Matrix
| Criterion | Option A | Option B |
|---|---|---|
| Performance headroom | High | Medium |
| Portability without native build | Medium | High |
| Consistency with existing runtime work | High | Medium |

## Recommendation
**Option A** - Keep Rust-first plus fallback to preserve performance opportunities without breaking portability.

## Open Questions
Should long-term queue and timer semantics be fully contract-tested between Rust and fallback paths.
