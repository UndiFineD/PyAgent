# prj0000082 — agent-execution-sandbox — Quality & Security Review

_Agent: @8ql | Date: 2026-03-26 | Branch: prj0000082-agent-execution-sandbox_
_Status: DONE_

---

## Branch Gate
| Check | Result |
|---|---|
| Expected branch | `prj0000082-agent-execution-sandbox` |
| Observed branch | `prj0000082-agent-execution-sandbox` |
| **Gate** | **✅ PASS** |

---

## Scope
| File | Change type |
|---|---|
| `src/core/sandbox/__init__.py` | Created |
| `src/core/sandbox/SandboxConfig.py` | Created |
| `src/core/sandbox/SandboxViolationError.py` | Created |
| `src/core/sandbox/SandboxedStorageTransaction.py` | Created |
| `src/core/sandbox/SandboxMixin.py` | Created |
| `tests/test_sandbox.py` | Created |
| `tests/test_SandboxConfig.py` | Created |
| `tests/test_SandboxMixin.py` | Created |
| `tests/test_SandboxViolationError.py` | Created |
| `tests/test_SandboxedStorageTransaction.py` | Created |
| `src/core/reasoning/EvaluationEngine.py` | Modified (sync loop fix) |

No `.github/workflows/` files changed — workflow injection scan skipped.

---

## Part A — Security Findings

### [INFO] S101 — assert in module-level validate() helpers
**File:** `src/core/sandbox/SandboxConfig.py:76`, `SandboxMixin.py:73`, `SandboxViolationError.py:52`, `SandboxedStorageTransaction.py:165`
**Rule:** ruff S101
**Description:** Four `validate()` helper functions use `assert` to confirm their own class is importable. These cannot be stripped by `-O` in a context that matters; the `validate()` pattern is intentional across this codebase (same pattern present in six other modules).
**Recommendation:** No action required — INFO only. Not a production code path.

### [LOW] Information exposure in SandboxViolationError reason field
**File:** `src/core/sandbox/SandboxedStorageTransaction.py:88-91`
**Description:** The `_validate_path()` error message includes the full allowed_paths list in the `reason` field:
```python
reason=f"path not in allowed_paths: {self._sandbox.allowed_paths}"
```
This exposes the allowlist to any caller that can catch and inspect the exception. In a multi-agent environment an untrusted agent triggering a violation learns which directories are in the allowlist.
**Exploitability:** LOW — knowing the allowlist does not allow bypassing the resolve-based check. Informational advantage only.
**Recommendation:** Replace with a generic reason: `"path not in allowed_paths"` (drop the list). Non-blocking.

### Path Traversal Security Analysis (A05) — PASS
| Sub-check | Result |
|---|---|
| `Path.resolve()` called before allowlist comparison | ✅ `_is_subpath` resolves both sides |
| `write()` validates BEFORE queuing op | ✅ `_validate_path(path)` precedes `super().write()` |
| `delete()` validates BEFORE queuing op | ✅ `_validate_path(path)` precedes `super().delete()` |
| `mkdir()` validates BEFORE queuing op | ✅ `_validate_path(path)` precedes `super().mkdir()` |
| `commit()` validates legacy target BEFORE writing | ✅ guard present: `if self._target is not None: self._validate_path(...)` |
| Empty `allowed_paths` = deny-all | ✅ `any([])` is `False` → always raises |
| Symlink escapes caught | ✅ `resolve()` follows symlinks before comparison |
| `../` traversal sequences caught | ✅ `resolve()` collapses traversal before comparison |

### Host Injection Analysis (A03) — PASS
| Sub-check | Result |
|---|---|
| Host validation uses exact string match | ✅ `host not in self._sandbox_config.allowed_hosts` |
| Crafted host `"allowed.host:443/../evil"` bypass | ✅ No match — rejected |
| `eval()` / `exec()` / `subprocess` / shell interpolation | ✅ None found |
| `allow_all_hosts` default | ✅ `False` |

### Dependency CVE Audit — PASS
**Baseline (`pip_audit_results.json`):** 0 dependencies with vulnerabilities.
No new dependencies introduced by this PR.

### mypy --strict — PASS
```
Success: no issues found in 5 source files
```

---

## Part B — Quality Gaps

| # | Type | Description | Responsible agent | Blocking? |
|---|---|---|---|---|
| 1 | INFO | `__all__` not sorted (RUF022) in `__init__.py` | @6code | No |
| 2 | INFO | `Optional[X]` instead of `X \| None` (UP045, 2 uses) | @6code | No |
| 3 | INFO | Quoted return type `"SandboxConfig"` (UP037) | @6code | No |
| 4 | INFO | TC001/TC003 imports could move to TYPE_CHECKING block | @6code | No |
| 5 | DESIGN DRIFT | `_is_subpath` is a `@staticmethod` on class in impl vs module-level function in design.md | @3design | No — both approaches are correct |

**Plan vs delivery:** All 5 production files + 5 test files delivered. ✅
**Test count:** 32 passed, 1 skipped (symlink on Windows — expected) vs 19 planned — exceeded. ✅
**Coverage:** 100% on all 5 sandbox modules. ✅
**Pre-existing failures:** 4 (unchanged from baseline, unrelated to this PR). ✅
**All 9 project artifacts present:** ✅

---

## Part C — Lessons Written

| Pattern | Agent memory file | Recurrence count | Promoted to rule? |
|---|---|---|---|
| `SandboxViolationError.reason` exposes allowlist — caller gains enumeration info | `8ql.memory.md` | 1 (new) | No (threshold = 2) |

---

## OWASP Coverage

| Category | Status | Notes |
|---|---|---|
| A01 — Broken Access Control | ✅ PASS | Path allowlist enforced before every I/O op |
| A02 — Cryptographic Failures | ✅ N/A | No crypto in scope |
| A03 — Injection | ✅ PASS | No eval/exec; host check is exact-match string comparison |
| A04 — Insecure Design | ✅ PASS | Empty allowlist → deny-all by construction |
| A05 — Security Misconfiguration | ✅ PASS | `allow_all_hosts=False` default; no open policies |
| A06 — Vulnerable Components | ✅ PASS | 0 CVEs in baseline; no new dependencies |
| A07 — Auth Failures | ✅ N/A | No auth layer in scope |
| A08 — Software Integrity | ✅ PASS | No new deps; no deserialization; `S301` clean |
| A09 — Logging / Monitoring | ✅ N/A | Not in scope |
| A10 — SSRF | ✅ PASS | Host allowlist in `_validate_host()` prevents SSRF |

---

## Verdict

| Gate | Status |
|---|---|
| Security — ruff-S | ✅ PASS (4× S101 in validate() helpers — INFO only) |
| Security — mypy --strict | ✅ PASS (0 errors) |
| Security — pip-audit CVEs | ✅ PASS (0 vulnerabilities) |
| Security — Workflow injection | ✅ N/A (no workflow files changed) |
| Security — OWASP A05 path traversal | ✅ PASS |
| Security — OWASP A03 injection | ✅ PASS |
| Plan vs delivery | ✅ PASS (all tasks delivered; test count exceeded) |
| AC vs test coverage | ✅ PASS (all 19 ACs covered; 32 pass) |
| Docs vs implementation | ✅ PASS (minor design drift on `_is_subpath` — functionally equivalent) |
| **Overall** | **✅ CLEAR → @9git** |

### Rationale
All security-critical controls (path resolve-before-compare, deny-all on empty allowlist,
validate-before-I/O, default-deny host policy) are correctly implemented with no bypasses
found. The single LOW finding (allowlist exposed in error reason) is informational only and
does not allow bypass of any control. No blocking issues.
