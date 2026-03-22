# dev-tools-structure — Design

_Status: COMPLETE_

## `src/tools/__init__.py` Structure

```python
_SKIP = frozenset({"tool_registry", "__main__", "common"})

for _finder, _name, _ispkg in pkgutil.iter_modules(__path__):
    if _ispkg: continue
    if _name in _SKIP: continue
    try:
        importlib.import_module(f"{__name__}.{_name}")
    except Exception as _exc:
        _log.debug("tools: skipped %s — %s", _name, _exc)
```

## Test Coverage Design
| Test | Assertion |
|------|-----------|
| `test_dev_tools_structure` | `src/tools/` dir created by setup_structure |
| `test_required_tool_modules_exist` | 8 specific `.py` files present |
| `test_pm_subpackage_exists` | `pm/` dir + 4 modules present |
| `test_tools_package_importable` | `import src.tools` does not raise |
