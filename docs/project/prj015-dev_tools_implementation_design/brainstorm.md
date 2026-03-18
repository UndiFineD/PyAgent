# Async Runtime Update
> **2026-03-10:** Project migrated to Node.js-like asynchronous runtime; synchronous loops are prohibited by automated tests.

# Development Tools Implementation Considerations

* **Testing:** Each utility should include a corresponding test module under `tests/tools/` verifying its behavior with mocked inputs.  CI pipelines will run these tests automatically; code coverage targets apply.
* **Documentation:** A `docs/tools.md` or README in `src/tools/` should catalog available utilities, usage examples, and configuration options.  CLI tools must support `--help` and follow standard exit codes.
* **Modularity:** Common functionality (e.g. reading config, logging helpers) should live in shared modules so that scripts remain thin.
* **Versioning:** Tools are versioned along with the main project; breaking changes require a minor version bump and clear migration notes.
* **Security:** Scripts that handle keys or network configuration must validate inputs and avoid storing secrets in plaintext.  Provide development versus production modes.
* **Dependencies:** Prefer standard library; any third‑party packages required by tools should be listed in `require-dev.txt` and used sparingly.

## Next Steps

1. Sketch out the first set of utilities (e.g., SSL expiry checker, git alias manager, nginx config generator).
2. Write skeleton scripts with docstrings and CLI entrypoints.
3. Add corresponding unit tests that initially assert files/outputs are created or commands return expected values.
4. Integrate the tools into the existing CI workflow so they run on every push/PR.
5. Use the `scripts/setup_structure.py` approach to create any supporting directories (e.g. `src/tools`, `docs/`).

With these details in place the design is ready for conversion into an implementation plan.

## Implementation Status

Several implementation considerations have already been addressed in the
current repo state:

* Testing conventions are active; utility tests live under `tests/tools/` and
  are executed by CI (e.g. the PM package tests and context/roadmap tests).
* `docs/tools.md` has been drafted (see `docs/tools.md`) listing available
  utilities and usage examples, fulfilling the documentation requirement.
* Shared helpers such as simple logging functions and config readers existed
  earlier in `src/tools/` and are imported by scripts in `scripts/`.
* Dependencies are limited to the standard library plus a few dev packages
  already listed in `requirements.txt` and `requirements-ci.txt`.

Security and versioning guidelines are still aspirational, but the basic
modularity and CI integration goals have been met by the work done so far.
