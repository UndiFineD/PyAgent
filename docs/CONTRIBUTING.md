# Contributing to PyAgent

Thank you for your interest in contributing to PyAgent! This document provides guidelines and information for contributors.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [Code Style Guidelines](#code-style-guidelines)
5. [Testing Requirements](#testing-requirements)
6. [Pull Request Process](#pull-request-process)
7. [Documentation Standards](#documentation-standards)
8. [Security Considerations](#security-considerations)

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md):

- **Be respectful**: Treat all contributors with respect and professionalism
- **Be inclusive**: Welcome contributions from everyone, regardless of background
- **Be constructive**: Provide helpful feedback and be open to receiving it
- **Be patient**: Remember that contributors have varying levels of experience

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- VS Code (recommended)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/pyagent.git
cd pyagent

# Create virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
# or
.\.venv\Scripts\Activate.ps1   # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (flake8, black, pytest, etc.)
pip install -r requirements-dev.txt

# Run tests to verify setup
pytest src/

Development Setup
IDE Configuration
VS Code (Recommended):

Create .vscode/settings.json to align with project standards:

File Organization
The project source code is located in the src directory.

Naming Conventions
Type	Convention	Example
Modules	lowercase_underscore	agent_context.py
Classes	PascalCase	ContextAgent
Functions	lowercase_underscore	calculate_priority_score()
Constants	UPPERCASE	DEFAULT_TEMPLATES
Private	Leading underscore	_validate_file_extension()
Code Style Guidelines
Python Code Style
We follow PEP 8 with the following specifics:

Formatter: Black with line length 120 (or project default).
Import sorting: isort.
Type hints: Required for all public functions and class methods.
Docstrings: Google-style docstrings for all public APIs.
Testing Requirements
Test Structure
Tests are currently co-located in the src directory or in a dedicated tests folder depending on the module.

Unit tests should mock external dependencies (filesystem, API calls).
Integration tests should be marked explicitly if they require live environments.
Writing Tests
Running Tests
Pull Request Process
Before Submitting
Create an issue describing the change.
Fork the repository and create a feature branch.
Write tests for new functionality.
Run the full test suite locally (pytest).
Run linting (flake8 src/).
Submit Pull Request.
Branch Naming
Commit Messages
Follow Conventional Commits:

Documentation Standards
Code Documentation
All classes and public methods must have docstrings.
Use type hinting for arguments and return values.
Markdown Documentation
Use clear headings.
Keep line lengths reasonable (soft wrap is preferred in editors, but avoid hard wrapping unless necessary for tables/code).
Use relative links for internal references.
Security Considerations
Sensitive Data
Never commit secrets, API keys, or credentials.
Use environment variables for configuration (e.g., OPENAI_API_KEY, GITHUB_TOKEN).
Reporting Vulnerabilities
For security vulnerabilities, please email the project maintainers directly. Do not open public issues for security concerns.

Questions?
General questions: Open a
Discussion.

Bug reports: Open an Issue.
Feature requests: Open an Issue with [Feature] prefix.
Thank you for contributing to PyAgent! 🎉
