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


## Legacy Project Overview Exception

This project overview predates the modern Project Identity / Goal and Scope / Branch Plan
template. It was authored with an earlier workflow format and has not been migrated.
The project was completed successfully; the deviation is a documentation formatting issue only.

Migration to the modern template is on record with @0master.
