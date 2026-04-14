# jwt-refresh-token-support - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-04-04_

## Test Plan
Phase 1 / first red slice (T-JRT-001) only.

Scope:
- tests/test_backend_refresh_sessions.py
- docs/project/prj0000122-jwt-refresh-token-support/jwt-refresh-token-support.test.md

Approach:
- Author failing-first contract tests for refresh-session lifecycle behavior without implementing production code.
- Use assertion-level checks against the planned API contracts so RED is caused by missing behavior, not import/module absence.
- Keep deterministic fixture isolation via tmp-backed `PYAGENT_AUTH_SESSION_STORE_PATH`.
- Execute one focused selector: `python -m pytest -q tests/test_backend_refresh_sessions.py`.

AC-to-test matrix:
| AC ID | Test Case ID(s) |
|---|---|
| AC-JRT-001 | TC-JRT-001, TC-JRT-002 |
| AC-JRT-003 | TC-JRT-005 |
| AC-JRT-005 | TC-JRT-003, TC-JRT-004 |
| AC-JRT-008 | TC-JRT-004 |

Weak-test detection gate:
- Gate 1: Reject tests that only assert import/existence/`assert True`/no-exception.
- Gate 2: Require at least one concrete HTTP status and payload contract assertion per case.
- Gate 3: RED failure must be assertion mismatch on expected behavior (e.g., 200/401 contract), not `ImportError`/`AttributeError`.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-JRT-001 | Valid API-key bootstrap returns managed token pair via `POST /v1/auth/session`. | tests/test_backend_refresh_sessions.py | RED |
| TC-JRT-002 | Invalid API key is rejected with `401` on bootstrap. | tests/test_backend_refresh_sessions.py | RED |
| TC-JRT-003 | Refresh rotation succeeds once and replay of prior token returns `401`. | tests/test_backend_refresh_sessions.py | RED |
| TC-JRT-004 | Logout revokes refresh-session family and later refresh returns `401`. | tests/test_backend_refresh_sessions.py | RED |
| TC-JRT-005 | Refresh token is never persisted in plaintext in the session store file. | tests/test_backend_refresh_sessions.py | RED |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-JRT-001 | FAIL (RED expected) | `assert 404 == 200` for `POST /v1/auth/session` bootstrap success contract |
| TC-JRT-002 | FAIL (RED expected) | `assert 404 == 401` for invalid API-key bootstrap rejection contract |
| TC-JRT-003 | FAIL (RED expected) | bootstrap precondition fails (`assert 404 == 200`), so refresh/replay lifecycle is not yet implemented |
| TC-JRT-004 | FAIL (RED expected) | bootstrap precondition fails (`assert 404 == 200`), so logout/revocation lifecycle is not yet implemented |
| TC-JRT-005 | FAIL (RED expected) | bootstrap precondition fails (`assert 404 == 200`), so persistence contract cannot pass yet |

## Unresolved Failures
- Selector: `c:/Dev/PyAgent/.venv/Scripts/python.exe -m pytest -q tests/test_backend_refresh_sessions.py`
- Summary: `5 failed in 4.77s`
- Failure signatures:
	- `tests/test_backend_refresh_sessions.py::test_auth_session_bootstrap_returns_managed_token_pair` -> `assert 404 == 200`
	- `tests/test_backend_refresh_sessions.py::test_auth_session_bootstrap_with_invalid_api_key_returns_401` -> `assert 404 == 401`
	- `tests/test_backend_refresh_sessions.py::test_refresh_rotation_rejects_replayed_refresh_token` -> `assert 404 == 200`
	- `tests/test_backend_refresh_sessions.py::test_logout_revokes_refresh_session_family` -> `assert 404 == 200`
	- `tests/test_backend_refresh_sessions.py::test_refresh_token_is_not_persisted_in_plaintext` -> `assert 404 == 200`
- Qualifying RED check:
	- Failure class is assertion-level HTTP behavior mismatch for missing route/contract implementation.
	- Non-qualifying failures absent: `ImportError`, `AttributeError`.
