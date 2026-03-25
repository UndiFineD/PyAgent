# opentelemetry-tracing — Project Overview

**ID:** prj0000070  
**Name:** opentelemetry-tracing  
**Branch:** prj0000070-opentelemetry-tracing  
**Priority:** P4  
**Budget:** M  
**Tags:** observability, tracing, backend, rust

## Goal
Add OpenTelemetry span instrumentation to the FastAPI backend for distributed tracing. Provides automatic HTTP request tracing and a Python API for creating custom spans.

## Scope boundary
- **New file:** `backend/tracing.py` — OTel setup, `get_tracer()`, `create_span()` helpers
- **Modified:** `backend/app.py` — initialize OTel on startup
- **Modified:** `requirements.txt` — add opentelemetry packages
- **New file:** `tests/test_tracing.py` — 5 tests

Out of scope: OTLP exporter config (uses in-memory exporter for tests), Rust FFI spans (future work), frontend trace propagation.

## Branch Plan
`prj0000070-opentelemetry-tracing`

## Handoff rule
Merge only after all 5 tests pass.

## Failure rule
If tests fail or imports are broken, return to @6code.
