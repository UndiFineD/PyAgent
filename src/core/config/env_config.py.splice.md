# Splice: src/core/config/env_config.py

This module contains multiple top-level classes/functions which could be split into separate modules:

- EnvVar
- EnvConfigMeta
- EnvConfig
- NamespacedConfig
- LazyEnvVar
- temp_env

Suggested split:
- Separate data models, core logic, and helpers into their own modules to improve testability.
