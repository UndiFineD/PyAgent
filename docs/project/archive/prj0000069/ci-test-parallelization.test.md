# ci-test-parallelization — Test Plan

_Owner: @5test_

## Tests in `tests/ci/test_ci_parallelization.py`

| # | Name | Description |
|---|------|-------------|
| 1 | `test_ci_workflow_has_matrix` | ci.yml jobs.test has strategy.matrix |
| 2 | `test_ci_matrix_has_three_shards` | matrix.shard has 3 values |
| 3 | `test_requirements_ci_has_xdist` | requirements-ci.txt contains pytest-xdist |
| 4 | `test_ci_uses_parallel_flag` | At least one run step in ci.yml uses -n flag |
