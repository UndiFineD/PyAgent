# dev-tools-capabilities — Security (QL) Review

_Status: COMPLETE_
_Reviewer: @8ql | Updated: 2026-03-22_

## Findings

### RESOLVED — CWE-78 OS Command Injection (`remote.py`)
- **Prior state**: `subprocess.run(parsed.run, shell=True)` allowed arbitrary shell expansion when `parsed.run` contained user-controlled input.
- **Fix**: All `subprocess.run` calls now receive an explicit `list[str]` argument with `shell=False` (default).
- **Verification**: Grep for `shell=True` returns 0 results in `src/tools/remote.py`. ✅

## Remaining Low Risk Items
| File | Finding | Severity | Disposition |
|------|---------|---------- |------------|
| `ssl_utils.py` | `socket.setdefaulttimeout` mutates global state | Low | Acceptable — local override within function scope |
| `git_utils.py` | `subprocess.run(["git", ...])` uses `PATH` lookup | Info | Acceptable — git is a trusted system binary |

## OWASP Top-10 Checklist
- [x] A01 Broken Access — N/A (no auth)
- [x] A02 Crypto Failures — N/A (TLS read-only inspection)
- [x] A03 Injection — Fixed (remote.py shell=True removed)
- [x] A04 Insecure Design — OK
- [x] A05 Misconfig — OK
- [x] A06 Vulnerable Components — stdlib only
- [x] A07 Auth Failures — N/A
- [x] A08 Data Integrity — OK
- [x] A09 Logging — OK (no secrets logged)
- [x] A10 SSRF — N/A
