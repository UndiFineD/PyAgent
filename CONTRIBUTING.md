# Contributing to PyAgent

Thank you for your interest in contributing!  Please follow these steps:

1. **Fork the repository** and create a feature branch (`feature/short-description`).
2. **Run tests locally** before submitting a PR:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   pytest
   ```
3. **Write a descriptive pull request title** and include a link to this
   repository in the description.  Use conventional commit style for the title
   (e.g. `feat(tools): add new CLI helper`).
4. **Ensure your code passes linting and formatting** (run `scripts/setup_structure.py` for any structure changes).
5. **Add or update documentation** as appropriate (see `docs/` directory).
6. **Do not merge your own PR**; ask for at least one reviewer.

The CI pipeline will run all tests, build the documentation, and verify any
required files (see `tests/docs/test_docs_exist.py`).
