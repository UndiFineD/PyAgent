# conky-real-metrics — Security Scan Results

_Status: DONE_
_Scanner: @8ql | Updated: 2026-03-23_

## Branch Gate
| Check | Result |
|---|---|
| Expected branch | `prj0000047-conky-real-metrics` |
| Observed branch | `prj0000047-conky-real-metrics` |
| Gate | **PASS** |

## Scan Scope
| File | Scan type | Tool |
|---|---|---|
| `backend/app.py` | Python security rules | ruff S (Bandit-equivalent) |
| `backend/app.py` | Manual OWASP review | @8ql |
| `web/apps/Conky.tsx` | Manual XSS / SSRF review | @8ql |
| `pip_audit_results.json` | Dependency CVE audit | pip-audit baseline diff |
| `tests/test_backend_system_metrics.py` | Mock correctness review | @8ql |

## Summary Table
| # | Check | Verdict | Notes |
|---|---|---|---|
| 1 | Information disclosure | **WARN** | CPU/mem/disk/network+iface names exposed unauthenticated; acceptable for local dev, risky if exposed beyond localhost |
| 2 | Injection (user input / subprocess) | **PASS** | Endpoint takes zero parameters; no subprocess calls; no input processing |
| 3 | Path traversal | **PASS** | New endpoint has no file I/O; existing agent-log endpoints use a frozen allowlist (`_VALID_AGENT_IDS`) |
| 4 | XSS (interface name injection) | **PASS** | React auto-escapes all JSX text content; a rogue `interface` value cannot execute as script |
| 5 | SSRF | **PASS** | Frontend fetches relative URL `/api/metrics/system` — no user-supplied URL |
| 6 | DoS (high-frequency polling) | **WARN** | No server-side rate limiting; 2 s interval is client-enforced only; psutil calls are cheap but unbounded |
| 7 | Authentication | **WARN** | Endpoint is unauthenticated — consistent with rest of API; acceptable for localhost-only dev tool |
| 8 | Dependency (psutil) | **PASS** | psutil 7.2.1 — `pip_audit_results.json` shows `"vulns": []`; no new CVEs introduced |

## Ruff S-Rules Scan
```
ruff check backend/app.py --select S
```
**Result: All checks passed** (0 findings)

## Dependency Audit
```json
{ "name": "psutil", "version": "7.2.1", "vulns": [] }
```
No new CVEs vs. committed baseline.

## CodeQL
SKIPPED — CLI not invoked in this review cycle. Python SARIF baseline at `results/python.sarif` is current.

## Rust unsafe check
SKIPPED — `rust_core/` not modified in this PR.

## Findings Detail

### WARN-1 — Information Disclosure
- **Severity:** MEDIUM
- **File:** `backend/app.py`, `GET /api/metrics/system`
- **Description:** The endpoint returns total RAM, used RAM, CPU%, disk I/O rates, and
  per-interface network names + throughput. No authentication is required. This is benign
  for a local developer dashboard (CORS already restricts to `localhost:5173` /
  `localhost:3000`), but would become a meaningful information leak if the backend were
  accidentally bound to `0.0.0.0` and exposed to a LAN or the internet.
- **Recommendation:** Document in `README.md` that the backend must only bind to
  `127.0.0.1`. No code change required for this sprint.

### WARN-2 — No Rate Limiting on `/api/metrics/system`
- **Severity:** LOW
- **File:** `backend/app.py`
- **Description:** Any caller can hammer the endpoint faster than the 2 s client interval.
  `psutil.cpu_percent(interval=None)` returns the cached value from the OS scheduler and
  is O(1); `virtual_memory()`, `net_io_counters()`, and `disk_io_counters()` each make one
  syscall. Realistic attack surface is negligible for a local tool, but there is no
  guard if the port is reachable by multiple clients.
- **Recommendation:** Consider adding `slowapi` or a simple token-bucket decorator in a
  future hardening pass. Not blocking this PR.

### WARN-3 — No Authentication on Any Backend Endpoint
- **Severity:** LOW (in context)
- **File:** `backend/app.py` (entire API surface)
- **Description:** All endpoints — `/health`, `/api/metrics/system`, `/api/agent-log/{id}`,
  `/api/agent-doc/{id}` — require no credentials. This is consistent with the existing
  design and acceptable for a localhost-only tool. The agent-log write endpoint could
  overwrite sensitive files if the backend were exposed publicly.
- **Recommendation:** No change needed for this sprint. Track as a future hardening item.

## Test Mock Review
All tests in `tests/test_backend_system_metrics.py` use `patch("backend.app.psutil", ...)`.
Real psutil is never called during the test suite. Coverage verified:

| Test | psutil call mocked? | Differential state reset? |
|---|---|---|
| `test_endpoint_returns_200` | ✓ | — |
| `test_response_has_correct_shape` | ✓ | — |
| `test_cpu_percent_is_in_valid_range` | ✓ | — |
| `test_memory_fields_correct` | ✓ | — |
| `test_network_entries_have_required_fields` | ✓ | — |
| `test_loopback_and_virtual_interfaces_excluded` | ✓ | — |
| `test_disk_fields_are_non_negative_numbers` | ✓ | — |
| `test_sampled_at_is_positive_and_recent` | ✓ | — |
| `test_first_call_returns_zero_rates` | ✓ | ✓ (resets all 4 globals) |

Mock correctness: **PASS**

## False Positives
| ID | Reason |
|---|---|
| — | None |

## Cleared
All HIGH/CRITICAL findings must be cleared before @9git proceeds.

**No BLOCK items found.**
Current status: **CLEAR — ready for @9git**

## Handoff
- BLOCK items: **0**
- WARN items: **3** (MEDIUM-1, LOW-2, LOW-3) — noted in PR description; do not block merge
- Next agent: **@9git**
