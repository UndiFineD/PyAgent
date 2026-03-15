# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Plugin System Design

Plugins allow third‑party extensions to augment or replace core behaviours
without touching the main codebase.  The `plugins/` directory in `src` will
eventually house community‑contributed logic units, whereas a central
`PluginManager` handles discovery and loading.

## Legacy Evidence

Several variants of `PluginManager.py` exist in `src-old` (under
`core/base/managers`, `classes/fleet`, `classes/base_agent/managers`), which
points to a historically flexible registry capable of loading plugins from
different domains (agent plugins, fleet plugins, etc.).  The list has
multiple entries referencing `PluginManager.py` as unimplemented items.

## Design Goals

- **Dynamic discovery** – locate plugin packages via filesystem scanning or
  entry points; support lazy instantiation.
- **Isolation & safety** – sandbox plugin execution, catch exceptions, enforce
  version compatibility.
- **Metadata & documentation** – each plugin exposes a name, description,
  author, version, and required core version.
- **Hot-reload support** – allow enabling/disabling plugins at runtime without
  restarting the system.

## Example Registry API

```python
class PluginManager(BaseCore):
    def register(self, plugin: PluginBase) -> None: ...
    def load_from_path(self, path: Path) -> PluginBase: ...
    def list_plugins(self) -> list[str]: ...
    def enable(self, name: str) -> None: ...
    def disable(self, name: str) -> None: ...
```

## Brainstorm Topics

- Permission model for plugins (what APIs may they call?).
- Plugin dependency resolution and compatibility checking.
- CLI for managing plugins (`pyagent plugins add`, `remove`, `update`).
- Metrics/telemetry emitted by plugins for usage analytics.

*Base descriptions derived from legacy `PluginManager` modules.*