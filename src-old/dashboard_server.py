#!/usr/bin/env python3
# some environments have incompatible FastAPI/pydantic versions, so
# wrap imports in a try/except. we also prefer functools.lru_cache

r"""LLM_CONTEXT_START

## Source: src-old/dashboard_server.description.md

# Description: `dashboard_server.py`

## Module purpose

(No module docstring found)

## Location
- Path: `src\dashboard_server.py`

## Public surface
- Classes: (none)
- Functions: get_status, get_thoughts, list_artifacts

## Behavior summary
- Has a CLI entrypoint (`__main__`).

## Key dependencies
- Top imports: `fastapi`, `fastapi.middleware.cors`, `typing`, `json`, `os`, `pathlib`, `uvicorn`

## Metadata

- SHA256(source): `6b4e4a95e865cf35`
- Last updated: `2026-01-08 22:51:33`
- File: `src\dashboard_server.py`
## Source: src-old/dashboard_server.improvements.md

# Improvements: `dashboard_server.py`

## Suggested improvements

- Add a concise module docstring describing purpose / usage.

## Notes
- These are suggestions based on static inspection; validate behavior with tests / runs.
- File: `src\dashboard_server.py`

LLM_CONTEXT_END
"""
try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
except Exception:
    # FastAPI not available or pydantic version mismatch; define dummies
    HTTPException = Exception

    class _DummyApp:
        """
        """
