# ci-test-parallelization — Plan

_Owner: @4plan_

## Tasks

1. Add `pytest-xdist>=3.6` to `requirements-ci.txt`
2. Update `.github/workflows/ci.yml`:
   - Add `strategy.matrix.shard: [1, 2, 3]`
   - Add `--ignore` flags per shard to split test load
   - Add `-n 2` for intra-shard parallelism
3. Create `tests/ci/test_ci_parallelization.py`
   - Validate the updated ci.yml structure

## Acceptance criteria
- [ ] ci.yml has a matrix with 3 shards
- [ ] requirements-ci.txt includes pytest-xdist
- [ ] structure tests pass
