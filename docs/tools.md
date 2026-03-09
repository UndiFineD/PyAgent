# Development Tools

This document catalogs the helper utilities bundled in `src/tools`.
Each module exposes functions that may be invoked from the command line or
imported by other scripts.  Future entries should include:

* `dependency_audit` – scan dependency manifests for outdated or vulnerable packages.
* `metrics` – collect code complexity and coverage metrics.
* `agent_plugins` – plugin loader framework.
* `self_heal` – misconfiguration detection and remediation.

CLI utilities support `--help` output and follow standard exit codes.  See
individual module docstrings for usage examples.
