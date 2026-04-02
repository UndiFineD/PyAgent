# prj0000100-repo-cleanup-docs-code - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-29_

## Test Plan
Add deterministic governance tests in `tests/docs/` for canonical allowlist location/content, codestructure schema integrity, and Copilot instruction policy references.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC1 | Canonical allowlist file must exist and root allowed_websites.md must not exist | tests/docs/test_allowed_websites_governance.py | PASS |
| TC2 | Allowed websites policy must include wikipedia.org and github.com | tests/docs/test_allowed_websites_governance.py | PASS |
| TC3 | Codestructure index must exist with `| file | line | code |` header and integer `line` column in rows | tests/docs/test_codestructure_governance.py | PASS |
| TC4 | Copilot instructions must enforce local search first and canonical allowlist path reference | tests/docs/test_copilot_instructions_governance.py | PASS |

## AC-to-Test Matrix
| AC ID | Requirement | Test Case IDs |
|---|---|---|
| AC-03 | Codestructure index exists with canonical schema and valid line anchors | TC3 |
| AC-04 | Allowed websites policy contains required domains | TC1, TC2 |
| AC-05 | Copilot instructions enforce local-first search and canonical allowlist path | TC4 |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC1 | PASS | `pytest -v tests/docs/test_allowed_websites_governance.py` |
| TC2 | PASS | `pytest -v tests/docs/test_allowed_websites_governance.py` |
| TC3 | PASS | `pytest -v tests/docs/test_codestructure_governance.py` |
| TC4 | PASS | `pytest -v tests/docs/test_copilot_instructions_governance.py` |

## Weak-Test Detection Gate
- Gate rule: reject tests that pass on placeholders/stubs, import-only checks, or unconditional assertions.
- Assessment: PASS.
- Evidence:
	- TC1/TC2 validate concrete file-system state and required domain content.
	- TC3 parses real table rows and asserts integer semantics for `line` values.
	- TC4 checks exact policy references in canonical instruction content.
- Placeholder susceptibility: none detected; all tests assert behavior/content contracts.

## Unresolved Failures
none
