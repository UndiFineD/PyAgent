# ci-test-parallelization — Code Log

_Owner: @6code_

## Files changed

### `requirements-ci.txt`
- Added `pytest-xdist>=3.6`

### `.github/workflows/ci.yml`
- Added matrix strategy (shard: [1,2,3])
- Each shard uses different `--ignore` dirs
- Each shard uses `-n 2`

### `tests/ci/test_ci_parallelization.py` (NEW)
- 4 tests, all passing
