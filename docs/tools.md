# Development Tools

This document catalogs the helper utilities bundled in `src/tools`.
Each module exposes functions that may be invoked from the command line or
imported by other scripts.  Future entries should include:

* `dependency_audit` – scan dependency manifests for outdated or vulnerable packages.
* `metrics` – collect code complexity and coverage metrics.
* `agent_plugins` – plugin loader framework.

The initial set of skeleton tools implemented for the 2026‑03‑09
capabilities plan are:

* `git_utils` – wrappers for git/gh operations, PR checklist enforcement, and
  changelog helpers.
* `remote` – SSH/FTP helpers built on `paramiko`.
* `ssl_utils` – certificate creation and expiry checking utilities.
* `netcalc`/`nettest` – CIDR/address calculators and simple dual‑stack
  connectivity tests.
* `nginx`/`proxy_test` – nginx vhost rendering and live configuration validation.
* `port_forward`/`knock` – firewall rule scripting and port-knocking client.
* `boot` – polyglot project bootstrapper that generates starter manifests
  (`package.json`, `pyproject.toml`, `Cargo.toml`).
* `self_heal` – misconfiguration detection and remediation (autonomy support).

The initial set of skeleton tools implemented for the 2026‑03‑09
capabilities plan are:

* `git_utils` – wrappers for git/gh operations, PR checklist enforcement, and
  changelog helpers.
* `remote` – SSH/FTP helpers built on `paramiko`.
* `ssl_utils` – certificate creation and expiry checking utilities.
* `netcalc`/`nettest` – CIDR/address calculators and simple dual‑stack
  connectivity tests.
* `nginx`/`proxy_test` – nginx vhost rendering and live configuration validation.
* `port_forward`/`knock` – firewall rule scripting and port-knocking client.
* `boot` – polyglot project bootstrapper that generates starter manifests
  (`package.json`, `pyproject.toml`, `Cargo.toml`).

Each tool currently has a placeholder `main()` that prints its name; real
functionality will be added iteratively with full unit tests and docs.
CLI utilities support `--help` output and follow standard exit codes.  See
individual module docstrings for usage examples.
