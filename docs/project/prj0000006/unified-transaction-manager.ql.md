# unified-transaction-manager - Security Scan Results

_Status: DONE_
_Scanner: @8ql | Updated: 2026-03-20_

## Scan Scope
| File | Scan type | Tool |
|---|---|---|
| `src/core/UnifiedTransactionManager.py` | ruff S + code_quality | ruff, ql tool |
| `src/core/crdt_bridge.py` | ruff S + code_quality | ruff, ql tool |
| `src/core/security_bridge.py` | ruff S + code_quality | ruff, ql tool |
| `tests/test_unified_transaction_manager.py` | ruff S | ruff |
| `tests/test_UnifiedTransactionManager.py` | ruff S | ruff |
| `tests/test_quality_yaml.py` | ruff S | ruff |

## Findings
| ID | Severity | File | Line | Description |
|---|---|---|---|---|
| F-01 | LOW | `src/core/crdt_bridge.py` | 32 | S607: partial executable path `"cargo"` — build-time only, standard Rust toolchain usage |
| F-02 | LOW | `src/core/crdt_bridge.py` | 46 | S603: subprocess call — binary path fully resolved from `__file__`, no user input |
| F-03 | LOW | `src/core/security_bridge.py` | 30 | S607: partial executable path `"cargo"` — build-time only |
| F-04 | LOW | `src/core/security_bridge.py` | 38,44,50,69 | S603: subprocess calls — binary path fully resolved, all args are Path objects |
| F-05 | INFO | test files | various | S101: assert in pytest tests — expected pytest convention |
| F-06 | INFO | `tests/test_unified_transaction_manager.py` | 68 | S110: try-except-pass in test rollback scenario — test code only |

## False Positives
| ID | Reason |
|---|---|
| F-02, F-04 | S603 fires on all subprocess calls. Binary path derived from `Path(__file__).resolve().parents[2]` — fully absolute, no external input. Not a real vulnerability. |
| F-01, F-03 | S607 fires on `"cargo"`. Standard Rust build tool invocation inside an `if not binary.exists()` guard. Build-time only, not runtime. |
| F-05 | S101 assert is enforced by pytest. Test files are excluded from production security surface. |

## Cleared
- **CRITICAL findings**: 0
- **HIGH findings**: 0
- **MEDIUM findings**: 0
- **LOW/INFO findings**: 6 (all false positives or test-only patterns)
- **pip-audit new CVEs**: 0
- **CodeQL**: ran via `python -m src.tools ql --base main` — code_quality clean on prj006 src files
- **Decision**: CLEAR — no blocker for @9git
