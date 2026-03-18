# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Development Tools Core Capabilities

To support day‑to‑day operations the toolkit should include a set of small,
focused utilities.  Each item below will typically correspond to one Python
module living under `src/tools` and a CLI entrypoint so the script can be run
from the command line or imported by other tooling for automation.  Every
utility will have a matching `tests/tools/test_<name>.py` that exercises the
module using a temporary workspace and mocks filesystem/network operations.

* **Git & GitHub** – this umbrella covers a collection of helpers:
  - `tools/git_aliases.py` exports functions like `create_feature_branch()` and
    `update_changelog()` which can be wired into shell aliases or pre-commit
    hooks.
  - `tools/gh_pr_checklist.py` can read a YAML template and validate that a
    pull request description meets project standards.
  - Utilities here should manipulate the `gh` CLI and generate markdown for
    changelogs; tests will stub the `gh` binary using the `subprocess` module
    and assert correct arguments.

* **FTP & SSH** – keep a lightweight wrapper around `paramiko` (optional,
  dependency tracked in `require-dev.txt`) and provide `tools/remote.py` with
  helpers such as `upload_files(host, user, paths)` and `run_remote_cmd()`.
  Unit tests can start a local SSH server (via `pytest-ssh` plugin) or simply
  mock the underlying socket layer.

* **SSL certificate management** – implement `tools/ssl_utils.py` with
  functions to request Let’s Encrypt certs (using `acme` library) or generate
  self‑signed ones via `cryptography`.  The module should include
  `check_expiry(path)` which returns expiry dates; a CI job will call this and
  emit warnings.  Tests will use temporary keypairs and ensure expiry logic
  works.

* **IPv4/IPv6 configuration** – `tools/netcalc.py` can expose CLI calculators
  (CIDR-to-range, address validation) and `tools/nettest.py` might spin up a
  docker network to verify dual‑stack connectivity.  These are mostly pure
  Python, making testing trivial with pytest parameterization.

* **NGINX & reverse proxy** – helpers in `tools/nginx.py` to render vhost
  templates from a Jinja2 template, write them into `/etc/nginx/sites-available`,
  and verify syntax (`nginx -t`).  A companion `tools/proxy_test.py` can make
  HTTP requests through a local nginx container to validate rules.  Use a
  small fixture that launches nginx in Docker during tests.

* **Port forwarding & knocking** – modules such as `tools/port_forward.py` and
  `tools/knock.py` will manipulate `iptables` rules (on Linux) or generate
  `pf` lines (on BSD).  They should also include a simple knock-client that
  sends a sequence of zero‑byte packets; tests can simulate this by running
  the client against a dummy UDP server.

* **Polyglot support** – a set of bootstrappers under `tools/boot.py` that
  generate skeleton files (`package.json`, `pyproject.toml`, `Cargo.toml`) and
  provide `init_js_project()`, `init_rust_project()` functions.  The scripts
  will call these helpers with the desired language and create sane defaults.
  Tests simply run them in a tmpdir and verify the files are created with
  expected contents.

By housing these scripts under `src/tools/` or `scripts/` with unit tests, the
team can treat the development ecosystem as first‑class code.  Many of the
above utilities will also be invoked by CI (e.g. SSL expiry check) so they
need to be easily scriptable and have deterministic behavior.

## Implementation Status

A subset of the capabilities enumerated above has already been implemented:

* Git & GitHub helpers are beginning to land in `src/tools/pm` (KPI/risk
  email utilities) and the roadmap/roadmap CLI tools; these modules are
  exercised by their own tests.
* General-purpose bootstrappers reside under `src/roadmap` and `src/context_manager`
  which were originally conceived as development utilities before being
  promoted to core packages.
* No FTP/SSH, SSL, or nginx-specific helpers have been written yet beyond the
  generic scripts in `scripts/` (which are not network-aware).  Likewise,
  netcalc, port forwarding, and polyglot bootstrappers remain on the future
  work list.

This list shows that the design is being followed in spirit: utilities are
placed under `src/tools` and are testable, but many of the specific items
remain to be created by the implementation plan that will follow.
