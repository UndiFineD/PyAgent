# dev-tools-utilities — Design

_Status: COMPLETE_

## Test Isolation Pattern
```python
@pytest.fixture(autouse=True)
def _clean_registry():
    snapshot = dict(_REGISTRY)
    yield
    _REGISTRY.clear()
    _REGISTRY.update(snapshot)
```
This ensures no test leaks registrations to subsequent tests.

## Tests Covered
| Test | Covers |
|------|--------|
| register + retrieve | basic registration |
| duplicate same desc is idempotent | no re-raise |
| duplicate different desc raises | ValueError |
| list_tools sorted | alphabetical sort |
| run_tool int result | dispatch to int-returning fn |
| run_tool unknown raises | KeyError |
| Tool frozen dataclass | immutability |
| main cli list | prints tool names |
| main cli run | dispatches and returns exit code |
| main cli unknown | returns 1 |
