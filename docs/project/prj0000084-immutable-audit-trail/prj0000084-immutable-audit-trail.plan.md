# prj0000084-immutable-audit-trail - Implementation Plan

_Status: DONE_
_Planner: @4plan | Updated: 2026-03-27_

## Overview

Deliver the immutable audit trail as a deterministic, append-only hash-chain package in
`src/core/audit/` with no required edits outside this package for v1. The implementation
is test-first: all tests are authored before production code and executed in strict
module order to prevent dependency churn and partial stubs.

TDD execution rule:
- Red: write each planned test and confirm failure for the expected reason.
- Green: implement the minimum logic to satisfy the failing test.
- Refactor: improve internals without changing public contracts or test outcomes.

---

## Module Implementation Order

`@6code` implementation order is fixed to avoid import cycles and unstable incremental
test runs:

| # | File | Rationale |
|---|------|-----------|
| 1 | `src/core/audit/exceptions.py` | Base exception types required by all modules |
| 2 | `src/core/audit/AuditVerificationResult.py` | Independent result model used by verifier/core |
| 3 | `src/core/audit/AuditEvent.py` | Canonical event model consumed by hasher/core |
| 4 | `src/core/audit/AuditHasher.py` | Deterministic hashing primitive consumed by core |
| 5 | `src/core/audit/AuditTrailCore.py` | Append/read/verify orchestration depends on prior modules |
| 6 | `src/core/audit/AuditTrailMixin.py` | Host convenience layer depends on core/exceptions |
| 7 | `src/core/audit/__init__.py` | Re-export surface after all module symbols exist |

---

## Task List

- [ ] T1 - Define exception hierarchy | Files: `src/core/audit/exceptions.py` | Acceptance: `AuditTrailError` root and all required subclasses are importable and class relationships are correct
- [ ] T2 - Implement verification result model | Files: `src/core/audit/AuditVerificationResult.py` | Acceptance: frozen, slot-based result model with all design fields
- [ ] T3 - Implement immutable event model | Files: `src/core/audit/AuditEvent.py` | Acceptance: canonical dict/json transforms deterministic, schema version enforced
- [ ] T4 - Implement hash canonicalization | Files: `src/core/audit/AuditHasher.py` | Acceptance: canonical bytes deterministic, hash output valid lowercase SHA-256 hex
- [ ] T5 - Implement append/read/verify orchestration | Files: `src/core/audit/AuditTrailCore.py` | Acceptance: append-only JSONL chain, linkage and verifier contracts pass all mapped tests
- [ ] T6 - Implement host mixin adapters | Files: `src/core/audit/AuditTrailMixin.py` | Acceptance: no-core path returns `None`, convenience emitters delegate correctly
- [ ] T7 - Export package API | Files: `src/core/audit/__init__.py` | Acceptance: all public symbols import from package root
- [ ] T8 - Complete TDD validation gates | Files: `tests/test_AuditEvent.py`, `tests/test_AuditHasher.py`, `tests/test_AuditTrailCore.py`, `tests/test_AuditTrailMixin.py`, `tests/test_AuditExceptions.py`, `tests/test_audit_trail.py` | Acceptance: all 18 planned tests pass with lint/type checks green

---

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | Foundation models and exceptions complete | T1, T2, T3 | ⬜ |
| M2 | Hashing and core chain behavior complete | T4, T5 | ⬜ |
| M3 | Integration adapters and exports complete | T6, T7 | ⬜ |
| M4 | Full TDD/quality gates complete | T8 | ⬜ |

---

## Test File Mapping

| Test file | Primary module(s) under test |
|---|---|
| `tests/test_AuditEvent.py` | `AuditEvent.py` |
| `tests/test_AuditHasher.py` | `AuditHasher.py`, `AuditEvent.py` |
| `tests/test_AuditTrailCore.py` | `AuditTrailCore.py`, `AuditHasher.py`, `AuditEvent.py`, `AuditVerificationResult.py` |
| `tests/test_AuditTrailMixin.py` | `AuditTrailMixin.py`, `AuditTrailCore.py` |
| `tests/test_AuditExceptions.py` | `exceptions.py` |
| `tests/test_audit_trail.py` | full-package integration path |

---

## Test Cases (18)

### Unit Tests (U01-U07)

| ID | Test name | Given | When | Then |
|---|---|---|---|---|
| U01 | `test_event_canonical_dict_contains_required_keys_and_schema_version` | Immutable `AuditEvent` with minimal valid fields | `to_canonical_dict()` | Required keys exist and `schema_version == 1` |
| U02 | `test_event_canonical_dict_stable_across_payload_insertion_order` | Two semantically identical payload dicts with different insertion order | Canonical dict and bytes generated | Canonical output is identical |
| U03 | `test_hasher_canonical_event_bytes_deterministic_for_same_event` | Same `AuditEvent` object and equivalent clone | `canonical_event_bytes()` called repeatedly | Byte output is deterministic and equal |
| U04 | `test_compute_event_hash_returns_64_lowercase_hex` | Valid previous hash and canonical bytes | `compute_event_hash()` | Hash length is 64 and matches lowercase hex format |
| U05 | `test_get_last_hash_returns_genesis_for_empty_and_latest_for_non_empty` | Empty temporary audit file, then file with appended events | `get_last_hash()` queried before/after appends | Returns genesis hash when empty and most recent hash when populated |
| U06 | `test_mixin_emit_event_returns_none_when_core_not_configured` | Host class using `AuditTrailMixin` with `_get_audit_trail_core()` returning `None` | `audit_emit_event(...)` | Returns `None` without raising |
| U07 | `test_exception_hierarchy_preserves_specific_types_under_audittrailerror` | Each custom audit exception type | Raised/caught via base class | Base catch works and subclass identity is preserved |

### Integration Tests (I01-I06)

| ID | Test name | Given | When | Then |
|---|---|---|---|---|
| I01 | `test_append_event_uses_genesis_previous_hash_for_first_record` | Empty audit file | First `append_event()` call | First stored record `previous_hash` equals `GENESIS_PREVIOUS_HASH` |
| I02 | `test_append_event_links_previous_hash_to_prior_event_hash` | Audit file with one prior record | Second `append_event()` call | Second record `previous_hash` equals first record `event_hash` |
| I03 | `test_append_event_dict_matches_equivalent_auditevent_hash` | Equivalent event data via explicit `AuditEvent` and `append_event_dict` | Append both forms in isolated files | Produced event hashes are equal for equivalent canonical data |
| I04 | `test_iter_records_preserves_append_order` | Three appended events | `iter_records()` | Records are returned in original append sequence order |
| I05 | `test_verify_file_valid_chain_with_three_events_returns_valid_result` | Untampered 3-event chain | `verify_file()` | `is_valid=True`, counts correct, no error code/message |
| I06 | `test_verify_file_empty_chain_is_valid_and_deterministic` | Empty audit file | `verify_file()` | Valid empty-chain result with deterministic counters |

### Negative Tests (N01-N05)

| ID | Test name | Given | When | Then |
|---|---|---|---|---|
| N01 | `test_verify_file_detects_tampered_payload_in_middle_record` | Valid 3-event chain with middle payload modified post-write | `verify_file()` | `is_valid=False`, `first_invalid_sequence` points to tampered record |
| N02 | `test_verify_file_detects_broken_previous_hash_link` | Valid chain with one record `previous_hash` edited to mismatch | `verify_file()` | Invalid result with chain-link error code |
| N03 | `test_verify_file_detects_malformed_hash_format` | Chain with non-hex or wrong-length hash value | `verify_file()` | Invalid result with malformed-hash error code |
| N04 | `test_verify_file_detects_malformed_json_line` | Audit file containing invalid JSON line | `verify_file()` | Invalid result with parse/serialization error code |
| N05 | `test_fail_closed_true_raises_auditpersistenceerror_on_unwritable_path` | `AuditTrailCore(fail_closed=True)` with unwritable file target | `append_event()` | Raises `AuditPersistenceError` |

---

## Acceptance Criteria Coverage Map

| AC ID | Acceptance criterion | Covered by test IDs |
|---|---|---|
| AC-01 | Canonical event serialization is deterministic and schema-stable | U01, U02, U03 |
| AC-02 | Event hashing is deterministic and format-valid | U04 |
| AC-03 | Genesis and chain linkage behavior is correct | I01, I02 |
| AC-04 | Dict-based append API is semantically equivalent to explicit event append | I03 |
| AC-05 | Append/read order and empty-chain semantics are deterministic | I04, I06 |
| AC-06 | Verifier accepts valid chains and reports accurate counters | I05 |
| AC-07 | Verifier detects tampering, broken links, malformed hash/json with first-failure localization | N01, N02, N03, N04 |
| AC-08 | Fail-closed mode raises persistence errors for unwritable targets | N05 |
| AC-09 | Mixin null-core path and exception hierarchy contracts are preserved | U06, U07 |

---

## Validation Commands

```powershell
& c:\Dev\PyAgent\.venv\Scripts\Activate.ps1

# Unit suites
python -m pytest tests/test_AuditEvent.py tests/test_AuditHasher.py tests/test_AuditExceptions.py -v

# Core + integration suites
python -m pytest tests/test_AuditTrailCore.py tests/test_AuditTrailMixin.py tests/test_audit_trail.py -v

# Full target run with coverage gate
python -m pytest tests/test_AuditEvent.py tests/test_AuditHasher.py tests/test_AuditTrailCore.py `
	tests/test_AuditTrailMixin.py tests/test_AuditExceptions.py tests/test_audit_trail.py `
	--cov=src/core/audit --cov-report=term-missing --cov-fail-under=90

# Type and lint checks
python -m mypy src/core/audit --strict
python -m ruff check src/core/audit

# Artifact/structure regression
python -m pytest tests/structure -q --tb=short
```
