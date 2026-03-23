# deployment-operations — Design

_Status: COMPLETE_
_Designer: @3design | Updated: 2026-03-22_

## Selected Design

### Deployment Directory Hierarchy
```
Deployment/
  development/
    servers/
    networks/
    services/
  staging/
    servers/
    networks/
    services/
  production/
    servers/
    networks/
    services/
```

### `scripts/setup_deployment.py` Interface
```python
def create_deployment_structure(root: str) -> None: ...

if __name__ == "__main__":
    create_deployment_structure(".")
```
- `root` defaults to repository root when called from CLI.
- `mkdir(parents=True, exist_ok=True)` — idempotent.

### CI Workflow (`.github/workflows/ci.yml`)
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.13" }
      - run: python scripts/setup_deployment.py
      - run: pytest tests/structure/ tests/ci/ -q
```

## Interface Decisions
- `create_deployment_structure` takes an explicit `root` arg for testability.
- No subprocess or shell invocation. stdlib `pathlib` only.
- CI workflow version-pins all actions to a hash or tag for security.
