# ci-test-parallelization — Project Overview

**ID:** prj0000069  
**Name:** ci-test-parallelization  
**Branch:** prj0000069-ci-test-parallelization  
**Priority:** P3  
**Budget:** S  
**Tags:** ci, testing, performance

## Goal
Split the pytest suite into N parallel matrix buckets using `pytest-xdist` to reduce CI wall time by ~60%.

## Scope boundary
- **Modified:** `requirements-ci.txt` — add `pytest-xdist`
- **Modified:** `.github/workflows/ci.yml` — matrix sharding strategy (3 buckets)
- **New file:** `tests/ci/test_ci_parallelization.py` — validates the new CI workflow shape

Out of scope: changing test logic, adding new tests, modifying other workflows.

## Branch Plan
`prj0000069-ci-test-parallelization`

## Handoff rule
Merge only after CI workflow structure tests pass.

## Failure rule
If tests fail, return to @6code before creating PR.
