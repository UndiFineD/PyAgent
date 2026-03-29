# prj0000100-repo-cleanup-docs-code - Code Artifacts

_Status: DONE_
_Coder: @6code | Updated: 2026-03-29_

## Implementation Summary
Completed governance implementation evidence for repository policy controls and durable index tracking.

- Canonical allowlist path is enforced at `.github/agents/data/allowed_websites.md` with local-search-first policy text and explicit allowed domains.
- Code structure index is maintained at `.github/agents/data/codestructure.md` with seeded/updated rows, including governance test anchors and required `| file | line | code |` schema.
- Copilot repository instructions include both local-search-first guidance (`rg`/`search_subagent`) and the canonical allowlist path reference `.github/agents/data/allowed_websites.md`.
- Governance tests are present under `tests/docs` and validate allowlist location/content, code-structure index schema/rows, and Copilot instruction policy references.

## Implementation Evidence Mapping
| AC ID | Changed module/file | Validating test(s) | Status |
|---|---|---|---|
| AC-03 | `.github/agents/data/codestructure.md` | `tests/docs/test_codestructure_governance.py` | DONE |
| AC-04 | `.github/agents/data/allowed_websites.md` | `tests/docs/test_allowed_websites_governance.py` | DONE |
| AC-05 | `.github/copilot-instructions.md` | `tests/docs/test_copilot_instructions_governance.py` | DONE |

## Modules Changed
| Module | Change | Lines |
|---|---|---|
| `.github/agents/data/allowed_websites.md` | Canonicalized allowlist location/policy and maintained allowed domains | updated |
| `.github/agents/data/codestructure.md` | Seeded and updated canonical index table rows | updated |
| `.github/copilot-instructions.md` | Added local-search-first and canonical allowlist-path governance guidance | updated |
| `tests/docs/test_allowed_websites_governance.py` | Added governance coverage for canonical allowlist location/content | added |
| `tests/docs/test_codestructure_governance.py` | Added governance coverage for index schema and row validity | added |
| `tests/docs/test_copilot_instructions_governance.py` | Added governance coverage for local-search-first and allowlist-path references | added |

## Test Run Results
```
python -m pytest -q tests/docs/test_allowed_websites_governance.py tests/docs/test_codestructure_governance.py tests/docs/test_copilot_instructions_governance.py
......                                                                   [100%]
6 passed in 1.78s
```

## Deferred Items
none
