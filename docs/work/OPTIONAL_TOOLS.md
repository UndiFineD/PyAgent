# Optional Tools for PyAgent

While PyAgent only requires Python 3.10+, the following tools are highly recommended to enhance your development workflow, code quality, and testing experience.

## Development Environment

- **[VS Code](https://code.visualstudio.com/)**: The recommended IDE for PyAgent development.
  - **Python Extension**: Essential for IntelliSense, linting, and debugging.
  - **Pylance**: Performant language server.
  - **Markdownlint**: Helps keep documentation formatted correctly.

- **[PyCharm](https://www.jetbrains.com/pycharm/)**: An excellent alternative IDE with powerful refactoring and debugging capabilities.

## Code Quality & Formatting

These tools are used in our CI pipeline, so having them locally is beneficial.

- **[Black](https://github.com/psf/black)**: The uncompromising Python code formatter.
- **[Flake8](https://flake8.pycqa.org/)**: Enforces style guide adherence and catches syntax errors.
- **[isort](https://pycqa.github.io/isort/)**: Automatically sorts and sections Python imports.
- **[MyPy](https://mypy-lang.org/)**: Static type checker to catch type-related bugs early.

## Testing & Coverage

- **[pytest-cov](https://pytest-cov.readthedocs.io/)**: Generates coverage reports to see which parts of the code are untested.
- **[pytest-xdist](https://pytest-xdist.readthedocs.io/)**: Runs tests in parallel to speed up the test suite.

## CLI Tools

- **[GitHub CLI (gh)](https://cli.github.com/)**: Manage pull requests, issues, and releases from the command line.
- **[pre-commit](https://pre-commit.com/)**: Automatically runs checks (Black, Flake8, etc.) before you commit code.

## Installation

You can install the Python-based tools via pip:

```bash
# Install development tools
pip install black flake8 isort mypy pytest-cov pre-commit
```

To set up pre-commit hooks:

```bash
pre-commit install
```
