# ci-test-parallelization — Security Review

_Owner: @8ql_

## OWASP checks

| Risk | Finding |
|------|---------|
| CI poisoning | No external actions added; only matrix and --ignore flags changed |
| Dependency confusion | pytest-xdist is a well-known PyPA package with pinned version range |

## Status: PASS
