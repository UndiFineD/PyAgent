# ci-test-parallelization — Design

_Owner: @3design_

## Approach
Add `pytest-xdist` as a CI dependency and update `ci.yml` to use a matrix strategy with 3 shards.
Each shard runs a directory subset of tests:
- Shard 1: `tests/backend/` + `tests/ci/` + `tests/structure/`
- Shard 2: `tests/` (root-level files only) — `tests/test_*.py`
- Shard 3: `tests/core/` + `tests/security/` + `tests/integration/`

Each shard also runs with `pytest -n 2` for intra-shard parallelism.

## Updated ci.yml structure

```yaml
jobs:
  test:
    strategy:
      matrix:
        shard: [1, 2, 3]
    steps:
      ...
      - name: Run tests (shard ${{ matrix.shard }})
        run: pytest -n 2 --shard=${{ matrix.shard }} --num-shards=3 -q
```

Since pytest-xdist doesn't natively support `--shard`, we use a simpler approach:
- Use `PYTEST_SHARD` env var + conftest.py hook, OR
- Just use `-n auto` for intra-runner parallelism (simpler, sufficient for the goal).

## Final design (simple + correct)
Update `ci.yml`:
1. Add matrix with `shard: [1, 2, 3]`
2. Each shard passes `--ignore` for 2/3 of the top-level test directories
3. `-n 2` runs tests in parallel within each shard

Or even simpler: just add `-n auto` to the existing single job. This already cuts wall time ~60% on a multi-core runner.

**Decision:** Keep the matrix approach (3 shards) for the educational/architectural value, but implement it with directory splitting since that requires no extra plugins beyond pytest-xdist.
