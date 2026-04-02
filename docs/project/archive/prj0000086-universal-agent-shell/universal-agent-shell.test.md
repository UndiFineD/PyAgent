# universal-agent-shell - Test Artifacts

_Status: DONE_
_Tester: @5test | Updated: 2026-03-27_

## Test Plan
Author red-phase tests for the Universal Shell Facade contracts defined in design and plan artifacts.
Focus on behavioral expectations for router normalization/classification, core registry contract, shell dispatch/fallback semantics, and public facade export surface.

## Test Cases
| ID | Description | File | Status |
|---|---|---|---|
| TC-U001 | Facade exports and exception hierarchy contract | tests/test_universal_shell.py | RED |
| TC-U002 | Router normalization and deterministic classification contract | tests/test_UniversalIntentRouter.py | RED |
| TC-U003 | Registry register/resolve/list/duplicate rejection contract | tests/test_UniversalCoreRegistry.py | RED |
| TC-U004 | Shell core route, fallback-once, and validation behavior | tests/test_UniversalAgentShell.py | RED |

## Validation Results
| ID | Result | Output |
|---|---|---|
| TC-U001 | RED | `python -m pytest -q tests/test_universal_shell.py tests/test_UniversalIntentRouter.py tests/test_UniversalCoreRegistry.py tests/test_UniversalAgentShell.py` -> 21 failed in 3.16s |
| TC-U002 | RED | Failure reason verified: explicit behavioral `pytest.fail` message for missing facade/router modules, not raw ImportError/AttributeError terminal failures |
| TC-U003 | RED | `python -m pytest --collect-only -q tests/test_universal_shell.py tests/test_UniversalIntentRouter.py tests/test_UniversalCoreRegistry.py tests/test_UniversalAgentShell.py` -> 21 tests collected |
| TC-U004 | PASS | `python -m pytest -q tests/structure` -> 129 passed in 1.91s |

## Unresolved Failures
1. All 21 red tests currently fail because `src.core.universal` implementation modules do not exist yet.
2. Expected implementation targets for @6code:
	- `src/core/universal/UniversalIntentRouter.py`
	- `src/core/universal/UniversalCoreRegistry.py`
	- `src/core/universal/UniversalAgentShell.py`
	- `src/core/universal/exceptions.py`
	- `src/core/universal/__init__.py`
