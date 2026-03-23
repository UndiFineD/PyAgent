# deployment-operations — Think

_Status: COMPLETE_
_Thinker: @2think | Updated: 2026-03-22_

## Problem Statement
The repository lacked a verifiable deployment skeleton. CI pipelines failed on
fresh checkouts because the `Deployment/` directory hierarchy did not exist and
no GitHub Actions workflow was defined.

## Key Constraints
- Deployment hierarchy must be created by a script (not checked into git as empty dirs).
- CI workflow must be valid YAML that GitHub Actions can parse.
- Tests verify structure presence, not runtime deployment success.
- Solution must be Windows-compatible (pathlib, not bash mkdir).

## Options Explored

### Option A — Shell scripts only
Use bash/PowerShell scripts for directory creation.
**Risk:** Platform inconsistency; shell unavailable in some CI runners.

### Option B — Python setup script + pytest verification (SELECTED)
`scripts/setup_deployment.py` creates the `Deployment/` hierarchy.
`tests/structure/test_deployment_dirs.py` verifies it exists after setup.
GitHub Actions `ci.yml` runs setup then tests.
**Benefit:** Consistent cross-platform execution; testable.

## Decision
Option B selected. Python stdlib + pytest gives the most portable, testable result
without introducing extra dependencies.
