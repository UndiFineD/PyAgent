# ci-test-parallelization — Think

_Owner: @2think_

## Problem
Single-job sequential test run on CI is slow as test count grows.

## Alternatives

### A — pytest-xdist with `-n auto` (within one job)
Parallelizes within a single machine. Reduces wall time but still single-job.

### B — GitHub Actions matrix + pytest-xdist shard groups (chosen)
Matrix strategy creates N jobs that run simultaneously. Each bucket runs a subset.
`pytest -n auto` within each bucket further parallelizes within runners.

### C — pytest-split (--splits N --group M)
Requires time-based splitting data. Adds complexity.

## Decision
Option B: 3-bucket matrix using `--shard-id=$(( GROUP - 1 ))` and `--num-shards=3` is too custom.
Actually simplest: use `pytest-xdist` `-n auto` in the single job + add matrix for 3 OS/python versions.
But cleanest for pure parallelization: matrix with `shard: [1, 2, 3]` and pytest marker filtering.

Final decision: Use `shard` matrix (1,2,3) + `pytest-xdist` `-n 2` within each shard. 
Sharding done via `--ignore` on shard boundaries, or use `pytest-xdist`'s built-in `--numprocesses`.
Actually the simplest demonstrable approach: run `-n auto` to parallelize workers within the CI runner.
