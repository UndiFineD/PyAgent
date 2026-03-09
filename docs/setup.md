# Setup & Installation

This guide explains how to prepare a development environment for PyAgent.

## Requirements

- Python 3.11+
- Git
- Docker (optional, used by some integration tests)

## Steps

1. Clone the repository:
   ```powershell
   git clone https://github.com/UndiFineD/PyAgent.git
   cd PyAgent
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Run the setup script to create required directories:
   ```powershell
   python scripts/setup_structure.py
   ```
5. Verify everything is working by running the test suite:
   ```powershell
   pytest
   ```

You can also build the documentation locally using MkDocs:
```powershell
pip install mkdocs mkdocstrings
mkdocs build
```

That's it!  You now have a fully functioning development workspace.