# transaction-managers-full — Security Scan Results

_Status: NOT_STARTED_
_Scanner: @8ql | Updated: 2026-03-22_

## Scan Scope
| File | Scan type | Tool |
|---|---|---|
| src/transactions/StorageTransactionManager.py | Crypto, path traversal, atomic write | CodeQL + manual |
| src/transactions/MemoryTransactionManager.py | Crypto, key exposure | CodeQL + manual |
| src/transactions/ProcessTransactionManager.py | Command injection, SSRF | CodeQL + manual |
| src/transactions/ContextTransactionManager.py | UUID predictability, recursion | CodeQL + manual |
| src/transactions/BaseTransaction.py | Contract safety | CodeQL |

## Key Security Requirements
- `StorageTransaction`: AES-256-GCM encryption for `write()` when user_id scoped
- `MemoryTransaction`: encrypted blocks when `encrypt=True`
- `ProcessTransaction`: no shell=True; subprocess args must not accept user-controlled strings without validation
- `ContextTransaction`: UUID from `uuid.uuid4()` (random, not predictable)
- No hardcoded keys, secrets, or credentials in any transaction module

## Findings
| ID | Severity | File | Line | Description |
|---|---|---|---|---|

## False Positives
| ID | Reason |
|---|---|

## Cleared
Current status: NOT_STARTED
