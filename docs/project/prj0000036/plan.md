# Prj0000036 Plugin System

_Status: IN_PROGRESS_
_Planner: @4plan | Updated: 2026-06-13_

## Goal

Build a `PluginManager` that discovers, loads, isolates, and manages
third-party plugins without touching the main codebase. Plugins augment or
replace core behaviours; the manager enforces version compatibility, hot-reload,
and safety isolation.

## Registry API

```python
class PluginManager(BaseCore):
    def register(self, plugin: PluginBase) -> None: ...
    def load_from_path(self, path: Path) -> PluginBase: ...
    def list_plugins(self) -> list[str]: ...
    def enable(self, name: str) -> None: ...
    def disable(self, name: str) -> None: ...
```

## Design Goals

- **Dynamic discovery** — filesystem scan or entry-point discovery; lazy
  instantiation.
- **Isolation & safety** — sandbox execution, catch all exceptions, enforce
  version and API compatibility.
- **Metadata** — every plugin exposes name, description, author, version, and
  required core version.
- **Hot-reload** — enable/disable plugins at runtime without restart.

## Tasks

- [ ] Define `PluginBase` ABC with required metadata properties
- [ ] Implement `PluginManager.load_from_path()` with exception isolation
- [ ] Implement filesystem and entry-point discovery
- [ ] Add version compatibility checking on load
- [ ] Implement `enable()` / `disable()` runtime toggle and hot-reload
- [ ] Define plugin permission model (allowlisted core APIs)
- [ ] Implement dependency resolution between plugins
- [ ] Add CLI commands: `pyagent plugins add`, `remove`, `update`, `list`
- [ ] Emit metrics/telemetry from `PluginManager` for usage analytics
- [ ] Write tests: `tests/test_plugin_manager.py`
- [ ] Document plugin authoring guide in `docs/`

## Milestones

| # | Milestone | Tasks | Status |
|---|---|---|---|
| M1 | PluginBase and manager skeleton | T1, T2 | NOT_STARTED |
| M2 | Discovery and version checks | T3, T4 | NOT_STARTED |
| M3 | Hot-reload and safety | T5, T6 | NOT_STARTED |
| M4 | Dependency resolution and CLI | T7, T8 | NOT_STARTED |
| M5 | Metrics, tests, docs | T9, T10, T11 | NOT_STARTED |
