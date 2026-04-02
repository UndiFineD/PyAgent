# async-runtime - Security Scan Results

_Status: DONE_
_Scanner: @8ql | Updated: 2026-03-23_

## Scan Scope
| File | Scan type | Tool |
|---|---|---|
| src/core/runtime.py | Runtime interface review | CodeQL/Python |
| src/runtime_py/__init__.py | Async fallback review | CodeQL/Python |
| rust_core/runtime | Native runtime review | CodeQL/Rust |

## Findings
| ID | Severity | File | Line | Description |
|---|---|---|---|---|
| none | none | n/a | n/a | No security findings — scan returned clean |

## False Positives
| ID | Reason |
|---|---|
| none | n/a |

## Cleared
Scan complete. No actionable findings. The async runtime uses `asyncio` exclusively;
no shell injection, SSRF, or unsafe deserialization vectors identified.
`rust_core/runtime` is a cdylib (PyO3 extension), not a standalone binary — attack
surface is limited to the Python-Rust FFI boundary, which is read-only for this module.
